from typing import Dict, List
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from .objectives import evaluate_design
from dataclasses import dataclass

@dataclass
class Bounds:
    apex1_deg: tuple
    apex2_deg: tuple
    rel_rot_deg: tuple
    thick1_mm: tuple
    thick2_mm: tuple

def random_params(bounds: Bounds, rng: np.random.Generator):
    def sample(pair):
        return float(rng.uniform(pair[0], pair[1]))
    return dict(
        apex1_deg=sample(bounds.apex1_deg),
        apex2_deg=sample(bounds.apex2_deg),
        rel_rot_deg=sample(bounds.rel_rot_deg),
        thick1_mm=sample(bounds.thick1_mm),
        thick2_mm=sample(bounds.thick2_mm)
    )

def nsga2_like(glasses: pd.DataFrame, site: Dict, cfg: Dict, wavelengths_nm: List[float], zenith_angles: List[float]):
    rng = np.random.default_rng(int(cfg.get('seed', 0)))
    bounds = Bounds(apex1_deg=(-3,3), apex2_deg=(-3,3), rel_rot_deg=(0,180), thick1_mm=(5,30), thick2_mm=(5,30))
    max_pairs = int(cfg.get('max_pairs', 200))
    glasses_sample = glasses.sample(min(max_pairs, len(glasses)), random_state=int(cfg.get('seed',0))).reset_index(drop=True)
    pairs = []
    for i in range(len(glasses_sample)):
        for j in range(i, len(glasses_sample)):
            pairs.append((glasses_sample.loc[i].to_dict(), glasses_sample.loc[j].to_dict()))
    pairs = pairs[:max_pairs]
    pop_size = int(cfg['optimizer'].get('pop_size', 48))
    generations = int(cfg['optimizer'].get('generations', 10))
    population = [random_params(bounds, rng) for _ in range(pop_size)]
    weights = {k: float(v) for k,v in cfg.get('objective_weights', {'chromatic_residual':1.0,'pupil_wobble':0.5,'throughput_loss':0.3}).items()}
    results = []
    for gen in range(generations):
        def eval_pair(g1, g2, params):
            agg = {'chromatic_residual':0.0, 'pupil_wobble':0.0, 'throughput_loss':0.0}
            for z in zenith_angles:
                out = evaluate_design(g1, g2, params, wavelengths_nm, float(z), site)
                for k in agg:
                    agg[k] = max(agg[k], out[k])
            score = weights['chromatic_residual']*agg['chromatic_residual'] +                     weights['pupil_wobble']*agg['pupil_wobble'] +                     weights['throughput_loss']*agg['throughput_loss']
            return dict(score=score, g1=g1['name'], g2=g2['name'], params=params, agg=agg)
        jobs = []
        for (g1,g2) in pairs:
            for p in population:
                jobs.append((g1,g2,p))
        evaluated = Parallel(n_jobs=cfg.get('parallel', {}).get('n_workers', 4))(delayed(eval_pair)(g1,g2,p) for (g1,g2,p) in jobs)
        evaluated.sort(key=lambda x: x['score'])
        elites = evaluated[:min(64, len(evaluated))]
        results.extend(elites)
        new_pop = []
        for e in elites[:min(len(elites), pop_size//2)]:
            new_pop.append(e['params'])
            p = e['params'].copy()
            p['apex1_deg'] += float(rng.normal(0, 0.2))
            p['apex2_deg'] += float(rng.normal(0, 0.2))
            p['rel_rot_deg'] = float(np.clip(p['rel_rot_deg'] + rng.normal(0, 5), 0, 180))
            p['thick1_mm'] = float(np.clip(p['thick1_mm'] + rng.normal(0, 1.0), 1, 50))
            p['thick2_mm'] = float(np.clip(p['thick2_mm'] + rng.normal(0, 1.0), 1, 50))
            new_pop.append(p)
        while len(new_pop) < pop_size:
            new_pop.append(random_params(bounds, rng))
        population = new_pop
    rows = []
    for e in results:
        row = dict(score=e['score'], glass1=e['g1'], glass2=e['g2'], **e['params'], **e['agg'])
        rows.append(row)
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values('score').drop_duplicates(subset=['glass1','glass2']).reset_index(drop=True)

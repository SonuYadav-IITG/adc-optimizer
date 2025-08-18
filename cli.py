import argparse, yaml
from .io_glass import load_catalogs
from .search import nsga2_like
from .report import save_markdown
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', required=True)
    ap.add_argument('--optimize', required=True)
    ap.add_argument('--out', default='results/adc_report.md')
    args = ap.parse_args()
    site = yaml.safe_load(open(args.site))
    cfg = yaml.safe_load(open(args.optimize))
    glasses = load_catalogs(cfg['candidate_glass_catalogs'])
    wavelengths = site['wavelength_nm']
    zeniths = site.get('zenith_angles_deg', [30.0])
    Path(Path(args.out).parent).mkdir(parents=True, exist_ok=True)
    df = nsga2_like(glasses, site, cfg, wavelengths, zeniths)
    save_markdown(df, args.out, topn=30)
    print(f"Saved report to {args.out}")

if __name__ == '__main__':
    main()

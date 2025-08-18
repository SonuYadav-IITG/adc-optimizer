from typing import List
import pandas as pd

def load_catalog(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if 'name' not in df.columns:
        df = df.reset_index().rename(columns={'index': 'name'})
    df['catalog'] = path
    return df

def load_catalogs(paths: List[str]) -> pd.DataFrame:
    frames = []
    for p in paths:
        frames.append(load_catalog(p))
    return pd.concat(frames, ignore_index=True)

def parse_sellmeier_coeffs(coeffs_field: str):
    if pd.isna(coeffs_field):
        raise ValueError("Empty Sellmeier coeffs field")
    s = str(coeffs_field).replace(',', ';')
    parts = [float(x) for x in s.split(';') if x.strip()!='']
    if len(parts) < 6:
        raise ValueError(f"Expected 6 Sellmeier coefficients, got {len(parts)}: {parts}")
    B1,B2,B3,C1,C2,C3 = parts[:6]
    return dict(B1=B1, B2=B2, B3=B3, C1=C1, C2=C2, C3=C3)

from typing import Sequence, Dict
import numpy as np
from .io_glass import parse_sellmeier_coeffs

def n_sellmeier_um(wavelength_um: float, coeffs: Dict[str, float]) -> float:
    lam2 = float(wavelength_um)**2
    B1,B2,B3 = coeffs['B1'], coeffs['B2'], coeffs['B3']
    C1,C2,C3 = coeffs['C1'], coeffs['C2'], coeffs['C3']
    val = 1.0 + B1*lam2/(lam2 - C1) + B2*lam2/(lam2 - C2) + B3*lam2/(lam2 - C3)
    return float(np.sqrt(val))

def dispersion_curve(row, wavelengths_nm: Sequence[float]):
    coeffs = parse_sellmeier_coeffs(row.get('coeffs', row.get('Coeff', None)))
    wl_um = (np.asarray(wavelengths_nm) / 1000.0).astype(float)
    return np.array([n_sellmeier_um(x, coeffs) for x in wl_um])

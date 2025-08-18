from typing import Sequence, Dict
import numpy as np

def refractive_index_air(wavelength_um: float, pressure_Pa: float, temperature_C: float, RH: float, CO2_ppm: float=450.0) -> float:
    T = temperature_C + 273.15
    lam_um = float(wavelength_um)
    sigma2 = (1.0/lam_um)**2
    n_minus_1 = (1e-8) * ( 5792105.0 / (238.0185 - sigma2) + 167917.0 / (57.362 - sigma2) )
    n_minus_1 *= (pressure_Pa / 101325.0) * (288.15 / T)
    e = RH * 0.01 * 610.94 * np.exp((17.625 * temperature_C) / (temperature_C + 243.04))
    n_minus_1 += -1e-10 * e
    return 1.0 + float(n_minus_1)

def differential_refraction(wavelengths_nm: Sequence[float], zenith_angle_deg: float, site: Dict) -> np.ndarray:
    wl_um = np.asarray(wavelengths_nm) / 1000.0
    n = np.array([refractive_index_air(w, site['pressure_Pa'], site['temperature_C'], site.get('relative_humidity', 0.2)) for w in wl_um])
    n0 = np.mean(n)
    Z = np.deg2rad(zenith_angle_deg)
    delta_rad = (n - n0) * np.tan(Z)
    return np.rad2deg(delta_rad) * 3600.0

from typing import Sequence, Dict
import numpy as np

def prism_deviation(n: Sequence[float], apex_angle_deg: float) -> np.ndarray:
    A = np.deg2rad(float(apex_angle_deg))
    return (np.asarray(n) - 1.0) * A

def pupil_wobble_estimate(apex_deg: float, thickness_mm: float, n_curve: Sequence[float]) -> float:
    A = np.deg2rad(float(apex_deg))
    n_mean = float(np.mean(n_curve))
    wobble = (n_mean - 1.0) * A * (float(thickness_mm) / 1000.0)
    return float(wobble)

def adc_residual_dispersion(n1_curve: Sequence[float], n2_curve: Sequence[float],
                            apex1_deg: float, apex2_deg: float, rel_rot_deg: float,
                            wavelengths_nm: Sequence[float], zenith_angle_deg: float, site: Dict) -> np.ndarray:
    wl = np.asarray(wavelengths_nm)
    dev1 = prism_deviation(n1_curve, apex1_deg)
    dev2 = prism_deviation(n2_curve, apex2_deg)
    theta = np.deg2rad(float(rel_rot_deg))
    adc_x = dev1 + dev2 * np.cos(theta)
    adc_y = dev2 * np.sin(theta)
    adc_mag = np.sqrt(adc_x**2 + adc_y**2)
    from .atmos import differential_refraction
    atm_arcsec = differential_refraction(wl, zenith_angle_deg, site)
    atm_rad = np.deg2rad(atm_arcsec / 3600.0)
    adc_norm = adc_mag - np.mean(adc_mag)
    residual = atm_rad - adc_norm
    return residual

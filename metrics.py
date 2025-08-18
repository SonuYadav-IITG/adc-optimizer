import numpy as np

def chromatic_rms(residual_rad):
    arcsec = np.rad2deg(np.asarray(residual_rad)) * 3600.0
    return float(np.sqrt(np.mean(arcsec**2)))

def throughput_loss(glass1, glass2, wavelengths_nm):
    per_surface_loss = 0.002
    n_surfaces = 4
    loss = 1.0 - (1.0 - per_surface_loss)**n_surfaces
    return float(loss)

def pupil_wobble_metric(wobble1_rad, wobble2_rad):
    total_rad = abs(wobble1_rad) + abs(wobble2_rad)
    return float(np.rad2deg(total_rad) * 3600.0)

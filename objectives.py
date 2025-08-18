from .materials import dispersion_curve
from .raytrace import adc_residual_dispersion, pupil_wobble_estimate
from .metrics import chromatic_rms, throughput_loss, pupil_wobble_metric

def evaluate_design(glass1_row, glass2_row, params, wavelengths_nm, zenith_angle_deg, site):
    n1 = dispersion_curve(glass1_row, wavelengths_nm)
    n2 = dispersion_curve(glass2_row, wavelengths_nm)
    residual = adc_residual_dispersion(n1, n2,
                                       params['apex1_deg'], params['apex2_deg'],
                                       params['rel_rot_deg'],
                                       wavelengths_nm, zenith_angle_deg, site)
    chrom_rms = chromatic_rms(residual)
    wobble1 = pupil_wobble_estimate(params['apex1_deg'], params['thick1_mm'], n1)
    wobble2 = pupil_wobble_estimate(params['apex2_deg'], params['thick2_mm'], n2)
    wobble = pupil_wobble_metric(wobble1, wobble2)
    t_loss = throughput_loss(glass1_row, glass2_row, wavelengths_nm)
    return dict(chromatic_residual=chrom_rms,
                pupil_wobble=wobble,
                throughput_loss=t_loss)

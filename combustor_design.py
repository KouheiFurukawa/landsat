import pprint
from cycle_calculation import calc
import math

spec = calc(2.0, 1, 5.6, 1.8, 1900, 1200, 99.78)
R = 287
m3 = spec['m3']
Tt3 = spec['Tt3']
Pt3 = spec['Pt3']
rho_t3 = Pt3 / (R * Tt3)
m_fcb = spec['m_fcb']
If = 43.3 * (10 ** 6)


def combustor_design(SR, r, D):
    V = m_fcb * If / (SR * 1000 * Pt3)
    CLP = m3 / ((Pt3 / (1.013 * 10 ** 5)) ** 1.8 * (V / 0.305 ** 3))
    H = (V / (D * math.pi * r)) ** 0.5
    L = H * r
    A = V / L
    Aref = 2 * A
    Vref = m3 / (rho_t3 * Aref)
    b = 382 * (2 ** 0.5 + math.log(0.4 / 1.03))
    theta = (Pt3 / 6895) ** 1.75 * (Aref / 0.0254 ** 2) * (H * 1.4 / 0.0254) * math.exp(Tt3 * 1.8 / b) * 10 ** (-5) / (m3 / 0.45)

    return {
        'V': V,
        'SR': SR,
        'CLP': CLP,
        'Vref': Vref,
        'theta': theta,
        'H': H,
        'L': L,
        'b': b,
        'A': A,
        'm_fcb': m_fcb,
        'm3': m3,
    }


pprint.pprint(combustor_design(0.5, 2, 0.6))

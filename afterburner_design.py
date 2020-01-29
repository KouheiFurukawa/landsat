import pprint
from cycle_calculation import calc
import math

spec = calc(2.0, 1, 5.6, 1.8, 1900, 1200, 99.78)
gamma_t = 1.33
R = 287
If = 43.3 * (10 ** 6)
A6A = spec['A6A']
M6A = spec['M6A']
Tt6A = spec['Tt6A']
T6A = Tt6A / (1 + M6A ** 2 * (gamma_t - 1) / 2)
Pt6A = spec['Pt6A']
V6A = M6A * (gamma_t * R * T6A) ** 0.5

M7 = 0.3
Tt7 = spec['Tt7']
Pt7 = spec['Pt7']
m_fab = spec['m_fab']
T7 = Tt7 / (1 + M7 ** 2 * (gamma_t - 1) / 2)
P7 = Pt7 / (1 + M7 ** 2 * (gamma_t - 1) / 2)
V7 = M7 * (gamma_t * R * T7) ** 0.5
A7 = A6A * V6A / V7

D7 = 2 * (A7 / math.pi) ** 0.5


def afterburner_design():
    CLP = 0.8
    V = If * m_fab / (Pt7 * CLP) / 1000
    L = V / A7
    return {
        'A6A': A6A,
        'M6A': M6A,
        'Tt6A': Tt6A,
        'Pt6A': Pt6A,
        'V6A': V6A,
        'M7': M7,
        'Tt7': Tt7,
        'Pt7': Pt7,
        'D7': D7,
        'V': V,
        'L': L,
        'm_fab': m_fab,
        'V7': V7,
        'A7': A7,
    }


pprint.pprint(afterburner_design())

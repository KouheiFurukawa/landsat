import pprint
from cycle_calculation import calc
import math
from hpc_design import hpc_design, fan_design

gamma_t = 1.33
gc = 9.8
R = 287
Cpt = 1150
spec = calc(2.0, 1, 5.6, 1.8, 1900, 1200, 99.78)

T_ = 288.15
P_ = 1.013 * 10 ** 5


def MFP(m):
    return (m * (gamma_t * gc / R) ** 0.5) / (1 + ((gamma_t - 1) / 2) * m ** 2) ** ((gamma_t + 1) / (2 * (gamma_t - 1)))


m4 = spec['m4']
m45_ = spec['m4']
Pt4 = spec['Pt4']
Tt4 = spec['Tt4']
Tt45_ = spec['Tt45_']
eta_tHP = 0.93
Pt45_ = Pt4 * ((Tt45_ / Tt4 - 1) / eta_tHP + 1) ** (gamma_t / (gamma_t - 1))

m45 = spec['m45']
m5_ = spec['m45']
Pt45 = spec['Pt5']
Tt45 = spec['Tt45']
Tt5_ = spec['Tt5_']
eta_tLP = 0.93
Pt5_ = Pt45 * ((Tt5_ / Tt45 - 1) / eta_tLP + 1) ** (gamma_t / (gamma_t - 1))

Utip = 480
Utip_l = 300

alpha_1_hpt = 0
alpha_2_hpt = -5
alpha_1_lpt = -5
alpha_2_lpt = 0
# Mi = 0.15
# Mo = 0.45
# NG = 14824.599941346492


def turbine_design(stages, m, Tt_in, Tt_out, Pt_in, Pt_out, utip, alpha_1, alpha_2, M_in, M_out, ng, passage_type):
    T_in = Tt_in / (1 + ((gamma_t - 1) / 2) * M_in ** 2)
    u_in = M_in * (gamma_t * R * T_in) ** 0.5
    T_out = Tt_out / (1 + ((gamma_t - 1) / 2) * M_out ** 2)
    u_out = M_out * (gamma_t * R * T_in) ** 0.5
    V_in = M_in * (gamma_t * R * T_in) ** 0.5

    m_in_ = m * (P_ / Pt_in) * (Tt_in / T_) ** 0.5
    AI = m * Tt_in ** 0.5 / (Pt_in * MFP(M_in) * math.cos(math.radians(alpha_1)))
    DHI_max = utip / (math.pi * ng / 60)
    DHI_min = 2 * (0.25 * DHI_max ** 2 - AI / math.pi) ** 0.5
    DMI = (DHI_min + DHI_max) / 2
    UMI = utip * (DMI / DHI_max)
    U_in = utip

    AO = m * Tt_out ** 0.5 / (Pt_out * MFP(M_out) * math.cos(math.radians(alpha_2)))

    if passage_type == 'I':
        DHO_min = DHI_min
        DHO_max = 2 * ((AO + 0.25 * math.pi * DHO_min ** 2) / math.pi) ** 0.5
        DMO = (DHO_min + DHO_max) / 2
    elif passage_type == 'E':
        DHO_max = DHI_max
        DHO_min = 2 * ((0.25 * math.pi * DHO_max ** 2 - AO) / math.pi) ** 0.5
        DMO = (DHO_min + DHO_max) / 2
    else:
        DMO = DMI
        h = AO / (math.pi * DMO)
        DHO_max = DMO + h
        DHO_min = DMO - h

    UMO = utip * (DMO / DHO_max)
    U_out = utip * (DHO_max / DHI_max)

    Tstg = (Tt_in - Tt_out) / stages
    dv = Tstg * Cpt / utip
    phi = psi = Cpt * Tstg / ((UMO + UMI) / 2) ** 2

    return {
        'm': m,
        'Tt_in': Tt_in,
        'Tt_out': Tt_out,
        'T_in': T_in,
        'T_out': T_out,
        'Pt_in': Pt_in,
        'Pt_out': Pt_out,
        'Ns': stages,
        'Utip': utip,
        'alpha_1': alpha_1,
        'alpha_2': alpha_2,
        'Mi': M_in,
        'Mo': M_out,
        'NG': ng,
        'AI': AI,
        'AO': AO,
        'DHI_min': DHI_min,
        'DHI_max': DHI_max,
        'DMI': DMI,
        'DHO_max': DHO_max,
        'DHO_min': DHO_min,
        'DMO': DMO,
        'phi': phi,
        'Tstg': Tstg,
        'm_in_': m_in_,
        'V_in': V_in,
        'dv': dv,
        'U_in': U_in,
        'U_out': U_out,
        'u_in': u_in,
        'u_out': u_out,
    }


hpt_design = turbine_design(1, m4, Tt4, Tt45_, Pt4, Pt45_, Utip, alpha_1_hpt, alpha_2_hpt, 0.15, 0.3, hpc_design['NG'], 'I')
lpt_design = turbine_design(3, m45, Tt45, Tt5_, Pt45, Pt5_, Utip_l, alpha_1_lpt, alpha_2_lpt, 0.40, 0.45, fan_design['NG'], 'I')

r_hpt = [hpt_design['DHI_min'] + (hpt_design['DHO_max'] - hpt_design['DHI_max']) * (
        (2 * i) / (hpc_design['Ns'] * 2)) ** 2 for i in range(hpt_design['Ns'])]
r_lpt = [lpt_design['DHI_max'] + (lpt_design['DHO_max'] - lpt_design['DHI_max']) * (
        (2 * i) / (lpt_design['Ns'] * 2)) ** 2 for i in range(lpt_design['Ns'])]


if __name__ == "__main__":
    pprint.pprint(turbine_design(1, m4, Tt4, Tt45_, Pt4, Pt45_, Utip, alpha_1_hpt, alpha_2_hpt, 0.15, 0.3, hpc_design['NG'], 'I'))
    pprint.pprint(turbine_design(3, m45, Tt45, Tt5_, Pt45, Pt5_, Utip_l, alpha_1_lpt, alpha_2_lpt, 0.4, 0.45, fan_design['NG'], 'I'))
    print(r_lpt)


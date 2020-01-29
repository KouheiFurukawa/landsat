import pprint
import math
from cycle_calculation import calc

spec = calc(2.0, 1, 5.6, 1.8, 1900, 1200, 99.78)
gamma = 1.4
Rc = 287
Cpc = 1000

T_ = 288.15
P_ = 1.013 * 10 ** 5

m25 = spec['m25']
Pt25 = spec['Pt25']
Tt25 = spec['Tt25']
Tt3 = spec['Tt3']
Pt3 = spec['Pt3']

m2 = spec['m2']
Pt2 = spec['Pt2']
Tt2 = spec['Tt2']

# 設計パラメータ
Ns_fan = 3
Ns_hpc = 6


def compressor_design(stages, BRI, MO, m, Pt_in, Pt_out, Tt_in, Tt_out, passage_type, QA):
    UTI = 450

    m_in_ = m * (P_ / Pt_in) * (Tt_in / T_) ** 0.5

    # def calc_qa(M):
    #     P_in = Pt_in / (1 + M ** 2 * ((gamma - 1) / 2)) ** (gamma / (gamma - 1))
    #     T_in = Tt_in / (1 + ((gamma - 1) / 2) * M ** 2)
    #
    #     return M * P_in * (gamma / (Rc * T_in)) ** 0.5
    #
    # M_cand = [i * 0.01 for i in range(0, 100)]
    # QA_cand = [calc_qa(m) for m in M_cand]
    # print(QA_cand)
    # MI = 0
    # T_in = 0
    #
    # for i in range(len(QA_cand)):
    #     if QA_cand[i] > QA:
    #         QA = QA_cand[i]
    #         MI = i * 0.01
    #         P_in = Pt_in / (1 + MI ** 2 * ((gamma - 1) / 2)) ** (gamma / (gamma - 1))
    #         T_in = Tt_in / (1 + ((gamma - 1) / 2) * MI ** 2)
    #         break
    #
    # u_in = MI * (gamma * Rc * T_in) ** 0.5

    if QA == 131:
        u_in = 280.09
        MI = 0.7
    else:
        u_in = 225.45
        MI = 0.5

    DTI = m / QA
    DHI_max = 2 * (DTI / (1 - BRI ** 2) / math.pi) ** 0.5
    DHI_min = BRI * DHI_max
    DMI = (DHI_max + DHI_min) / 2
    UMI = UTI * (DMI / DHI_max)

    T_out = Tt_out / (1 + ((gamma - 1) / 2) * MO ** 2)
    DTO = m * (Rc * Tt_out / Pt_out) / (MO * (gamma * Rc * T_out) ** 0.5)

    if passage_type == 'I':
        DHO_min = DHI_min
        DHO_max = 2 * ((DTO + 0.25 * math.pi * DHO_min ** 2) / math.pi) ** 0.5
        DMO = (DHO_min + DHO_max) / 2
    elif passage_type == 'E':
        DHO_max = DHI_max
        DHO_min = 2 * ((0.25 * math.pi * DHO_max ** 2 - DTO) / math.pi) ** 0.5
        DMO = (DHO_min + DHO_max) / 2
    else:
        DMO = DMI
        h = DTO / (math.pi * DMO)
        DHO_max = DMO + h
        DHO_min = DMO - h

    UMO = UTI * (DMO / DHI_max)
    UTO = UTI * (DHO_max / DHI_max)
    NG = UTI / (DHI_max * math.pi) * 60
    NG_ = NG * (T_ / Tt_in) ** 0.5

    Um = (UMO + UMI) / 2
    Tstg = (Tt_out - Tt_in) / stages
    psi = Cpc * Tstg / Um ** 2
    di = Cpc * Tstg

    u_out = MO * (gamma * Rc * T_out) ** 0.5
    dv = di / UTI

    return {
        'm': m,
        'Pt_in': Pt_in,
        'Tt_in': Tt_in,
        'm_in_': m_in_,
        'QA': QA,
        'BRI': BRI,
        'UTI': UTI,
        'DTI': DTI,
        'DHI_max': DHI_max,
        'DHI_min': DHI_min,
        'DMI': DMI,
        'UMI': UMI,
        'MO': MO,
        'T_out': T_out,
        'DTO': DTO,
        'DHO_min': DHO_min,
        'DHO_max': DHO_max,
        'DMO': DMO,
        'NG': NG,
        'NG_': NG_,
        'Um': Um,
        'Ns': stages,
        'Tstg': Tstg,
        'psi': psi,
        'u_out': u_out,
        'u_in': u_in,
        'dv': dv,
        'UTO': UTO,
        'MI': MI,
    }


hpc_design = compressor_design(7, 0.7, 0.3, m25, Pt25, Pt3, Tt25, Tt3, 'E', 190)
fan_design = compressor_design(2, 0.5, 0.5, m2, Pt2, Pt25, Tt2, Tt25, 'E', 131)
r_hpc = [hpc_design['DHI_min'] + (hpc_design['DHO_min'] - hpc_design['DHI_min']) * (
            (1 + 2 * i) / (hpc_design['Ns'] * 2 + 1)) ** 2 for i in range(hpc_design['Ns'])]
r_fan = [fan_design['DHI_min'] + (fan_design['DHO_min'] - fan_design['DHI_min']) * (
        (2 * i) / (fan_design['Ns'] * 2)) ** 2 for i in range(fan_design['Ns'])]
if __name__ == "__main__":
    pprint.pprint(compressor_design(3, 0.5, 0.5, m2, Pt2, Pt25, Tt2, Tt25, 'E', 131))
    pprint.pprint(compressor_design(7, 0.7, 0.3, m25, Pt25, Pt3, Tt25, Tt3, 'E', 190))

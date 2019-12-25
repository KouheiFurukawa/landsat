import math
import pprint

# trent1000
T0 = 216.6888
M0 = 1.4
P0 = 1.165237 * (10 ** 4)
rho = 1.225
D = 2.85
a = 295.0401

# 物理定数
gamma = 1.4
gamma_t = 1.33
Rt = 287  # [J/kg * K]
Rc = 287
gc = 9.8
V0 = M0 * a
Cpc = 1000  # [J/kg*K]
Cpt = 1150  # [J/kg*K]

m0 = 150  # [kg/s]

alpha = 0.2
beta_HP = 0.15
beta_LP = 0.05

omega1 = 0.06
omega_cb = 0.05
omega_ab_off = 0
omega_ab_on = 0.06
omega_n_core = 0.02
omega_n_bp = 0.02
omega_bp = 0.05


def calc(pr_fan, pr_cLP, pr_cHP, mu, Tt4, Tt7, amf):
    # 断熱効率
    eta_cLP = 0.9
    eta_cHP = 1
    eta_tHP = 0.9
    eta_tLP = 0.92
    eta_mLP = 0.99
    eta_mHP = 0.99
    eta_cb = 0.99
    eta_fan = (pr_fan ** ((gamma - 1) / gamma) - 1) / (pr_fan ** ((gamma - 1) / (0.9 * gamma)) - 1)

    # ①入口大気
    Pt0 = P0 * (1 + (M0 ** 2) * (gamma - 1) / 2) ** (gamma / (gamma - 1))
    Tt0 = T0 * (1 + (M0 ** 2) * (gamma - 1) / 2)

    # ②インテーク出口
    Pt2 = Pt0 * (1 - omega1)
    Tt2 = Tt0
    m2 = m0
    I2 = Cpc * Tt2

    # ファン出口(バイパス部)
    Pt13 = pr_fan * Pt2
    Tt13 = Tt2 * (1 + ((pr_fan ** ((gamma - 1) / gamma) - 1) / eta_fan))
    I13 = I2 + Cpc * (Tt13 - Tt2)
    m13 = mbp = m2 * (mu / (1 + mu))

    # ファンノズル(バイパス部)
    Pt19 = Pt13 * (1 - omega_bp)
    Tt19 = Tt13

    # ファン出口(コア部)
    Pt21 = pr_fan * Pt2
    Tt21 = Tt2 * (1 + (pr_fan ** ((gamma - 1) / gamma) - 1) / eta_fan)
    I21 = I2 + Cpc * (Tt21 - Tt2)
    m21 = m_core = m2 / (1 + mu)

    # 低圧圧縮機LPC出口(＝高圧圧縮機入口)
    Pt25 = Pt21 * pr_cLP
    Tt25 = Tt21 * (1 + (pr_cLP ** ((gamma - 1) / gamma) - 1) / eta_cLP)
    I25 = Cpc * Tt25
    m25 = m21

    # ④高圧圧縮機HPC出口
    Pt3 = pr_cHP * Pt25
    Tt3 = Tt25 * pr_cHP ** ((gamma - 1) / (0.9 * gamma))
    I3 = I25 + Cpc * (Tt3 - Tt25)
    m3 = m25

    # ⑤燃焼器出口(冷却空気合流前)
    If = 43.3 * (10 ** 6)  # [J/kg], Jet-A
    Pt4 = Pt3 * (1 - omega_cb)
    I4 = I3 + Cpt * (Tt4 - Tt3)
    m_fcb = (m3 - alpha * m3) * (I4 - I3) / (If * eta_cb - I4)
    m4 = m3 - alpha * m3 + m_fcb

    # ⑥高圧タービンHPT出口(冷却空気混合後)
    I45_ = I4 - m3 * (I3 - I25) / (eta_mHP * m4)
    Tt45_ = Tt4 - (I4 - I45_) / Cpt
    Pt45 = Pt4 * ((Tt45_ / Tt4 - 1) / eta_tHP + 1) ** (gamma_t / (gamma_t - 1))
    I45 = (m4 * I45_ + m3 * beta_HP * I3) / (m4 + m3 * beta_HP)
    Tt45 = Tt4 - (I4 - I45) / Cpt
    m45 = m4 + m3 * beta_HP

    # ⑦低圧タービンLPT出口(冷却空気混合後)
    I5_ = I45 - (m2 * (I13 - I2) * mu / (1 + mu) + m2 * (I25 - I2) / (1 + mu)) / (eta_mLP * m45)
    Tt5_ = Tt45 - (I45 - I5_) / Cpt
    Pt5 = Pt45 * ((Tt5_ / Tt45 - 1) / eta_tLP + 1) ** (gamma_t / (gamma_t - 1))
    I5 = (m45 * I5_ + m3 * beta_LP * I3) / (m45 + m3 * beta_LP)
    Tt5 = Tt45 - (I45 - I5) / Cpt
    m5 = m45 + m3 * beta_LP

    # ミキサー
    m6 = m5
    m16 = m13
    m6A = m6 + m16
    I6 = I5
    I16 = I13
    Cp6A = (m16 * Cpc + m6 * Cpt) / m6A
    gamma_6A = (m16 * gamma + m6 * gamma_t) / m6A
    R6A = (m16 * Rc + m6 * Rt) / m6A
    Tt6A = (m16 * I16 + m6 * I6) / (Cp6A * m6A)
    I6A = Cp6A * Tt6A
    Pt16 = Pt13 * (1 - omega_bp)
    Pt6 = Pt5
    M6 = 0.9
    M16 = ((2 / (gamma - 1)) * (
            ((Pt16 / Pt6) * (1 + M6 ** 2 * (gamma_t - 1) / 2) ** (gamma_t / (gamma_t - 1))) ** (
            (gamma - 1) / gamma) - 1)) ** 0.5

    P6 = Pt6 / (1 + M6 ** 2 * (gamma_t - 1) / 2) ** (gamma_t / (gamma_t - 1))
    P16 = Pt16 / (1 + M16 ** 2 * (gamma - 1) / 2) ** (gamma / (gamma - 1))

    Tt16 = Tt13
    Tt6 = Tt5
    T6 = Tt6 / (1 + M6 ** 2 * ((gamma_t - 1) / 2))
    T16 = Tt16 / (1 + M16 ** 2 * ((gamma - 1) / 2))
    A16 = m16 * (Rc * T16 / gamma) ** 0.5 / (P16 * M16)
    A6 = m6 * (Rt * T6 / gamma_t) ** 0.5 / (P6 * M6)
    A6A = A16 + A6
    Z2 = P6 * A6 * (1 + gamma_t * M6 ** 2) + P16 * A16 * (1 + gamma * M16 ** 2)
    Z1 = (Z2 ** 2 * gc * gamma_6A) / (m6A ** 2 * R6A * Tt6A)
    M6A2 = (2 * gamma_6A - Z1 + (Z1 ** 2 - 2 * gamma_6A * Z1 - 2 * Z1) ** 0.5) / (
            gamma_6A * Z1 - Z1 - 2 * gamma_6A ** 2)
    M6A2_ = (2 * gamma_6A - Z1 - (Z1 ** 2 - 2 * gamma_6A * Z1 - 2 * Z1) ** 0.5) / (
            gamma_6A * Z1 - Z1 - 2 * gamma_6A ** 2)
    if M6A2 > 0:
        M6A = M6A2 ** 0.5
    else:
        M6A = M6A2_ ** 0.5
    P6A = Z2 / (A6A * (1 + gamma_6A * M6A ** 2))
    Pt6A = P6A * (1 + M6A ** 2 * (gamma_6A - 1) / 2) ** (gamma_6A / (gamma_6A - 1))

    # ⑧アフターバーナ(ドライ時＝非燃焼)
    Pt7 = Pt6A
    Tt7 = Tt6A
    I7 = I6A
    m7 = m6A
    m_fab = 0

    Pt9 = Pt7 * (1 - omega_n_core)
    Tt9 = Tt7
    m9 = m7
    pr_cri = ((gamma_6A + 1) / 2) ** (gamma_6A / (gamma_6A - 1))

    P9_choke = Pt9 / pr_cri

    P9 = (P0 + P9_choke) / 2
    M9 = ((2 / (gamma_t - 1)) * ((Pt9 / P9) ** ((gamma_t - 1) / gamma_t) - 1)) ** 0.5

    T9 = Tt9 / ((gamma_t + 1) / 2)
    V9 = M9 * (gamma_t * Rt * T9) ** 0.5
    rho9 = P9 / (Rt * T9)
    A9 = m9 / (rho9 * V9)

    # 推力
    FN = (m9 * V9 - m0 * V0) + A9 * (P9 - P0)

    # SFC
    sfc = (m_fcb + m_fab) / FN

    return {
        'core': m9 * V9,
        'm0': amf,
        'm13': m13,
        'm19': mbp,
        'm2': m2,
        'm21': m21,
        'm25': m25,
        'm3': m3,
        'm4': m4,
        'm45': m45,
        'm5': m5,
        'm7': m7,
        'm6A': m6A,
        'm9': m9,
        'pr_fan': pr_fan,
        'pr_cHP': pr_cHP,
        'pr_cLP': pr_cLP,
        'bpr': mu,
        'P0': P0,
        'P6': P6,
        'Pt0': Pt0,
        'Pt2': Pt2,
        'Pt13': Pt13,
        'Pt16': Pt16,
        'Pt21': Pt21,
        'Pt25': Pt25,
        'Pt3': Pt3,
        'Pt4': Pt4,
        'Pt45': Pt45,
        'Pt5': Pt5,
        'Pt6': Pt6,
        'Pt6A': Pt6A,
        'Pt7': Pt7,
        'Pt9': Pt9,
        'P9': P9,
        'P16': P16,
        'Pt19': Pt19,
        'I2': I2,
        'I13': I13,
        'I21': I21,
        'I25': I25,
        'I3': I3,
        'I4': I4,
        'I45': I45,
        'I45_': I45_,
        'I5': I5,
        'I5_': I5_,
        'I6A': I6A,
        'I7': I7,
        'T0': T0,
        'T6': T6,
        'T16': T16,
        'Tt0': Tt0,
        'Tt2': Tt2,
        'Tt13': Tt13,
        'Tt21': Tt21,
        'Tt25': Tt25,
        'Tt3': Tt3,
        'Tt4': Tt4,
        'Tt45': Tt45,
        'Tt45_': Tt45_,
        'Tt5': Tt5,
        'Tt5_': Tt5_,
        'Tt6A': Tt6A,
        'Tt7': Tt7,
        'Tt9': Tt9,
        'T9': T9,
        'Tt19': Tt19,
        'F': FN,
        'sfc': sfc * 3600 * 9.8,
        'eta_tHP': eta_tHP,
        'eta_tLP': eta_tLP,
        'm_fab': m_fab,
        'm_fcb': m_fcb,
        'M9': M9,
        'M16': M16,
        'M6A': M6A,
        'M6': M6,
        'Z1': Z1,
        'Z2': Z2,
        'OPR': Pt3 / Pt0,
        'Isp': FN / (amf * 9.8),
        'M6A2': M6A2,
        'M6A2_': M6A2_,
        'A6': A6,
        'A16': A16,
        'A6A': A6A,
        'A9': A9,
        'pr_cri': pr_cri,
    }


pprint.pprint(calc(2.8, 1, 12, 1.6, 2000, 2000, 150))


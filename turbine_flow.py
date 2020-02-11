import math
import pprint
from turbine_design import hpt_design, lpt_design, r_hpt, r_lpt

Cp = 1150
gamma_t = 1.33


def velocity_triangle_turbine(alpha1, alpha2, alpha3, u, U, Tt_out):
    V1 = u / math.cos(math.radians(alpha1))
    V2 = u / math.cos(math.radians(alpha2))
    v1 = V1 * math.sin(math.radians(alpha1))
    v2 = V2 * math.sin(math.radians(alpha2))

    v2R = v2 + U
    beta2 = math.degrees(math.atan(v2R / u))
    V2R = u / math.cos(math.radians(beta2))

    V3 = u / math.cos(math.radians(alpha3))
    v3 = V3 * math.sin(math.radians(alpha3))
    v3R = v3 + U
    beta3 = math.degrees(math.atan(v3R / u))
    V3R = u / math.cos(math.radians(beta3))
    sigma = 2

    G_rotor = 0.5 * (beta3 + beta2)
    G_stator = 0.5 * (alpha1 + alpha2)

    Z_stator = 2 / (sigma * math.cos(math.radians(G_stator))) * math.cos(math.radians(alpha2)) ** 2 * (
            math.tan(math.radians(alpha1)) + math.tan(math.radians(alpha2)))
    Z_rotor = 2 / (sigma * math.cos(math.radians(G_rotor))) * math.cos(math.radians(beta3)) ** 2 * (
            math.tan(math.radians(beta2)) + math.tan(math.radians(beta3)))

    theta12 = alpha1 - alpha2
    theta23 = alpha3 - alpha2

    T_out = Tt_out - V3R ** 2 / (2 * Cp)
    MoR = ((Tt_out / T_out - 1) * 2 / (gamma_t - 1)) ** 0.5
    AR_SV = 4
    AR_RB = 4
    Csv = 0.102 / AR_SV
    Crb = 0.116 / AR_RB
    Cx_stator = Csv * math.cos(math.radians(G_stator))
    Cx_rotor = Crb * math.cos(math.radians(G_rotor))

    return {
        'V1': V1,
        'V2': V2,
        'v2': v2,
        'v2R': v2R,
        'beta2': beta2,
        'V2R': V2R,
        'V3': V3,
        'v3': v3,
        'v3R': v3R,
        'beta3': beta3,
        'V3R': V3R,
        'G_rotor': G_rotor,
        'G_stator': G_stator,
        'Z_stator': Z_stator,
        'Z_rotor': Z_rotor,
        'MoR': MoR,
        'Cx_rotor': Cx_rotor,
        'Cx_stator': Cx_stator,
        'theta12': theta12,
        'theta23': theta23,
        'u': u,
        'v1': v1,
    }


if __name__ == "__main__":
    # HPT
    pprint.pprint(velocity_triangle_turbine(0, -82, -5, 85.09, 480, 1532.7))
    pprint.pprint(velocity_triangle_turbine(0, -82, -5, 85.09, 462.25, 1532.7))
    pprint.pprint(velocity_triangle_turbine(0, -82, -5, 85.09, 444.49, 1532.7))

    # LPT
    pprint.pprint(velocity_triangle_turbine(-5, -17, 39, 298.87, 300, 1412.95))
    pprint.pprint(velocity_triangle_turbine(39, -22, 35, 311.33, 303.96, 1324.70))
    pprint.pprint(velocity_triangle_turbine(35, -46, 0, 323.78, 317.41, 1236.45))

    pprint.pprint(velocity_triangle_turbine(-5, -17, 39, 298.87, 275.67, 1412.95))
    pprint.pprint(velocity_triangle_turbine(39, -22, 35, 311.33, 277.65, 1324.70))
    pprint.pprint(velocity_triangle_turbine(35, -46, 0, 323.78, 284.37, 1236.45))

    pprint.pprint(velocity_triangle_turbine(-5, -17, 39, 298.87, 251.33, 1412.95))
    pprint.pprint(velocity_triangle_turbine(39, -22, 35, 311.33, 251.33, 1324.70))
    pprint.pprint(velocity_triangle_turbine(35, -46, 0, 323.78, 251.33, 1236.45))

    # U_in = hpt_design['U_in']
    # U_out = hpt_design['U_out']
    # Tt_in = hpt_design['Tt_in']
    # Tstg = hpt_design['Tstg']
    # V_in = hpt_design['V_in']

    U_in = lpt_design['U_in']
    U_out = lpt_design['U_out']
    Tt_in = lpt_design['Tt_in']
    Tstg = lpt_design['Tstg']
    u_in = lpt_design['u_in']
    u_out = lpt_design['u_out']
    Ns = lpt_design['Ns']
    DHI_max = lpt_design['DHI_max']
    DHI_min = lpt_design['DHI_min']

    # for l in range(Ns):
    #     for i in range(-5, -4):
    #         for j in range(-90, 90):
    #             for k in range(39, 40):
    #                 flow = velocity_triangle_turbine(i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U_in * r_lpt[l] / DHI_max, Tt_in - (l + 1) * Tstg)
    #                 dv = lpt_design['dv']
    #                 if type(flow['MoR']) is complex:
    #                     continue
    #                 if flow['Z_rotor'] <= 1 and flow['Z_stator'] <= 1 and flow['MoR'] <= 0.9 and flow['theta12'] <= 120 and \
    #                         flow['theta23'] <= 120 and 0.98 < (flow['v3'] - flow['v2']) / dv < 1.02:
    #                     print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U_in * r_lpt[l] / DHI_max, Tt_in - (l + 1) * Tstg)

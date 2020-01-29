import math
import pprint
from hpc_design import hpc_design, fan_design, r_hpc, r_fan

gamma = 1.4
Rc = 287
Cpc = 1000

T_ = 288.15
P_ = 1.013 * 10 ** 5


def velocity_triangle(alpha1, alpha2, alpha3, u, U):
    V1 = u / math.cos(math.radians(alpha1))
    v1 = V1 * math.sin(math.radians(alpha1))
    v1R = v1 - U
    beta1 = math.degrees(math.atan(v1R / u))
    V1R = u / math.cos(math.radians(beta1))

    V2 = u / math.cos(math.radians(alpha2))
    v2 = V2 * math.sin(math.radians(alpha2))
    v2R = v2 - U
    beta2 = math.degrees(math.atan(v2R / u))
    V2R = u / math.cos(math.radians(beta2))

    V3 = u / math.cos(math.radians(alpha3))
    v3 = V3 * math.sin(math.radians(alpha3))
    v3R = v3 - U
    beta3 = math.degrees(math.atan(v3R / u))
    V3R = u / math.cos(math.radians(beta3))

    sigma = 2
    DF_rotor = 1 - V2R / V1R + abs(v1R - v2R) / (2 * V1R * sigma)
    DF_stator = 1 - V3 / V2 + abs(v2 - v3) / (2 * sigma * V2)
    R = abs((v1R + v2R) / (2 * U))
    G_rotor = 0.5 * (beta1 + beta2)
    G_stator = 0.5 * (alpha2 + alpha3)
    Cp_rotor = 1 - (V2R / V1R) ** 2
    Cp_stator = 1 - (V3 / V2) ** 2

    h_ave = 236
    AR_SV = 1
    AR_RB = 0.5
    Csv = 222 / AR_SV
    Crb = 215 / AR_RB
    Cx_stator = Csv * math.cos(math.radians(G_stator))
    Cx_rotor = Crb * math.cos(math.radians(G_rotor))

    return {
        'V1': V1,
        'v1': v1,
        'v1R': v1R,
        'beta1': beta1,
        'V1R': V1R,
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
        'DF_rotor': DF_rotor,
        'DF_stator': DF_stator,
        'R': R,
        'G_rotor': G_rotor,
        'G_stator': G_stator,
        'Cp_rotor': Cp_rotor,
        'Cp_stator': Cp_stator,
        'Cx_stator': Cx_stator,
        'Cx_rotor': Cx_rotor,
        'alpha1': alpha1,
        'alpha2': alpha2,
        'alpha3': alpha3,
        'AR_SV': AR_SV,
        'AR_RB': AR_RB,
        'Csv': Csv,
        'Crb': Crb,
        'u': u,
    }


if __name__ == "__main__":
    # pprint.pprint(velocity_triangle(0, 0, 14, 180.59, 450))
    # pprint.pprint(velocity_triangle(14, 43, 14, 180.59, 450))
    # pprint.pprint(velocity_triangle(14, 43, 13, 180.59, 450))
    # pprint.pprint(velocity_triangle(13, 42, 0, 180.59, 450))
    #
    # pprint.pprint(velocity_triangle(0, 0, 24, 225.45, 450))
    # pprint.pprint(velocity_triangle(24, 44, 19, 225.5, 450))
    # pprint.pprint(velocity_triangle(19, 41, 0, 225.5, 450))

    Ns = fan_design['Ns']
    u_in = fan_design['u_in']
    u_out = fan_design['u_out']
    U = fan_design['UTI']
    DHI_max = fan_design['DHI_max']

    for l in range(Ns):
        for i in range(0, 90):
            for j in range(-90, 90):
                for k in range(0, 90):
                    # flow = velocity_triangle(i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U * r_hpc[l] / DHI_max)
                    flow = velocity_triangle(i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U)
                    design = fan_design
                    if flow['DF_rotor'] <= 0.55 and flow['DF_stator'] <= 0.55 and 0.5 <= flow[
                        'R'] <= 0.8 and flow['Cp_rotor'] <= 0.45 and 0.35 < flow[
                        'Cp_stator'] <= 0.45:
                        # print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U * r_hpc[l] / DHI_max)
                        if l == 0 and 1.02 > (flow['v2'] - flow['v1']) / (design['dv'] * 1.05) > 0.98:
                            print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns)
                        elif l == 1 and 1.02 > (flow['v2'] - flow['v1']) / (design['dv'] * 0.95) > 0.98:
                            print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns)
                        elif l > 2 and 1.02 > (flow['v2'] - flow['v1']) / (design['dv']) > 0.98:
                            print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns)

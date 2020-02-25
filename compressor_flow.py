import math
import pprint
from hpc_design import hpc_design, fan_design, r_hpc, r_fan

gamma = 1.4
Rc = 287
Cpc = 1000

T_ = 288.15
P_ = 1.013 * 10 ** 5


def velocity_triangle(alpha1, alpha2, alpha3, u, uout, U):
    V1 = u / math.cos(math.radians(alpha1))
    v1 = V1 * math.sin(math.radians(alpha1))
    v1R = v1 - U
    beta1 = math.degrees(math.atan(v1R / u))
    V1R = u / math.cos(math.radians(beta1))

    u2 = (u + uout) / 2
    V2 = u2 / math.cos(math.radians(alpha2))
    v2 = V2 * math.sin(math.radians(alpha2))
    v2R = v2 - U
    beta2 = math.degrees(math.atan(v2R / u2))
    V2R = u2 / math.cos(math.radians(beta2))

    u3 = uout
    V3 = u3 / math.cos(math.radians(alpha3))
    v3 = V3 * math.sin(math.radians(alpha3))
    v3R = v3 - U
    beta3 = math.degrees(math.atan(v3R / u3))
    V3R = u3 / math.cos(math.radians(beta3))

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
        'u1': u,
        'u2': u2,
        'u3': u3,
        'U': U,
    }


if __name__ == "__main__":
    # HPC
    # print('tip')
    # pprint.pprint(
    #     velocity_triangle(0, 0, 21, (225.45 * (7 - 0) + 180.59 * 0) / 7, (225.45 * (7 - 0) + 180.59 * 0) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(21, 48, 22, (225.45 * (7 - 0) + 180.59 * 0) / 7, (225.45 * (7 - 1) + 180.59 * 1) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(22, 44, 21, (225.45 * (7 - 1) + 180.59 * 1) / 7, (225.45 * (7 - 2) + 180.59 * 2) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(21, 44, 15, (225.45 * (7 - 2) + 180.59 * 2) / 7, (225.45 * (7 - 3) + 180.59 * 3) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(15, 41, 16, (225.45 * (7 - 3) + 180.59 * 3) / 7, (225.45 * (7 - 4) + 180.59 * 4) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(16, 41, 17, (225.45 * (7 - 4) + 180.59 * 4) / 7, (225.45 * (7 - 5) + 180.59 * 5) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(17, 42, 14, (225.45 * (7 - 5) + 180.59 * 5) / 7, (225.45 * (7 - 6) + 180.59 * 6) / 7, 450))
    # pprint.pprint(
    #     velocity_triangle(14, 41, 0, (225.45 * (7 - 6) + 180.59 * 6) / 7, (225.45 * (7 - 7) + 180.59 * 7) / 7, 450))
    #
    # print('mid')
    # pprint.pprint(
    #     velocity_triangle(0, 0, 21, (225.45 * (7 - 0) + 180.59 * 0) / 7, (225.45 * (7 - 0) + 180.59 * 0) / 7, 382.57))
    # pprint.pprint(
    #     velocity_triangle(21, 48, 22, (225.45 * (7 - 0) + 180.59 * 0) / 7, (225.45 * (7 - 1) + 180.59 * 1) / 7, 382.90))
    # pprint.pprint(
    #     velocity_triangle(22, 44, 21, (225.45 * (7 - 1) + 180.59 * 1) / 7, (225.45 * (7 - 2) + 180.59 * 2) / 7, 384.54))
    # pprint.pprint(
    #     velocity_triangle(21, 44, 15, (225.45 * (7 - 2) + 180.59 * 2) / 7, (225.45 * (7 - 3) + 180.59 * 3) / 7, 387.83))
    # pprint.pprint(
    #     velocity_triangle(15, 41, 16, (225.45 * (7 - 3) + 180.59 * 3) / 7, (225.45 * (7 - 4) + 180.59 * 4) / 7, 392.77))
    # pprint.pprint(
    #     velocity_triangle(16, 41, 17, (225.45 * (7 - 4) + 180.59 * 4) / 7, (225.45 * (7 - 5) + 180.59 * 5) / 7, 399.67))
    # pprint.pprint(
    #     velocity_triangle(17, 42, 14, (225.45 * (7 - 5) + 180.59 * 5) / 7, (225.45 * (7 - 6) + 180.59 * 6) / 7, 407.90))
    # pprint.pprint(
    #     velocity_triangle(14, 41, 0, (225.45 * (7 - 6) + 180.59 * 6) / 7, (225.45 * (7 - 7) + 180.59 * 7) / 7, 418.09))
    #
    # print('hub')
    # pprint.pprint(
    #     velocity_triangle(0, 0, 21, (225.45 * (7 - 0) + 180.59 * 0) / 7, (225.45 * (7 - 0) + 180.59 * 0) / 7, 315.13))
    # pprint.pprint(
    #     velocity_triangle(21, 48, 22, (225.45 * (7 - 0) + 180.59 * 0) / 7, (225.45 * (7 - 1) + 180.59 * 1) / 7, 315.79))
    # pprint.pprint(
    #     velocity_triangle(22, 44, 21, (225.45 * (7 - 1) + 180.59 * 1) / 7, (225.45 * (7 - 2) + 180.59 * 2) / 7, 319.08))
    # pprint.pprint(
    #     velocity_triangle(21, 44, 15, (225.45 * (7 - 2) + 180.59 * 2) / 7, (225.45 * (7 - 3) + 180.59 * 3) / 7, 325.66))
    # pprint.pprint(
    #     velocity_triangle(15, 41, 16, (225.45 * (7 - 3) + 180.59 * 3) / 7, (225.45 * (7 - 4) + 180.59 * 4) / 7, 335.53))
    # pprint.pprint(
    #     velocity_triangle(16, 41, 17, (225.45 * (7 - 4) + 180.59 * 4) / 7, (225.45 * (7 - 5) + 180.59 * 5) / 7, 349.34))
    # pprint.pprint(
    #     velocity_triangle(17, 42, 14, (225.45 * (7 - 5) + 180.59 * 5) / 7, (225.45 * (7 - 6) + 180.59 * 6) / 7, 365.79))
    # pprint.pprint(
    #     velocity_triangle(14, 41, 0, (225.45 * (7 - 6) + 180.59 * 6) / 7, (225.45 * (7 - 7) + 180.59 * 7) / 7, 386.18))

    # ファン
    print('tip')
    pprint.pprint(velocity_triangle(0, 0, 26, 280.09, 280.09, 450))
    pprint.pprint(velocity_triangle(26, 45, 20, 280.09, 252.77, 450))
    pprint.pprint(velocity_triangle(20, 39, 0, 252.77, 225.45, 450))

    print('mid')
    pprint.pprint(velocity_triangle(0, 0, 26, 280.09, 280.09, 337.5))
    pprint.pprint(velocity_triangle(26, 45, 20, 280.09, 252.77, 356.68))
    pprint.pprint(velocity_triangle(20, 39, 0, 252.77, 225.45, 382.38))

    print('hub')
    pprint.pprint(velocity_triangle(0, 0, 26, 280.09, 280.09, 225))
    pprint.pprint(velocity_triangle(26, 45, 20, 280.09, 252.77, 263.36))
    pprint.pprint(velocity_triangle(20, 39, 0, 252.77, 225.45, 314.76))

    Ns = hpc_design['Ns']
    u_in = hpc_design['u_in']
    u_out = hpc_design['u_out']
    U = hpc_design['UTI']
    DHI_max = hpc_design['DHI_max']

    # for l in range(0, 3):
    #     for i in range(0, 90):
    #         for j in range(-90, 90):
    #             for k in range(-90, 90):
    #                 flow = velocity_triangle(i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U * r_hpc[l] / DHI_max)
    #                 # flow = velocity_triangle(i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U)
    #                 design = hpc_design
    #                 if flow['DF_rotor'] <= 0.55 and flow['DF_stator'] <= 0.55 and 0.5 <= flow[
    #                     'R'] <= 0.8 and 0.35 < flow['Cp_rotor'] <= 0.45 and 0.35 < flow[
    #                     'Cp_stator'] <= 0.45:
    #                     print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns, U * r_hpc[l] / DHI_max)
    # if 1.02 > (flow['v2'] - flow['v1']) / (design['dv']) > 0.98:
    #     print(l + 1, i, j, k, (u_in * (Ns - l) + u_out * l) / Ns)

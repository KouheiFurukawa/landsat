import matplotlib.pyplot as plt
from cycle_calculation import calc
import numpy as np
import pprint
import plotly.graph_objects as go
from plotly.graph_objects import Layout, Scatter
from plotly.offline import plot as py

pr_fan = 2.4
pr_cLP = 1
pr_cHP = 4.8
m0 = 100
bpr = 0.3
Tt7 = 1200
Tt4 = 1600
y = np.array([])
x = np.array([])
z = np.array([])

# sfc = np.array([])
# isp = np.array([])
# for m in [0.1 * x for x in range(15, 50)]:
#     for k in [x * 0.1 for x in range(11, 31)]:
#         for l in [1200, 1250, 1300, 1350, 1400, 1450, 1500, 1600]:
#             for i in [1500, 1600, 1700, 1800, 1900]:
#                 for j in [0.1 * x for x in range(50,101)]:
#                     cc = calc(k, pr_cLP, j, m, i, l, m0)
#                     if 'sfc' in cc and 'Isp' in cc:
#                         if cc['sfc'] > 0 and cc['Isp'] > 0:
#                             sfc = np.append(sfc, cc['sfc'])
#                             isp = np.append(isp, cc['Isp'])
#
# print(len(sfc), len(isp))
# plt.scatter(isp, sfc, s=5)

for m in [0.01 * x for x in range(150, 501)]:
    sfc = np.array([])
    isp = np.array([])
    v9 = np.array([])
    calculated = np.array([])
    a = np.array([])
    b = np.array([])

    for k in [x * 0.1 for x in range(11, 31)]:
        for l in [1200, 1250, 1300, 1350, 1400, 1450, 1500, 1600]:
            sfc_local = 10
            isp_local = 0
            v9_local = 0
            cc_local = {}

            for i in [1500, 1600, 1700, 1800, 1900]:
                for j in [0.1 * x for x in range(50,101)]:
                    cc = calc(k, pr_cLP, j, m, i, l, m0)
                    if 'sfc' in cc and 'Isp' in cc:
                        if type(cc['sfc']) is float and type(cc['Isp']) is float:
                            if 0 < cc['sfc'] < sfc_local and cc['m_fab'] > 0:
                                sfc_local = cc['sfc']
                                isp_local = cc['Isp']
                                v9_local = cc['V9']
                                cc_local = cc
            if isp_local > 0:
                sfc = np.append(sfc, sfc_local)
                isp = np.append(isp, isp_local)
                v9 = np.append(v9, v9_local)
                calculated = np.append(calculated, cc_local)
                a = np.append(a, k)
                b = np.append(b, l)

    sfc_global = 10
    isp_global = 0
    v9_global = 0
    cc_global = {}
    for n in range(len(sfc)):
        if sfc[n] < sfc_global:
            sfc_global = sfc[n]
            isp_global = isp[n]
            v9_global = v9[n]
            cc_global = calculated[n]
    if 80 < isp_global < 81:
        pprint.pprint(cc_global)
    y = np.append(y, v9_global)
    z = np.append(z, sfc_global)
    x = np.append(x, isp_global)

# plt.scatter(np.array([0.01 * x for x in range(0, 501)]), y, s=5)

plt.scatter(x, z, s=5)
plt.xlabel('Specific thrust')
plt.ylabel('SFC')
plt.show()

# print(sfc)
# print(isp)
# trace1 = go.Carpet(
#     a=a,
#     b=b,
#     x=isp,
#     y=sfc,
#     aaxis=dict(
#         gridcolor='black',
#         color='black',
#         tickprefix='fpr = ',
#         smoothing=1.3
#     ),
#     baxis=dict(
#         gridcolor='black',
#         color='black',
#         tickprefix='T_ab = ',
#         smoothing=1.3
#     )
# )
#
# data = [trace1]
#
# fig = go.Figure(data=data, layout=Layout(font=dict(family='Arial, sans-serif',
#                                                    size=18,
#                                                    color='rgb(0,0,0)'),
#                                          yaxis=dict(
#                                              title='SFC[lb/(lbf*s)]',
#                                              titlefont=dict(
#                                                  family='Arial, sans-serif',
#                                                  size=18
#                                              ),
#                                              showticklabels=True
#                                          ),
#                                          xaxis=dict(
#                                              title='Specific thrust[s]',
#                                              titlefont=dict(
#                                                  family='Arial, sans-serif',
#                                                  size=18
#                                              ),
#                                              showticklabels=True
#                                          ),
#                                          margin=go.Margin(
#                                              l=100,
#                                              r=50)
#                                          ))
# fig.show()

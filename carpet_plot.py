import matplotlib.pyplot as plt
from pylab import figure
from cycle_calculation import calc
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot as py

pr_fan = 1.8
pr_cLP = 1
pr_cHP = 6
m0 = 200
bpr = 2.5
Tt7 = 1400
Tt4 = 2000

sfc = np.array([])
isp = np.array([])
a = np.array([])
b = np.array([])

for i in [1400, 1500, 1600, 1700, 1800, 1900, 2000]:
    for j in [1.05, 1.1, 2, 4, 6, 10, 15, 18, 20]:
        cc = calc(pr_fan, pr_cLP, j, bpr, i, Tt7, m0)
        if 'sfc' in cc and 'Isp' in cc:
            if type(cc['sfc']) is float and type(cc['Isp']) is float:
                if 0 < cc['sfc'] and 0 < cc['Isp']:
                    sfc = np.append(sfc, cc['sfc'])
                    isp = np.append(isp, cc['Isp'])
                    a = np.append(a, i)
                    b = np.append(b, j)

print(sfc)
print(isp)
trace1 = go.Carpet(
    a=a,
    b=b,
    x=isp,
    y=sfc,
    aaxis=dict(
        gridcolor='black',
        color='black',
        tickprefix='TIT = ',
        smoothing=1.3
    ),
    baxis=dict(
        gridcolor='black',
        color='black',
        tickprefix='T_ab = ',
        smoothing=1.3
    )
)

data = [trace1]

fig = go.Figure(data=data)
py(fig)

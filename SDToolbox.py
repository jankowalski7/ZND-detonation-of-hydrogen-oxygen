import sys
import numpy as np
from cantera import *
from SDToolbox import *
import csv

# Keybord input
Tmin = 300
Tmax = 800
Pmin = 101325
Pmax = 405300
fimin = float(0.3)
fimax = float(1.5)

q = 'C2H6:1 O2:3.5'
mech = 'gri30_highT.cti'
# Number of iterations
npoints = 10

Ti = np.zeros(npoints, 'd')
Pi = np.zeros(npoints, 'd')
fi = np.zeros(npoints, 'd')
Tcj = np.zeros(npoints, 'd')
s = np.zeros(npoints, 'd')
Pcj = np.zeros(npoints, 'd')
vcj = np.zeros(npoints, 'd')

#######################Temperature function###############
for j in range(npoints):
    Ti[j] = Tmin + (Tmax - Tmin) * j / (npoints - 1)
    [cj_speed, R2] = CJspeed(101325, Ti[j], q, mech, 0)
    gas = PostShock_eq(cj_speed, 101325, Ti[j], q, mech)
    vcj[j] = gas.density
    Pcj[j] = gas.P / 100000
    Tcj[j] = gas.T
    s[j] = cj_speed

csv_file = 'sdt_Tempfunc.csv'
with open(csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Pressure', 'Initial temperature', 'cjspeed', 'Final Temperature', 'Final pressure', 'density'])
    for i in range(npoints):
        writer.writerow([101325, Ti[i], s[i], Tcj[i], Pcj[i], vcj[i]])

#######################Pressure function###############
for j in range(npoints):
    Pi[j] = Pmin + (Pmax - Pmin) * j / (npoints - 1)
    [cj_speed, R2] = CJspeed(Pi[j], 300, q, mech, 0)
    gas = PostShock_eq(cj_speed, Pi[j], 300, q, mech)
    vcj[j] = gas.density
    Pcj[j] = gas.P / 100000
    Tcj[j] = gas.T
    s[j] = cj_speed

csv_file = 'sdt_Pressurefunc.csv'
with open(csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Initial temperature', 'Pressure', 'cjspeed', 'Final Temperature', 'Final pressure', 'density'])
    for i in range(npoints):
        writer.writerow([300, Pi[i], s[i], Tcj[i], Pcj[i], vcj[i]])

#######################Fi function###############
for j in range(npoints):
    fi[j] = fimin + (fimax - fimin) * j / (npoints - 1)
    no = float(3.5 / fi[j])  # Number of O2 moles
    q = 'C2H6:1 O2:' + str(no)
    [cj_speed, R2] = CJspeed(101325, 300, q, mech, 0)
    gas = PostShock_eq(cj_speed, 101325, 300, q, mech)
    vcj[j] = gas.density
    Pcj[j] = gas.P / 100000
    Tcj[j] = gas.T
    s[j] = cj_speed

csv_file = 'sdt_Fifunc.csv'
with open(csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(
        ['Pressure', 'Initial temperature', 'fi', 'cjspeed', 'Final Temperature', 'Final pressure', 'density'])
    for i in range(npoints):
        writer.writerow([101325, 300, fi[i], s[i], Tcj[i], Pcj[i], vcj[i]])

print 'output written to csv files'
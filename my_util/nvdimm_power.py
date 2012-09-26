#!/usr/bin/python -O

import sys
import re

idle_energy_pattern = re.compile("Accumulated Idle Energy: ([0-9\.]+) mJ")
access_energy_pattern = re.compile("Accumulated Access Energy: ([0-9\.]+) mJ")
erase_energy_pattern = re.compile("Accumulated Erase Energy: ([0-9\.]+) mJ")
total_energy_pattern = re.compile("Total Energy: ([0-9\.]+) mJ")

idle_power_pattern = re.compile("Average Idle Power: ([0-9\.]+) mW")
access_power_pattern = re.compile("Average Access Power: ([0-9\.]+) mW")
erase_power_pattern = re.compile("Average Erase Power: ([0-9\.]+) mW")
total_power_pattern = re.compile("Average Power: ([0-9\.]+) mW")

fin = open('nvdimm_logs/NVDIMM.log', 'r')
fout1 = open('nvdimm_power.dat', 'w')
fout2 = open('nvdimm_energy.dat', 'w')
    
num_package = 0
idle_energy = 0
access_energy = 0
erase_energy = 0
total_energy = 0
idle_power = 0
access_power = 0
erase_power = 0 
total_power = 0

for line in fin:
    ie = idle_energy_pattern.match(line)
    ae = access_energy_pattern.match(line)
    ee = erase_energy_pattern.match(line)
    te = total_energy_pattern.match(line)

    ip = idle_power_pattern.match(line)
    ap = access_power_pattern.match(line)
    ep = erase_power_pattern.match(line)
    tp = total_power_pattern.match(line)

    if ie is not None: idle_energy += float(ie.group(1))
    if ae is not None: access_energy += float(ae.group(1))
    if ee is not None: erase_energy += float(ee.group(1))
    if te is not None: total_energy += float(te.group(1))

    if ip is not None:
        num_package += 1
        idle_power = (idle_power + float(ip.group(1))) / num_package
    if ap is not None:
        access_power = (access_power + float(ap.group(1))) / num_package
    if ep is not None:
        erase_power = (erase_power + float(ep.group(1))) / num_package
    if tp is not None:
        total_power = (total_power + float(tp.group(1))) / num_package

print >>fout1, "%f %f %f %f" %(total_power, idle_power, access_power, erase_power)
print >>fout2, "%f %f %f %f" %(total_energy, idle_energy, access_energy, erase_energy)

fin.close()
fout1.close()
fout2.close()

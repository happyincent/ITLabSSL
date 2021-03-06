#!/usr/bin/env python2
"""
Author        :Julio Sanz
Website       :www.elarraydejota.com
Email         :juliojosesb@gmail.com
Description   :Generate CPU graph from cpu.dat file
Dependencies  :Python 2.x, matplotlib
Usage         :python cpu.py
License       :GPLv3
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import csv
from datetime import datetime
import matplotlib.dates

# ======================
# VARIABLES
# ======================

# Aesthetic parameters
plt.rcParams.update({'font.size': 8})
plt.rcParams['lines.linewidth'] = 1.5
time_format = matplotlib.dates.DateFormatter('%H:%M:%S')
plt.gca().xaxis.set_major_formatter(time_format)
plt.gcf().autofmt_xdate()

# Time (column 0)
x = []
# Data arrays
user_cpu = []
system_cpu = []
idle_cpu = []

# ======================
# FUNCTIONS
# ======================

def generate_graph():
    with open('../../data/cpu.dat', 'r') as csvfile:
        data_source = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
        for row in data_source:
            # [0] column is a time column
            # Convert to datetime data type
            a = datetime.strptime((row[0]),'%H:%M:%S')
            x.append((a))
            # The remaining columns contain data
            user_cpu.append(row[2])
            system_cpu.append(row[4])
            idle_cpu.append(row[7])
    
    # Plot lines
    plt.plot(x,user_cpu, label='User %', color='g', antialiased=True)
    plt.plot(x,system_cpu, label='System %', color='r', antialiased=True)
    # plt.plot(x,idle_cpu, label='Idle %', color='b', antialiased=True)
    
    # Graph properties
    plt.xlabel('Time',fontstyle='italic')
    plt.ylabel('CPU %',fontstyle='italic')
    plt.title('CPU usage graph')
    plt.grid(linewidth=0.4, antialiased=True)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fancybox=True, shadow=True)
    plt.autoscale(True)
    
    # Graph saved to PNG file
    plt.savefig('../../graphs/cpu.png', bbox_inches='tight')
    #plt.show()

# ======================
# MAIN
# ======================

if __name__ == '__main__':
    generate_graph()
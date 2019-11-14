#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:41:07 2017

Script to plot power and HTC amplitudes during transient
Also plots gain and phase shift

To-Do: Test LaTeX figure export

@author: Rodrigo de Oliveira
"""
savePlot = False
latex = False

if latex:
    import matplotlib as mpl
    mpl.use("pgf")
    pgf_with_rc_fonts = {
        "font.family": "serif",
        "font.serif": [],                   # use latex default serif font
        "font.sans-serif": ["DejaVu Sans"], # use a specific sans-serif font
    }
    mpl.rcParams.update(pgf_with_rc_fonts)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import tau
from numpy import sin, degrees, mean, std
import peakutils
sns.set()

start_time = 200

ref_power = 1E9
htc = 1E6
amplitude = 0.1
period = 1.25

from pp_options import *

filePath= '../2.0_T{}_new/logPower.dat'.format(period)

power = pd.read_csv(filePath, sep=';', index_col='time')

power['power_amplitude'] = power['power']/ref_power

#print(power['power_amplitude'])
#print(power['power_amplitude'].values)
#power_peaks = peakutils.indexes(power['power_amplitude'].values, thres=0.9, min_dist=200)
power_peaks = peakutils.indexes(power['power_amplitude'].values, thres=conf[str(period)]['thres'], min_dist=conf[str(period)]['min_dist'])

#print(power_peaks)
#print(type(power_peaks))
#print(power.iloc[power_peaks])

power['htc'] = htc + htc*amplitude*sin(tau/period*power.index.values)
power['htc_amplitude'] = power['htc']/htc
htc_peaks = peakutils.indexes(power['htc_amplitude'].values, thres=0.9, min_dist=conf[str(period)]['min_dist'])

#print(power['htCoef_amplitude'])

fig, ax = plt.subplots()

power_conf = {'markevery': list(power_peaks),
              'marker': 'o',
              'markersize': 8
              }

power['power_amplitude'].plot.line(fontsize=14,
                                   figsize=(8.1,5),
                                   legend=None,
                                   ax=ax,
                                   **power_conf)

ax.set(xlabel='Time (s)',
       ylabel='Power amplitude')

#ax.set_xlim(xmin=200, xmax=220)
#ax.set_xlim(xmin=200, xmax=520)
ax.set_ylim(ymin=0.88, ymax=1.12)

ax2 = ax.twinx()

# set a single color cycler for both axes
ax2._get_lines.prop_cycler = ax._get_lines.prop_cycler

htc_conf = {'markevery': list(htc_peaks),
               'marker': 'X',
               'markersize': 8
               }

power['htc_amplitude'].plot.line(fontsize=14,
                                 figsize=(8.1,5),
                                 legend=None,
                                 ax=ax2,
                                 #yticks=[1.1, 1.0, 0.9],
                                 **htc_conf)

ax2.set(ylabel='HTC amplitude')
ax2.set_ylim(ymin=0.88, ymax=1.12)

# FREQUENCY RESPONSE

gain = 100*amplitude*(power['power_amplitude'].iloc[power_peaks].values-1)
phase_shift = degrees(tau/period * (power.iloc[power_peaks].index.values - power.iloc[htc_peaks].index.values))

freq_response = pd.DataFrame(data={'gain': gain, 'phase_shift': phase_shift}, columns=['gain', 'phase_shift'], index=power.iloc[power_peaks].index)

#print(freq_response)

fig, ax = plt.subplots()

freq_response['gain'].plot.line(fontsize=14,
                                figsize=(8.1,5),
                                legend=None,
                                ax=ax,
                                )

ax.set(xlabel='Time (s)',
       ylabel='Gain')

#ax.set_xlim(xmin=200, xmax=520)
#ax.set_ylim(ymin=0.985, ymax=1.015)

ax2 = ax.twinx()

# set a single color cycler for both axes
ax2._get_lines.prop_cycler = ax._get_lines.prop_cycler

freq_response['phase_shift'].plot.line(fontsize=14,
                                       figsize=(8.1,5),
                                       legend=None,
                                       ax=ax2,
                                       )

ax2.set(ylabel='Phase shift')

# setting the xlim manually is a temporary workaround while the simplified outputs are not
# writting the values at the initial time, 0 in this case. This is a known issue to be fixed.

mean_gain = mean(gain[-5:])
mean_phase_shift = mean(phase_shift[-5:])

std_gain = std(gain[-5:], ddof=1)
std_phase_shift = std(phase_shift[-5:], ddof=1)

print("The gain is: {}+-{}".format(mean_gain,std_gain))
print("The phase shift is: ", mean_phase_shift, "+-", std_phase_shift)

if savePlot:
    if latex:
        plt.savefig('power.pgf', bbox_inches='tight')
    else:
        plt.savefig('power.pdf', bbox_inches='tight')
else:
    plt.show()
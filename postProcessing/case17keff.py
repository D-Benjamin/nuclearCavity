import numpy as np
import matplotlib as mpl
mpl.use('pgf')

def figsize(scale):
    fig_width_pt = 417.68646                        # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "font.size": 10,
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
#    "font.size": 20,
#    "axes.labelsize": 20,               # LaTeX default is 10pt font.
#    "legend.fontsize": 16,               # Make the legend/label fonts a little smaller
#    "xtick.labelsize": 16,
#    "ytick.labelsize": 16,
    "figure.figsize": figsize(0.9),     # default fig size of 0.9 textwidth
    "pgf.texsystem": "lualatex",        # change this if using xetex or luatex
#    "pgf.preamble": [
#    r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
#    r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
#    ]
}
mpl.rcParams.update(pgf_with_latex)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def savefig(filename):
    plt.savefig('{}.pgf'.format(filename), bbox_inches='tight')
    plt.savefig('{}.pdf'.format(filename), bbox_inches='tight')

casePath = '../1.7/'
file = 'k_eff.dat'

reference_keff = 1.004134
reference_reactivity = (reference_keff-1)/reference_keff

powerRange = np.linspace(0, 1, 6)
velocityRange = np.linspace(0, 0.5, 6)

# matrix[power][velocity]
pow_vel = np.zeros(shape=(len(powerRange), len(velocityRange)))

# DataFrame accessed as data[velocity].loc[power]
data = pd.DataFrame(data=pow_vel, index=powerRange, columns=velocityRange)
data.index.name = 'Power (GW)'
data.columns.name = 'Velocity (m/s)'

for power in powerRange:
    for velocity in velocityRange:
        case = '1.7_P{power:.1f}_U{velocity:.1f}/'.format(power=power, velocity=velocity)
        keff_data = pd.read_csv(casePath + case + file, sep=';', index_col='time')
        last = keff_data.last_valid_index()
        keff = keff_data.at[last, 'k_eff']
        reactivity = (keff-1)/keff
        data.at[power, velocity] = (reactivity - reference_reactivity)*100000

plt.figure()
powerPlot = data.plot(figsize=figsize(0.7))
powerPlot.set(ylabel='Reactivity (pcm)')
savefig('equal_velocity')

plt.figure()
velocityPlot = data.T.plot(subplots=True,
                           layout=(3, 2),
                           sharex=True,
                           #fontsize=14,
                           figsize=(10, 8),
                           legend=None,
                           title=['Power 0.0 GW', 'Power 0.2 GW', 'Power 0.4 GW', 'Power 0.6 GW', 'Power 0.8 GW', 'Power 1.0 GW'])
#[ax.set(ylabel='Reactivity') for ax in plt.gcf().axes]
plt.gcf().axes[0].set(ylabel='Reactivity (pcm)')
plt.gcf().axes[2].set(ylabel='Reactivity (pcm)')
plt.gcf().axes[4].set(ylabel='Reactivity (pcm)')
savefig('equal_power')
#plt.show()

# filePath = '../k_eff.dat'
#
# savePlot = True
# latex = False
#
# if latex:
#     import matplotlib as mpl
#     mpl.use("pgf")
#     pgf_with_rc_fonts = {
#         "font.family": "serif",
#         "font.serif": [],                   # use latex default serif font
#         "font.sans-serif": ["DejaVu Sans"], # use a specific sans-serif font
#     }
#     mpl.rcParams.update(pgf_with_rc_fonts)
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# keff = pd.read_csv(filePath, sep=';', index_col='time')
#
# #print(list(keff)) # gives a list of data column names (['k_eff'] in this case)
# #print(keff.index.name) # gives the name of the index ('time' in this case)
#
# sns.set()
#
# plt.figure()
# ax = keff.plot.line(fontsize=14,
#                     figsize=(8.1,5),
#                     legend=None)
# #ax.set_title('$k_eff$ variation with time') # might be obvious...
# ax.set(xlabel='Time (s)',
#        ylabel='$k_eff$')
#
# # setting the xlim manually is a temporary workaround while the simplified outputs are not
# # writting the values at the initial time, 0 in this case. This is a known issue to be fixed.
# ax.set_xlim(xmin=0)
#
# if savePlot:
#     if latex:
#         plt.savefig('k_eff.pgf', bbox_inches='tight')
#     else:
#         plt.savefig('k_eff.pdf', bbox_inches='tight')
# else:
#     plt.show()

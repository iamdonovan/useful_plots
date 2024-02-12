import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


font = {'family': 'sans',
        'weight': 'normal',
        'size': 14}
matplotlib.rc('font', **font)

data = pd.read_csv('data/absorption_components.csv')
data.wavelength *= 1000

tdata = pd.read_csv('data/smoothed_transmission.csv')

patch_args = {'fc': 'k', 'ec': 'k', 'linewidth': 2}

fig, ax = plt.subplots(1, 1, figsize=(7, 9))
axs = fig.subplots(6, 1)

plt.setp(ax.spines.values(), visible=False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylabel('absorption (%)', labelpad=38)
ax.set_xlabel('wavelength (nm)', labelpad=25)


axs[0].fill_between(data.wavelength, data.CH4, **patch_args)

axs[1].fill_between(data.wavelength, data.N2O, **patch_args)
axs[1].fill_between(data.wavelength, data.N2, **patch_args)

axs[2].fill_between(data.wavelength, data.O2, **patch_args)
axs[2].fill_between(data.wavelength, data.O3, **patch_args)

axs[3].fill_between(data.wavelength, data.CO2, **patch_args)

axs[4].fill_between(data.wavelength, data.H2O, **patch_args)

axs[5].fill_between(tdata.wavelength, 1 - tdata.transmission, **patch_args)

axs[5].set_ylim(0, 1)
axs[5].set_yticks([0, 1])
axs[5].set_yticklabels(['0', '100'])

axs[5].set_xscale('log')
axs[5].set_xlim(100, 40000)
axs[5].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
axs[5].set_xticks([100, 200, 500, 1000, 2000, 5000, 10000, 40000])
axs[5].set_xticklabels([100, 200, 500, 1000, 2000, 5000, 10000, 40000])


labels = ['CH$_4$', 'N$_2$O, N$_2$', 'O$_2$, O$_3$', 'CO$_2$', 'H$_2$O', '']

for ind, ax in enumerate(axs[:-1]):
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['0', '100'])
    
    ax.set_xlim(100, 40000)
    ax.set_xticks([100, 200, 500, 1000, 2000, 5000, 10000, 40000])
    ax.set_xscale('log')

    ax.set_xticklabels('')
    
    ax.annotate(labels[ind], xy=(1.02, 0.5), xycoords='axes fraction', fontsize=12)


fig.savefig('figures/AbsorptionComponents.png', dpi=300, bbox_inches='tight')


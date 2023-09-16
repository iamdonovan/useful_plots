from scipy.constants import codata
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from pybob.plot_tools import set_pretty_fonts

set_pretty_fonts(font_size=18, legend_size=6)

h = codata.physical_constants['Planck constant'][0]
k = codata.physical_constants['Boltzmann constant'][0]
c = codata.physical_constants['speed of light in vacuum'][0]
wienConstant = 2.897e-3

def planck(wav, T):
    p = c * h / (k * wav * T)

    result = np.zeros(np.shape(wav)) + 1e-99
    result[p<700] = (h*c*c)/(np.power(wav[p<700], 5) * (np.exp(p[p<700])-1))

    return result

wavelengths = np.arange(1e-9, 3e-6, 1e-9)
temps = np.array([200, 300, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000])

cmap = plt.cm.magma(temps / temps.max())

sm = plt.cm.ScalarMappable(cmap='magma', norm=plt.Normalize(vmin=100, vmax=8000))

fig, ax = plt.subplots(1, 1)

vis = Rectangle((380, 1), 320, 2.5e14, fc='k', ec='k', alpha=0.25)
ax.add_patch(vis)

for i, temp in enumerate(temps):
    Lvec = np.logspace(-1, 4, 500) * wienConstant / temp
    ax.plot(Lvec * 1e9, planck(Lvec, temp), color=cmap[i], label=str(temp))

# ax.legend()

ax.set_xlabel('$\lambda$ (nm)')
ax.set_ylabel('radiance (W/sr/ m$^3$)')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1, 2.5e14)
ax.set_xlim(25, 3e6)

cbaxes = inset_axes(ax, width="3%", height="70%", loc=1)

cbar = plt.colorbar(sm, extend='both', cax=cbaxes)
cbaxes.yaxis.set_ticks_position('left')
cbar.set_label('Temperature (K)', fontsize='xx-small')
cbaxes.yaxis.set_label_position('left')
cbar.ax.tick_params(labelsize='xx-small')

fig.savefig('planck_plot.png', bbox_inches='tight', dpi=200)

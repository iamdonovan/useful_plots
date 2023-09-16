from pathlib import Path
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from pybob.plot_tools import set_pretty_fonts


colors = ['slategray', 'lawngreen', 'forestgreen', 'darkorange', 'yellowgreen']

set_pretty_fonts(font_size=24, legend_size=6)

lib_folder = '/home/bob/Documents/teaching/ulster/egm310/2020/lectures/plots'

data = pd.read_csv(os.path.join(lib_folder, 'reflectance_data.csv'))

fig, ax = plt.subplots(1, 1, figsize=(11, 9))

for ii, name in enumerate(data.columns[1:]):
    ax.plot(data['wavelengths'] * 1000, 100 * data[name], color=colors[ii], label=name, linewidth=2)

ax.legend(fontsize=18)

ax.set_ylim(0, 100)
ax.set_xlim(350, 2500)

ax.set_ylabel('$\\rho(\lambda)$ (pct.)')
ax.set_xlabel('$\lambda$ (nm)')

fig.savefig('pixel_reflectance.png', bbox_inches='tight', dpi=300)

f2, ax2 = plt.subplots(1, 1, figsize=(11,9))

mixture = 0.35 * data['grass'] + 0.25 * data['oak'] + 0.25 * data['roof tile'] + 0.1 * data['agave'] + 0.05 * data['concrete']

ax2.plot(data['wavelengths'] * 1000, 100 * mixture, color='k', label='mixed spectrum', linewidth=2)

ax2.legend(fontsize=18)

ax2.set_ylim(0, 100)
ax2.set_xlim(350, 2500)

ax2.set_ylabel('$\\rho(\lambda)$ (pct.)')
ax2.set_xlabel('$\lambda$ (nm)')

f2.savefig(Path('figures', 'mixed_reflectance.png'), bbox_inches='tight', dpi=300)


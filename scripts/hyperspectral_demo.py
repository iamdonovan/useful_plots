import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from pybob.plot_tools import set_pretty_fonts
from pybob.bob_tools import bin_data


set_pretty_fonts(font_size=24, legend_size=6)

lib_folder = '/home/bob/Documents/teaching/ulster/egm310/2020/lectures/plots'
wav = 'splib07a_Oak_Oak-Leaf-1_fresh_ASDFRa_AREF/splib07a_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt'
data = 'splib07a_Oak_Oak-Leaf-1_fresh_ASDFRa_AREF/splib07a_Oak_Oak-Leaf-1_fresh_ASDFRa_AREF.txt'

colors = ['red', 'blue', '0.8', '0.5', 'forestgreen']

wavelengths = pd.read_csv(os.path.join(lib_folder, wav), names=['wavelength'], header=1)
reflectance = pd.read_csv(os.path.join(lib_folder, data), names=['reflectance'], header=1)

wavelengths = wavelengths[reflectance.reflectance > 0].copy()
reflectance = reflectance[reflectance.reflectance > 0].copy()

aster_bands = [(520, 600), (630, 690), (780, 860), (1600, 1700), (2145, 2185), (2185, 2225), (2235, 2285), (2295, 2365), (2360, 2430)]
oli_bands = [(430, 450), (450, 510), (530, 590), (640, 670), (850, 880), (1360, 1380), (1570, 1650), (2110, 2290)]
modis_bands = [(405, 420), (438, 448), (459, 479), (483, 493), (526, 536), (545, 565), (620, 670), (662, 672), (673, 683), (743, 753), (841, 876), (862, 877), (1230, 1250), (1628, 1652), (2105, 2155)]
mss_bands = [(500, 600), (600, 700), (700, 800), (800, 1100)]
tm_bands = [(450, 520), (520, 600), (630, 690), (760, 900), (1550, 1750), (2080, 2350)]
s2_bands = [(421, 457), (439, 535), (537, 582), (646, 685), (694, 714), (731, 749), (768, 796), (767, 908), (931, 958), (1338, 1414), (1539, 1681), (2072, 2312)]


labels = ['ASTER', 'MODIS', 'Landsat 1-5 MSS', 'Landsat 8-9 OLI', 'Sentinel-2 MSI']

fig, ax = plt.subplots(1, 1, figsize=(11, 9))

ax.plot(wavelengths.dropna() * 1000, 100 * reflectance.dropna(), color='k', label='original signature', linewidth=2)

for ii, (label, bands) in enumerate(zip(labels[3:], [oli_bands, s2_bands])):
    _wave = []
    _refl = []

    for b in bands:
        this_wave = (b[0] + b[1]) / 2000
        this_refl = reflectance.reflectance[np.logical_and(wavelengths.wavelength >= b[0] / 1000, 
                                                           wavelengths.wavelength <= b[1] / 1000)].mean()
        _wave.append(this_wave)
        _refl.append(this_refl)

    ax.plot(np.array(_wave) * 1000, 100 * np.array(_refl), 'o-', color=colors[ii], label=label, linewidth=2)

ax.legend(fontsize=18)
ax.set_ylim(0, 100)
ax.set_xlim(300, 2500)

ax.set_ylabel('$\\rho(\lambda)$ (pct.)')
ax.set_xlabel('$\lambda$ (nm)')

fig.savefig('spectral_resolution_comparison.png', bbox_inches='tight', dpi=300)

f1, ax1 = plt.subplots(1, 1, figsize=(11, 9))

hyperion_bands = np.arange(0.357, 2.576, 0.01)
hyperion_refl = bin_data(hyperion_bands, reflectance.reflectance.values, wavelengths.wavelength.values)

ax1.plot(wavelengths.dropna() * 1000, 100 * reflectance.dropna(), color='k', label='original signature', linewidth=2)
ax1.plot(hyperion_bands * 1000, hyperion_refl * 100, 'o-', color='m', label='EO-1 Hyperion')

ax1.legend(fontsize=18)
ax1.set_ylim(0, 100)
ax1.set_xlim(300, 2500)

ax1.set_ylabel('$\\rho(\lambda)$ (pct.)')
ax1.set_xlabel('$\lambda$ (nm)')


f1.savefig('spectral_resolution_hyperion.png', bbox_inches='tight', dpi=300)


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from pybob.plot_tools import set_pretty_fonts


set_pretty_fonts(font_size=24, legend_size=6)

names = ['Weathered Basalt', 'Concrete', 'Conifer Meadow', 'Lawn Grass', 'Oak', 'Snow', 'Ocean Water']

colors = ['slategray', 'lightgray', 'forestgreen', 'lawngreen', 'darkorange', 'powderblue', 'blue']

wav_list = ['splib07a_Basalt_weathered_BR93-43_BECKb_AREF/splib07a_Wavelengths_BECK_Beckman_0.2-3.0_microns.txt',
            'splib07a_Concrete_WTC01-37A_ASDFRa_AREF/splib07a_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt',
            'splib07a_Conifer-Meadow-Mix_YNP-CM-1_AVIRISb_RTGC/splib07a_Wavelengths_AVIRIS_1996_0.37-2.5_microns.txt',
            'splib07a_Lawn_Grass_GDS91_green_BECKa_AREF/splib07a_Wavelengths_BECK_Beckman_0.2-3.0_microns.txt',
            'splib07a_Oak_Oak-Leaf-1_fresh_ASDFRa_AREF/splib07a_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt',
            'splib07a_Melting_snow_mSnw01a_ASDFRa_AREF/splib07a_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt',
            'splib07a_Seawater_Open_Ocean_SW2_lwch_BECKa_AREF/splib07a_Wavelengths_BECK_Beckman_0.2-3.0_microns.txt']

data_list = ['splib07a_Basalt_weathered_BR93-43_BECKb_AREF/splib07a_Basalt_weathered_BR93-43_BECKb_AREF.txt',
             'splib07a_Concrete_WTC01-37A_ASDFRa_AREF/splib07a_Concrete_WTC01-37A_ASDFRa_AREF.txt',
             'splib07a_Conifer-Meadow-Mix_YNP-CM-1_AVIRISb_RTGC/splib07a_Conifer-Meadow-Mix_YNP-CM-1_AVIRISb_RTGC.txt',
             'splib07a_Lawn_Grass_GDS91_green_BECKa_AREF/splib07a_Lawn_Grass_GDS91_green_BECKa_AREF.txt',
             'splib07a_Oak_Oak-Leaf-1_fresh_ASDFRa_AREF/splib07a_Oak_Oak-Leaf-1_fresh_ASDFRa_AREF.txt',
             'splib07a_Melting_snow_mSnw01a_ASDFRa_AREF/splib07a_Melting_snow_mSnw01a_ASDFRa_AREF.txt',
             'splib07a_Seawater_Open_Ocean_SW2_lwch_BECKa_AREF/splib07a_Seawater_Open_Ocean_SW2_lwch_BECKa_AREF.txt']

fig, ax = plt.subplots(1, 1, figsize=(11, 9))

vis = Rectangle((380, 0), 320, 100, fc='k', ec='k', alpha=0.25)

blue = Rectangle((450, 0), 60, 100, fc='b', ec='k', alpha=0.25)
green = Rectangle((530, 0), 60, 100, fc='g', ec='k', alpha=0.25)
red = Rectangle((640, 0), 30, 100, fc='r', ec='k', alpha=0.25)
nir = Rectangle((850, 0), 30, 100, fc='k', ec='k', alpha=0.25)
swir1 = Rectangle((1570, 0), 80, 100, fc='k', ec='k', alpha=0.25)
swir2 = Rectangle((2110, 0), 180, 100, fc='k', ec='k', alpha=0.25)

ax.add_patch(vis)
# ax.add_patch(blue)
# ax.add_patch(green)
# ax.add_patch(red)
# ax.add_patch(nir)

for i, (wav, data) in enumerate(zip(wav_list, data_list)):
    wavelengths = pd.read_csv(wav, names=['wavelength'], header=1)
    reflectance = pd.read_csv(data, names=['reflectance'], header=1)

    wavelengths = wavelengths[reflectance.reflectance > 0].copy()
    reflectance = reflectance[reflectance.reflectance > 0].copy()

    ax.plot(wavelengths.dropna() * 1000, 100 * reflectance.dropna(), color=colors[i], label=names[i], linewidth=2)

ax.legend(fontsize=18)

ax.set_ylim(0, 100)

ax.set_ylabel('$\\rho(\lambda)$ (pct.)')
ax.set_xlabel('$\lambda$ (nm)')

fig.savefig('spectral_plot.png', bbox_inches='tight', dpi=200)

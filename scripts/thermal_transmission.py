from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from scipy.constants import codata


def planck(wav, T):
    p = c * h / (k * wav * T)

    result = np.zeros(np.shape(wav)) + 1e-99
    result[p<700] = (h*c*c)/(np.power(wav[p<700], 5) * (np.exp(p[p<700])-1))

    return result


def plot_transmission(data):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)

    ax.add_patch(Polygon(data.values, alpha=0.8))

    ax.set_xlim(data['wavelength'].min(), data['wavelength'].max())
    ax.set_ylim(0, 100)

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20)

    ax.set_ylabel('atmospheric transmission (%)', size=20)
    ax.set_xlabel('wavelength (nm)', size=20)
    return fig, ax


data = pd.read_csv('smoothed_transmission.csv')
data['transmission'] *= 100

data = data.loc[data['wavelength'] > 3000]
data.loc[1364, 'wavelength'] = 3000
data.loc[1364, 'transmission'] = 0

f1, ax1 = plot_transmission(data)
f1.savefig('ThermalTransmission.png', bbox_inches='tight', dpi=300)

ax2 = ax1.twinx()

# now plot earth's spectral emittance
h = codata.physical_constants['Planck constant'][0]
k = codata.physical_constants['Boltzmann constant'][0]
c = codata.physical_constants['speed of light in vacuum'][0]
wienConstant = 2.897e-3

wavelengths = np.arange(1e-9, 3e-6, 1e-9)
temp = 300

Lvec = np.logspace(-1, 4, 500) * wienConstant / temp

radiance = planck(Lvec, temp)
ax2.plot(Lvec * 1e9, 100 * radiance / max(radiance), color='k', linewidth=2)

ax2.set_ylim(0, 100)
ax2.tick_params(axis='y', labelsize=20)
ax2.set_ylabel('emitted radiation (%)', size=20)

f1.savefig(Path('figures', 'ThermalTransmissionEmittance.png'), bbox_inches='tight', dpi=300)

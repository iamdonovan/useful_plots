import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import Rectangle, Polygon


def make_band_patch(lmin, lmax, color, yloc, height, **kwargs):
    return Rectangle((lmin, yloc), lmax-lmin, height, fc=color, ec='k', **kwargs)


def annotate_patch(ax, patch, label, fontsize):
    start = patch.get_x() + patch.get_width() / 2 # center horizontally
    yloc = patch.get_y() + patch.get_height() / 2 # center vertically
    lab = ax.annotate(label, xy=(start, yloc), xytext=(0, 0),
                      textcoords='offset points',
                      ha='center', va='center', color='w', size=fontsize) # use 11 pt font, centered vertically, left-aligned, ...
    return lab



def plot_sensor(ax0, ax1, sens, yloc, height, fontsize=11, **kwargs):
    patch_list = []

    for b in sens['bands']:
        num, lmin, lmax, color = b
        this_patch = make_band_patch(lmin, lmax, color, yloc, height, **kwargs)
        patch_list.append(this_patch)

        if num is not None:
            if ax0.get_xlim()[1] > lmin:
                ax0.add_patch(this_patch)
                annotate_patch(ax0, this_patch, str(num), fontsize)
            else:
                ax1.add_patch(this_patch)
                annotate_patch(ax1, this_patch, str(num), fontsize)

    left = min([b.get_bbox().xmin for b in patch_list])

    yloc = patch_list[0].get_y() + patch_list[0].get_height() / 2

    if sens['name'] is not None:
        if ax0.get_xlim()[0] < left:
            ax0.annotate(sens['name'], xy=(left, yloc), xytext=(-5, 0),
                         textcoords='offset points', ha='right', va='center', color='k', size=12)
        else:
            ax1.annotate(sens['name'], xy=(left, yloc), xytext=(-5, 0),
                         textcoords='offset points', ha='right', va='center', color='k', size=12)


data = pd.read_csv('smoothed_transmission.csv')
data['transmission'] *= 100


fig = plt.figure(figsize=(22, 8))
ax = fig.add_subplot(111)
# ax.set_frame_on(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

gs = gridspec.GridSpec(1, 3, hspace=0.1)

ax0 = fig.add_subplot(gs[0, 0:2])
ax1 = fig.add_subplot(gs[2])

ax0.add_patch(Polygon(data.values, alpha=0.5))
ax1.add_patch(Polygon(data.values, alpha=0.5))

ax0.spines['right'].set_visible(False)
# ax0.spines['top'].set_visible(False)
ax1.spines['left'].set_visible(False)
# ax1.spines['top'].set_visible(False)
ax1.set_yticks([])

#if only up to NIR
ax0.set_xlim(350, 920)
ax0.set_ylim(0, 100)
ax0.set_xticks(range(400, 920, 100))

# if SWIR
#ax0.set_xlim(350, 2050)
#ax0.set_ylim(0, 100)
#ax0.set_xticks(range(400, 2050, 200))

ax1.set_xlim(7450, 13950)
ax1.set_xticks(range(8000, 15000, 2000))
ax1.set_ylim(0, 100)

ax0.tick_params(axis='x', labelsize=20)
ax0.tick_params(axis='y', labelsize=20)
ax1.tick_params(axis='x', labelsize=20)

ax.set_ylabel('atmospheric transmission (%)', size=20, labelpad=40)
ax.set_xlabel('wavelength (nm)', size=20, labelpad=35)

kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
d = 0.02
off = 0.67
ax.plot((-d + off, +d + off), (-d, +d), **kwargs)
ax.plot((-d + off, +d + off), (1-d, 1+d), **kwargs)

# now, add a sensor

# MicaSense
MX_Red = {'name': 'MX-Red/Altum-PT',
               'bands':  [('B', 459, 491, 'b'),
                          ('G', 546.5, 573.5, 'g'),
                          ('R', 661, 675, 'r'),
                          ('R-Edge', 711, 723, 'darkred'),
                          ('NIR', 813.5, 870.5, 'dimgray')]}  

MX_Blue = {'name': 'MX-Blue',
               'bands':  [('CoastalB', 430, 458, 'mediumturquoise'),
                          ('G', 524, 538, 'g'),
                          ('R', 642, 658, 'r'),
                          ('R-Edge', 700, 710, 'darkred'),
                          ('R-Edge', 731, 749, 'darkred')]}  

Altum_PT = {'name': 'Altum-PT',
               'bands':  [('Panchromatic', 400, 850, 'slategrey'),
                          ('Thermal', 7500, 13500, 'dimgray')]}  

landsat_oli = {'name': 'Landsat 8',
               'bands': [(1, 430, 450, 'mediumturquoise'),
                         (2, 450, 510, 'b'),
                         (3, 530, 590, 'g'),
                         (4, 640, 670, 'r'),
                         (5, 850, 880, 'darkred'),
                         (6, 1570, 1650, 'dimgray'),
                         (7, 2110, 2290, 'dimgray'),
                         (9, 1360, 1380, 'silver'),
                         (10, 10600, 11190, 'khaki'),
                         (11, 11500, 12510, 'khaki')]}

sentinel2 = {'name': 'Sentinel-2',
             'bands': [(1, 433, 453, 'mediumturquoise'),
                       (2, 457.5, 522.5, 'b'),
                       (3, 542.5, 577.5, 'g'),
                       (4, 650, 680, 'r'),
                       (5, 697.5, 712.5, 'darkred'),
                       (6, 732.5, 747.5, 'darkred'),
                       (8, 784.5, 899.5, 'darkred'),
                       (9, 935, 955, 'silver'),
                       (10, 1360, 1390, 'silver'),
                       (11, 1565, 1655, 'dimgray'),
                       (12, 2100, 2280, 'dimgray')]}

sentinel2_8a = {'name': None,
                'bands': [(7, 773, 793, 'darkred'),
                          ('8a', 855, 875, 'darkred')]}

oli_pan = {'name': None,
           'bands': [('8', 500, 680, 'slategrey')]}

# And Plot!
plot_sensor(ax0, ax1, landsat_oli, 5, 5)
plot_sensor(ax0, ax1, oli_pan, 1.5, 3.5)
plot_sensor(ax0, ax1, sentinel2, 15, 5)
plot_sensor(ax0, ax1, sentinel2_8a, 12, 3)

plot_sensor(ax0, ax1, MX_Blue, 30, 10)
plot_sensor(ax0, ax1, MX_Red, 42.5, 10)
plot_sensor(ax0, ax1, Altum_PT, 55, 10)

fig.savefig('TransmissionMicasenseSensorBands.png', bbox_inches='tight', dpi=300)


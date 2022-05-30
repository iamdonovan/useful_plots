import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

    right = max([b.get_bbox().xmax for b in patch_list])

    yloc = patch_list[0].get_y() + patch_list[0].get_height() / 2

    if sens['name'] is not None:
        if ax0.get_xlim()[1] > right:
            ax0.annotate(sens['name'], xy=(right, yloc), xytext=(5, 0),
                         textcoords='offset points', ha='left', va='center', color='k', size=11)
        else:
            ax1.annotate(sens['name'], xy=(right, yloc), xytext=(5, 0),
                         textcoords='offset points', ha='left', va='center', color='k', size=11)


data = pd.read_csv('smoothed_transmission.csv')
data['transmission'] *= 100


fig = plt.figure(figsize=(22, 10))
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

ax0.set_xlim(400, 2500)
ax0.set_ylim(0, 100)
ax0.set_xticks(range(400, 2500, 500))

ax1.set_xlim(8000, 14000)
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
landsat_mss = {'name': 'Landsat 1-3 MSS',
               'bands':  [(4, 500, 600, 'g'),
                          (5, 600, 700, 'r'),
                          (6, 700, 800, 'darkred'),
                          (7, 800, 1100, 'dimgray')]}  

landsat_tm = {'name': 'Landsat 4-5 TM',
              'bands': [(1, 450, 520, 'b'),
                        (2, 520, 600, 'g'),
                        (3, 630, 690, 'r'),
                        (4, 760, 900, 'darkred'),
                        (5, 1550, 1750, 'dimgray'),
                        (6, 10400, 12500, 'khaki'),
                        (7, 2080, 2350, 'dimgray')]}

landsat_etm = {'name': 'Landsat 7 ETM+',
              'bands': [(1, 450, 520, 'b'),
                        (2, 520, 600, 'g'),
                        (3, 630, 690, 'r'),
                        (4, 760, 900, 'darkred'),
                        (5, 1550, 1750, 'dimgray'),
                        (6, 10400, 12500, 'khaki'),
                        (7, 2080, 2350, 'dimgray')]}

landsat_oli = {'name': 'Landsat 8 OLI/TIRS',
               'bands': [(1, 430, 450, 'seagreen'),
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

etm_pan = {'name': None,
           'bands': [('8', 520, 900, 'slategrey')]}

oli_pan = {'name': None,
           'bands': [('8', 500, 680, 'slategrey')]}

aster = {'name': 'ASTER',
         'bands': [(1, 520, 600, 'g'),
                   (2, 630, 690, 'r'),
                   ('3N', 780, 860, 'darkred'),
                   (4, 1600, 1700, 'dimgray'),
                   (5, 2145, 2185, 'dimgray'),
                   (6, 2185, 2225, 'dimgray'),
                   (7, 2235, 2285, 'dimgray'),
                   (8, 2295, 2365, 'dimgray'),
                   (9, 2360, 2430, 'dimgray'),
                   (10, 8125, 8475, 'khaki'),
                   (11, 8475, 8825, 'khaki'),
                   (12, 8925, 9275, 'khaki'),
                   (13, 10250, 10950, 'khaki'),
                   (14, 10950, 11650, 'khaki')]}

aster_3b = {'name': None,
            'bands': [('3B', 780, 860, 'darkred')]}

modis = {'name': 'MODIS',
         'bands': [(1, 620, 670, 'r'),
                   (2, 841, 876, 'darkred'),
                   (3, 459, 479, 'b'),
                   (4, 545, 565, 'g'),
                   (5, 1230, 1250, 'dimgray'),
                   (6, 1628, 1652, 'dimgray'),
                   (7, 2105, 2155, 'dimgray'),
                   (8, 405, 420, 'b'),
                   (9, 438, 448, 'b'),
                   (10, 483, 493, 'b'),
                   (11, 526, 536, 'g'),
                   (12, 546, 556, 'g'),
                   (13, 662, 672, 'r'),
                   (14, 673, 683, 'r'),
                   (15, 743, 753, 'darkred'),
                   (16, 862, 877, 'darkred'),
                   (17, 890, 920, 'darkred'),
                   (18, 931, 941, 'darkred'),
                   (19, 915, 965, 'darkred'),
                   (20, 3660, 3840, 'silver'),
                   ('21-22', 3929, 3989, 'silver'),
                   (23, 4020, 4080, 'silver'),
                   (24, 4433, 4498, 'gainsboro'),
                   (25, 4482, 4549, 'gainsboro'),
                   (26, 1360, 1390, 'silver'),
                   (27, 6535, 6895, 'silver'),
                   (28, 7175, 7475, 'silver'),
                   (29, 8400, 8700, 'silver'),
                   (30, 9580, 9880, 'khaki'),
                   (31, 10780, 11280, 'khaki'),
                   (32, 11770, 12270, 'khaki'),
                   (33, 13185, 13485, 'khaki'),
                   (34, 13485, 13785, 'khaki'),
                   (35, 13785, 14085, 'khaki'),
                   (36, 14085, 14385, 'khaki')]}

plot_sensor(ax0, ax1, landsat_mss, 5, 5)
plot_sensor(ax0, ax1, landsat_tm, 15, 5)
plot_sensor(ax0, ax1, landsat_etm, 30, 5)
plot_sensor(ax0, ax1, etm_pan, 27, 3)
plot_sensor(ax0, ax1, landsat_oli, 40, 5)
plot_sensor(ax0, ax1, oli_pan, 37, 3)

plot_sensor(ax0, ax1, aster, 50, 5)
plot_sensor(ax0, ax1, aster_3b, 47, 3)

plot_sensor(ax0, ax1, sentinel2, 60, 5)
plot_sensor(ax0, ax1, sentinel2_8a, 57, 3)

# plot_sensor(ax0, ax1, modis, 70, 5, fontsize=8)

fig.savefig('TransmissionSensorBands.png', bbox_inches='tight', dpi=300)


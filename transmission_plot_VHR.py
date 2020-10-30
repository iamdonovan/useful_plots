import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import gridspec
from matplotlib.patches import Rectangle, Polygon


def make_band_patch(lmin, lmax, color, yloc, height, **kwargs):
    return Rectangle((lmin, yloc), lmax-lmin, height, fc=color, ec='k', **kwargs)


def annotate_patch(ax, patch, label):
    start = patch.get_x() + patch.get_width() / 2 # center horizontally
    yloc = patch.get_y() + patch.get_height() / 2 # center vertically
    lab = ax.annotate(label, xy=(start, yloc), xytext=(0, 0),
                      textcoords='offset points',
                      ha='center', va='center', color='w', size=11) # use 11 pt font, centered vertically, left-aligned, ...
    return lab



def plot_sensor(ax0, sens, yloc, height, **kwargs):
    patch_list = []

    for b in sens['bands']:
        num, lmin, lmax, color = b
        this_patch = make_band_patch(lmin, lmax, color, yloc, height, **kwargs)
        patch_list.append(this_patch)
        
        if num is not None:
            if ax0.get_xlim()[1] > lmin:
                ax0.add_patch(this_patch)
                annotate_patch(ax0, this_patch, str(num))
        	
    right = max([b.get_bbox().xmax for b in patch_list])

    yloc = patch_list[0].get_y() + patch_list[0].get_height() / 2

    if sens['name'] is not None:
        ax0.annotate(sens['name'], xy=(right, yloc), xytext=(5, 0),
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

ax0 = fig.add_subplot(gs[0, 0:3])
#ax1 = fig.add_subplot(gs[2])

ax0.add_patch(Polygon(data.values, alpha=0.5))
#ax1.add_patch(Polygon(data.values, alpha=0.5))

#ax0.spines['right'].set_visible(False)
# ax0.spines['top'].set_visible(False)
#ax1.spines['left'].set_visible(False)
# ax1.spines['top'].set_visible(False)
#ax1.set_yticks([])

# if SWIR
#ax0.set_xlim(350, 2050)
#ax0.set_ylim(0, 100)
#ax0.set_xticks(range(400, 2050, 200))

#if only up to NIR
ax0.set_xlim(350, 1150)
ax0.set_ylim(0, 100)
ax0.set_xticks(range(400, 1150, 200))

#ax1.set_xlim(8000, 14000)
#ax1.set_xticks(range(8000, 15000, 2000))
#ax1.set_ylim(0, 100)

#ax0.tick_params(axis='x', labelsize=20)
#ax0.tick_params(axis='y', labelsize=20)
#ax1.tick_params(axis='x', labelsize=20)

ax.set_ylabel('atmospheric transmission (%)', size=20, labelpad=40)
ax.set_xlabel('wavelength (nm)', size=20, labelpad=35)

#kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
#d = 0.02
#off = 0.67
#ax.plot((-d + off, +d + off), (-d, +d), **kwargs)
#ax.plot((-d + off, +d + off), (1-d, 1+d), **kwargs)

# now, add a sensor

GE_1 = {'name': 'GeoEye-1 GIS',
               'bands':  [('B', 450, 510, 'b'),
			              ('G', 510, 580, 'g'),
                          ('R', 655, 690, 'r'),
                          ('NIR', 780, 920, 'dimgray')]}  
GE_1_P = {'name': None,
               'bands':  [('P', 450, 800, 'gray')]}
						  
WV_2 = {'name': 'WorldView-2 WV110',
               'bands':  [('Coastal', 400, 450, 'darkblue'),
			              ('B', 450, 510, 'b'),
			              ('G', 510, 580, 'g'),
			              ('Y', 585, 625, 'y'),
                          ('R', 630, 690, 'r'),
                          ('Re', 705, 745, 'darkred')]}  
WV_2_P = {'name': None,
               'bands':  [('P', 450, 800, 'gray')]}
			   
WV_3 = {'name': None,
               'bands':  [('Coastal', 400, 450, 'darkblue'),
			              ('B', 450, 510, 'b'),
			              ('G', 510, 580, 'g'),
			              ('Y', 585, 625, 'y'),
                          ('R', 630, 690, 'r'),
                          ('Re', 705, 745, 'darkred'),
                          ('SWIR1', 1195, 1225, 'dimgray'),
                          ('SWIR2', 1550, 1590, 'dimgray'),
                          ('SWIR3', 1640, 1680, 'dimgray'),
                          ('SWIR4', 1710, 1750, 'dimgray'),
                          ('SWIR5', 2145, 2185, 'dimgray'),
                          ('SWIR6', 2185, 2225, 'dimgray'),
                          ('SWIR7', 2235, 2285, 'dimgray'),
                          ('SWIR8', 2295, 2365, 'dimgray')]}  

WV_3_NIR1 = {'name': None,
               'bands':  [('NIR1', 780, 895, 'dimgray')]}  
WV_3_NIR2 = {'name': 'WorldView-3 MSS',
               'bands':  [('NIR2', 860, 1040, 'dimgray')]}  
WV_3_P = {'name': None,
               'bands':  [('P', 450, 800, 'gray')]}  
			   
WV_4 = {'name': 'WorldView-4',
               'bands':  [('B', 450, 510, 'b'),
			              ('G', 510, 580, 'g'),
                          ('R', 655, 690, 'r'),
                          ('NIR', 780, 920, 'dimgray')]}  
WV_4_P = {'name': None,
               'bands':  [('P', 450, 800, 'gray')]}  

			   
			   
Pleiades_1 = {'name': 'Pleiades-1(A/B)',
               'bands':  [('B', 430, 550, 'b'),
                          ('R', 600, 720, 'r'),
                          ('NIR', 750, 950, 'dimgray')]}  
Pleiades_1_G = {'name': None,
               'bands':  [('G', 490, 610, 'g')]}  
Pleiades_1_P = {'name': None,
               'bands':  [('P', 480, 830, 'gray')]}  

#TO BE CONFIRMED
Pleiades_NEO = {'name': 'Pleiades-NEO',
               'bands':  [('B', 430, 550, 'b'),
                          ('R', 600, 720, 'r'),
                          ('NIR', 750, 950, 'dimgray')]}  
Pleiades_NEO_G = {'name': None,
               'bands':  [('DB', 400, 450, 'darkblue'),
			              ('G', 490, 610, 'g'),
                          ('Re', 720, 760, 'darkred')]}  

#TO BE CONFIRMED
Pleiades_NEO_P = {'name': None,
               'bands':  [('P', 480, 830, 'gray')]} 
			   
			   
Spot_1_2_3 = {'name': 'SPOT-(1/2/3)',
               'bands':  [('G', 500, 590, 'g'),
                          ('R', 610, 680, 'r'),
                          ('NIR', 780, 890, 'dimgray')]}  
						  
Spot_1_2_3_P = {'name': None,
               'bands':  [('P', 500, 730, 'gray')]}  
						  
Spot_4 = {'name': 'SPOT-4 HR VIR',
               'bands':  [('G', 500, 590, 'g'),
                          ('R', 610, 680, 'r'),
                          ('NIR', 780, 890, 'dimgray')]} 
						  
Spot_4_M = {'name': None,
               'bands':  [('MIR', 1580, 1750, 'dimgray')]} 
						  
Spot_4_P = {'name': None,
               'bands':  [('P', 510, 730, 'gray')]}  
						  
Spot_5 = {'name': 'SPOT-5 HRG',
               'bands':  [('G', 500, 590, 'g'),
                          ('R', 610, 680, 'r'),
                          ('NIR', 780, 890, 'dimgray')]}  
Spot_5_M = {'name': None,
               'bands':  [('MIR', 1580, 1750, 'dimgray')]}  
Spot_5_P = {'name': None,
               'bands':  [('P', 480, 710, 'gray')]}  
						  
Spot_6_7 = {'name': 'SPOT-(6/7)',
               'bands':  [('B', 450, 525, 'b'),
                          ('G', 530, 590, 'g'),
                          ('R', 625, 695, 'r'),
                          ('NIR', 760, 890, 'dimgray')]}  
Spot_6_7_P = {'name': None,
               'bands':  [('P', 450, 745, 'gray')]}  


## French series
#plot_sensor(ax0, Spot_1_2_3, 5, 5)
#plot_sensor(ax0, Spot_1_2_3_P, 2, 3)
#plot_sensor(ax0, Spot_4, 15, 5)
#plot_sensor(ax0, Spot_4_M, 15, 5)
#plot_sensor(ax0, Spot_4_P, 12, 3)
#plot_sensor(ax0, Spot_5, 25, 5)
#plot_sensor(ax0, Spot_5_M, 25, 5)
#plot_sensor(ax0, Spot_5_P, 22, 3)
#plot_sensor(ax0, Spot_6_7, 35, 5)
#plot_sensor(ax0, Spot_6_7_P, 32, 3)
#plot_sensor(ax0, Pleiades_1, 45, 2.5)
#plot_sensor(ax0, Pleiades_1_G, 47.5, 2.5)
#plot_sensor(ax0, Pleiades_1_P, 42, 3)
#plot_sensor(ax0, Pleiades_NEO, 55, 2.5)
#plot_sensor(ax0, Pleiades_NEO_G, 57.5, 2.5)
#plot_sensor(ax0, Pleiades_NEO_P, 52, 3)
#
##DigitalGlobe
#plot_sensor(ax0, WV_4, 5, 5)
#plot_sensor(ax0, WV_4_P, 2, 3)
#plot_sensor(ax0, WV_3, 15, 5)
#plot_sensor(ax0, WV_3_P, 12, 3)
#plot_sensor(ax0, WV_3_NIR1, 15, 2.5)
#plot_sensor(ax0, WV_3_NIR2, 17.5, 2.5)
#plot_sensor(ax0, WV_2, 25, 5)
#plot_sensor(ax0, WV_2_P, 22, 3)
#plot_sensor(ax0, GE_1, 35, 5)
#plot_sensor(ax0, GE_1_P, 32, 3)

# Current
plot_sensor(ax0, Spot_6_7, 5, 5)
plot_sensor(ax0, Spot_6_7_P, 2, 3)
plot_sensor(ax0, Pleiades_1, 15, 2.5)
plot_sensor(ax0, Pleiades_1_G, 17.5, 2.5)
plot_sensor(ax0, Pleiades_1_P, 12, 3)
plot_sensor(ax0, WV_3, 25, 5) 
plot_sensor(ax0, WV_3_P, 22, 3)
plot_sensor(ax0, WV_3_NIR1, 25, 2.5)
plot_sensor(ax0, WV_3_NIR2, 27.5, 2.5)
plot_sensor(ax0, WV_2, 35, 5)
plot_sensor(ax0, WV_2_P, 32, 3)
plot_sensor(ax0, GE_1, 45, 5)
plot_sensor(ax0, GE_1_P, 42, 3)

fig.savefig('TransmissionVHRSensorBands.png', bbox_inches='tight', dpi=300)


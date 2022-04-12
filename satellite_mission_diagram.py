import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle


# generate a legend based on our color scheme and divisions
def make_legend(ax, names, colors):
    patches = []
    for n, c in zip(names, colors):
        patches.append(mpatches.Patch(color=c, label=n))

    ax.legend(loc='upper left', bbox_to_anchor=(0, 1), framealpha=1, handles=patches, 
              title='max. ground res.', title_fontsize=18, fontsize=18, borderaxespad=0)


# create a rectangular patch, given the satellite data
def make_patch(start_year, end_year, pos, fc, alpha):
    width = end_year - start_year
    patch = Rectangle((start_year, pos + 0.05), width, 0.9, fc=fc, alpha=alpha, zorder=3)
    return patch


def annotate_patch(ax, patch, label):
    width = patch.get_extents().width
    width_ = patch.get_bbox().width
    
    start = patch.get_bbox().xmin

    xloc = 5 # padding from where we start the text
    align = 'left' # alignment relative to the box

    box_width = width_ / width * (len(label) * 12 + 15) # figure out how big the text will be (12 pt font, 15 pt buffer)

    if width < len(label) * 12:  # if our bar is too small, text goes to the left
        start = start - box_width
        if start < ax.get_xlim()[0]: # if the box is too far left, text goes on the right
            start = patch.get_bbox().xmax
        clr = 'k'
    elif start + box_width > ax.get_xlim()[1]:  # even if the bar is big enough, if box goes too far right, move to the left side.
        start = start - box_width
        clr = 'k'
    else:
        clr = 'w'

    yloc = patch.get_y() + patch.get_height() / 2 # center vertically
    lab = ax.annotate(label, xy=(start, yloc), xytext=(xloc, 0),
                      textcoords='offset points',
                      ha=align, va='center', color=clr, size=11) # use 11 pt font, centered vertically, left-aligned, ...
    return lab


fig, ax = plt.subplots(1, 1, figsize=(24, 16))

ax.set_xlim(1968, 2024)
ax.tick_params(axis='x', labelsize=24)
ax.set_yticks([])

ax.spines['right'].set_visible(False) # keep only the bottom axis visible
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)

res_labels = ['< 1 m', '1-10 m', '10-30 m', '30-100 m', '> 100 m']
res_colors = ['blueviolet', 'cornflowerblue', 'lightseagreen', 'sandybrown', 'lightcoral']

today = 2022.25 # current year-ish

# lists of the satellite data.
# form is (name, start, end, position on graph, res_colors index, alpha)
# landsat missions
landsat = [('Landsat 1 MSS', 1972.5, 1978, 3, 1),
           ('Landsat 2 MSS', 1975, 1982, 3, 1),
           ('Landsat 3 MSS', 1978, 1983, 3, 1),
           ('Landsat 4 TM/MSS', 1982.5, 1993.9, 3, 1),
           ('Landsat 5 TM/MSS', 1984.25, 2013.5, 3, 1),
           ('Landsat 6 ETM+', 1993.7, 1993.8, 2, 1),
           ('Landsat 7 ETM+', 1999.25, 2003.5, 2, 1),
           ('SLC-Off', 2003.5, today, 2, 0.5),
           (None, today, 2025, 2, 0.2),
           ('Landsat 8 OLI/TIRS', 2013, today, 2, 1),
           (None, today, 2025, 2, 0.2),
           ('Landsat 9 OLI/TIRS', 2021.75, today, 2, 1),
           (None, today, 2025, 2, 0.2)]

# terra
terra = [('ASTER', 1999.9, today, 2, 1),
         (None, today, 2025, 2, 0.2),
         ('MODIS', 1999.9, today, 4, 1),
         (None, today, 2025, 4, 0.2)]

# sentinel-2
sentinel = [('Sentinel-2 MSI', 2015.5, today, 2, 1),
            (None, today, 2025, 2, 0.2)]

# SPOT
spot = [('SPOT 1', 1986, 1991, 2, 1),
        ('SPOT 2', 1990, 2009.5, 2, 1),
        ('SPOT 3', 1993.75, 1997.9, 2, 1),
        ('SPOT 4', 1998.25, 2013.5, 2, 1),
        ('SPOT 5', 2002.25, 2015.25, 1, 1),
        ('SPOT 6', 2012.75, today, 1, 1),
        (None, today, 2025, 1, 0.2),
        ('SPOT 7', 2014.5, today, 1, 1),
        (None, today, 2025, 1, 0.2)]

# ALOS-PRISM
alos = [('ALOS PRISM', 2006, 2011.5, 1, 1),
        ('ALOS-2 PRISM', 2014.5, today, 1, 1),
        (None, today, 2025, 1, 0.2)]

# pléiades
pleiades = [('Pléiades', 2012, today, 0, 1),
            (None, today, 2025, 0, 0.2)]

# DigitalGlobe/WorldView
wv = [('IKONOS', 1999.75, 2015.25, 0, 1),
      ('QuickBird', 2001.75, 2015, 0, 1),
      ('GeoEye-1', 2008.75, today, 0, 1),
      (None, today, 2025, 0, 0.2),
      ('WorldView-1', 2007.75, today, 0, 1),
      (None, today, 2025, 0, 0.2),
      ('WorldView-2', 2009.75, today, 0, 1),
      (None, today, 2025, 0, 0.2),
      ('WorldView-3', 2014.5, today, 0, 1),
      (None, today, 2025, 0, 0.2),
      ('WorldView-4', 2016.9, 2019, 0, 1)]

rapideye = [('RapidEye', 2008.75, 2020.25, 1, 1)]

planet = [('Planet', 2010.5, today, 1, 1),
          (None, today, 2025, 1, 0.2)]

# plot and annotate all of the sensors - change combination as you see fit.
this_pos = 0

for sens in landsat + terra + sentinel + spot + alos + pleiades + wv + rapideye + planet:
    label, start_year, end_year, fc, alpha = sens
    if label == 'Landsat 6 ETM+':
        patch = make_patch(start_year, end_year, 0, res_colors[fc], alpha)
    elif label is None:
        patch = make_patch(start_year, end_year, this_pos-1, res_colors[fc], alpha)        
    else:
        patch = make_patch(start_year, end_year, this_pos, res_colors[fc], alpha)
    ax.add_patch(patch)

    if label is not None: # if label not given, no annotation
        annotate_patch(ax, patch, label)
        if 'ETM+' not in label: # don't want to increase for these two.
            this_pos += 1

# set the ylimits and draw the lines
ax.set_ylim(0, this_pos)

# plot vertical ticks every 5 years...
for yr in range(1970, 2025, 5):
    ax.plot([yr, yr], [0, this_pos], 'k--', linewidth=0.5)

# plot the present-day
ax.plot([today, today], [0, this_pos], 'k', linewidth=1)

# add a legend for the ground resolution
make_legend(ax, res_labels, res_colors)

# add a box indicating free data
# free_box = Rectangle([1971, 0], 52.5, 11, fc=None, fill=False, ec='r', lw=3, zorder=3)
# ax.add_patch(free_box)

# ax.annotate('Free Data!', (1971.2, 10), size=20)  # placed based on landsat + terra + sentinel, above
fig.savefig('SatelliteMissions.png', dpi=100, bbox_inches='tight')

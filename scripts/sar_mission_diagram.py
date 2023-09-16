from pathlib import Path
from datetime import datetime
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

# today = 2020.75 # current year-ish
current_date = datetime.today().date()
frac_date = current_date.timetuple().tm_yday / datetime(current_date.year, 12, 31).timetuple().tm_yday

# get the current date as a decimal year to 2 digits
today = current_date.year + round(frac_date, 2)

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

ax.set_xlim(1990, current_date.year + 5)
ax.tick_params(axis='x', labelsize=24)
ax.set_yticks([])

ax.spines['right'].set_visible(False) # keep only the bottom axis visible
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)

res_labels = ['X-band', 'C-band', 'L-band']
res_colors = ['blueviolet', 'cornflowerblue', 'lightseagreen']

# lists of the satellite data.
# form is (name, start, end, position on graph, res_colors index, alpha)
ers = [('ERS-1', 1991.5, 2000.25, 1, 1),
       ('ERS-2', 1995.25, 2011.75, 1, 1),
       ('Envisat', 2002.25, 2012.25, 1, 1)]

sentinel = [('Sentinel-1', 2014.25, today, 1, 1),
            (None, today, 2025, 1, 0.2)]

terrasar = [('TerraSAR-X', 2007.5, today, 0, 1),
            (None, today, 2025, 0, 0.2)]

radarsat = [('RADARSAT-1', 1995.75, 2013.25, 1, 1),
            ('RADARSAT-2', 2008, today, 1, 1),
            (None, today, 2025, 1, 0.2)]

alos = [('ALOS PALSAR', 2006, 2011.5, 2, 1),
        ('ALOS-2 PALSAR-2', 2014.5, today, 2, 1),
        (None, today, 2025, 2, 0.2)]


cosmo = [('COSMO-SkyMed', 2007.5, today, 0, 1),
         (None, today, 2025, 0, 0.2)]

# plot and annotate all of the sensors - change combination as you see fit.
this_pos = 0

for sens in ers + sentinel + terrasar + radarsat + alos + cosmo:
    label, start_year, end_year, fc, alpha = sens
    if label is None:
        patch = make_patch(start_year, end_year, this_pos-1, res_colors[fc], alpha)        
    else:
        patch = make_patch(start_year, end_year, this_pos, res_colors[fc], alpha)
    ax.add_patch(patch)

    if label is not None: # if label not given, no annotation
        annotate_patch(ax, patch, label)
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

# save the figure
fig.savefig(Path('figures', 'SARSatelliteMissions.png'), dpi=300, bbox_inches='tight')

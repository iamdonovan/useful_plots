import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import Rectangle, Polygon


def make_region_patch(reg):
    return Rectangle((reg['lower'], -1), reg['upper'] - reg['lower'], 2, fc='0.8', ec='k')


def annotate_patch(ax, patch, label):
    right = patch.get_x() + patch.get_width()
    left = patch.get_x()

    start = 10**(np.log10([left, right]).mean())
    yloc = patch.get_y() + patch.get_height() / 2 # center vertically
    lab = ax.annotate(label, xy=(start, yloc), xytext=(0, 0),
                      textcoords='offset points',
                      ha='center', va='center', color='k', size=11) # use 11 pt font, centered vertically, left-aligned, ...
    return lab

def lambda2nu(wavelength):
    return 3e8 / wavelength


def rainbow_patch(x, dx, h, c):
    return plt.Rectangle((x, -1), dx, h, color=c)


fig = plt.figure(figsize=(15, 3))
ax0 = fig.add_subplot(111)
ax0.set_frame_on(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
ax0.set_xticks([])
ax0.set_yticks([])

# ax0.vlines([0.3772, 0.3892], 0.68, 0.8, colors='k', linestyles='dashed', lw=1)
ax0.plot([0.2929, 0.3772], [0.326, 0.665], 'k--', lw=1)
ax0.plot([0.3892, 0.5604], [0.665, 0.326], 'k--', lw=1)

ax0.set_xlim(0, 1)
ax0.set_ylim(0, 1)


gs = gridspec.GridSpec(9, 7, hspace=0.1)

ax = fig.add_subplot(gs[1:3, :])
vis_ax = fig.add_subplot(gs[6, 2:4])

# ax.set_xticks([])
ax.set_yticks([])

regions = ['gamma', 'x', 'uv', 'vis', 'infrared', 'microwave', 'radio', 'long_radio']
full = [r'$\gamma$-rays', 'X-rays', 'UV', '', 'Infrared',
        'Microwave', 'Radio', 'Long radio waves']

upper = np.array([1e-4, 10, 380, 720, 1e5, 1e9, 1e12, 1e20]) / 1e9
lower = np.array([1e-8, 1e-4, 10, 380, 720, 1e5, 1e9, 1e12]) / 1e9

rdict = {}
for name, f, low, upp in zip(regions, full, lower, upper):
    rdict[name] = {'upper': upp, 'lower': low, 'full': f}

for name in regions:
    p = make_region_patch(rdict[name])
    ax.add_patch(p)
    annotate_patch(ax, p, rdict[name]['full'])

# ax.semilogx()
ax.set_ylim(-1, 1)
ax.set_xscale('log')
ax.set_xlim(lower[0], upper[-1])

freqs = list(range(24, -1, -2))
wavelengths = lambda2nu(np.array([10**x for x in range(24, -1, -2)], dtype=float))

ax.set_xticks([float(10**x) for x in range(-16, 10, 2)])

ax2 = ax.secondary_xaxis('top')
ax2.set_xticks(wavelengths, labels=['$10^{' + str(f) + '}$' for f in freqs])

vis = np.linspace(380, 720, 100) / 1e9
dx = vis[1] - vis[0]

vis_cmap = plt.get_cmap('rainbow')

for n, x in enumerate(vis):
    color = vis_cmap(n / vis.size)
    ax.add_patch(rainbow_patch(x, dx, 2, color))
    vis_ax.add_patch(rainbow_patch(x * 1e9, dx * 1e9, 40, color))

# fudge the upper xtick labels
# secax = ax.secondary_xaxis('top')

vis_ax.set_xlim(380, 720)
vis_ax.set_yticks([])

vis_ax.set_xlabel('wavelength (nm)')

ax.annotate(r'$\lambda$ (m)', (1.0, -0.03), xycoords='axes fraction', ha='right', va='top')
ax.annotate(r'$\nu$ (Hz)', (1.0, 1.05), xycoords='axes fraction', ha='right', va='bottom')

ax0.annotate(r'Increasing wavelength ($\lambda$) $\rightarrow$', (0.6, 0.48), xycoords='axes fraction')
ax0.annotate(r'$\leftarrow$ Increasing frequency ($\nu$)', (0.6, 1.05), xycoords='axes fraction')

fig.savefig('figures/ElectromagneticSpectrum.png', bbox_inches='tight')

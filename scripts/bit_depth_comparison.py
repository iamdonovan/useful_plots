import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import ImageGrid
from pybob.GeoImg import GeoImg


fn_img = '/home/bob/Downloads/LC08_L1TP_207022_20170503_20170515_01_T1/LC08_L1TP_207022_20170503_20170515_01_T1_B5.TIF'

img = GeoImg(fn_img)
img = img.crop_to_extent([646258, 652732, 6117787, 6121495], pixel_size=30)

fig = plt.figure(figsize=(20, 6))

axgrid = ImageGrid(fig, 111, nrows_ncols=(2, 4), axes_pad=(0.1, 0.4))

bit_depths = [1, 2, 4, 6, 8, 10, 12, 16]

# sm = plt.cm.ScalarMappable(cmap='seismic', norm=plt.Normalize(vmin=-200, vmax=200))

for i, bdepth in enumerate(bit_depths):
    ax = axgrid[i]

    mfact = 2**bdepth - 1
    img_stretch = np.round(mfact * (img.img - img.img.min()) / (img.img.max() - img.img.min()))
    im = ax.imshow(img_stretch, cmap='gray', vmin=0, vmax=mfact, norm=colors.PowerNorm(gamma=0.5))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('{}-bit'.format(bdepth), fontsize=20)

# axgrid.cbar_axes[0].colorbar(im, extend='both')

fig.savefig('BitDepthExample.png', bbox_inches='tight', dpi=300, transparent=True)

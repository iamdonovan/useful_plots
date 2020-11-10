import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch, Polygon
from mpl_toolkits.mplot3d import proj3d
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np


# https://stackoverflow.com/questions/29188612/arrows-in-matplotlib-using-mplot3d
# courtesy of user tacaswell
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


fig = plt.figure(figsize=(20, 10))

ax = fig.add_subplot(111, projection='3d')


t = np.arange(0, 4 * np.pi + 0.01, 0.01)
coords = np.vstack([t, np.sin(t)]).T

tx = np.arange(0, 4 * np.pi, np.pi / 6)

e = ax.plot(t, np.sin(t), 0 * t, zdir='y', color='b')
b = ax.plot(t, np.sin(t), 0 * t, zdir='z', color='r')

p = Polygon(coords, fc='r', alpha=0.2, ec='r')
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')

p = Polygon(coords, fc='b', alpha=0.2, ec='b')
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir='y')

b_prop_dict = dict(mutation_scale=10, arrowstyle='-|>', color='r', shrinkA=0, shrinkB=0)
e_prop_dict = dict(mutation_scale=10, arrowstyle='-|>', color='b', shrinkA=0, shrinkB=0)
for _t in tx: 
    a = Arrow3D([_t, _t], [0, 0], [0, np.sin(_t)], **e_prop_dict)
    ax.add_artist(a)

    a = Arrow3D([_t, _t], [0, np.sin(_t)], [0, 0], **b_prop_dict)
    ax.add_artist(a)

ax._axis3don = False

ax.set_xlim(1.75, 10.8) # have to do some weirdness to zoom in on the axis
ax.set_ylim(-0.7, 0.7)
ax.set_zlim(-0.7, 0.7)

arrow_prop_dict = dict(mutation_scale=20, arrowstyle='-|>', color='k', shrinkA=0, shrinkB=0, linewidth=3)

xax = Arrow3D([-1, 14], [0, 0], [0, 0], **arrow_prop_dict)
yax = Arrow3D([0, 0], [-1, 1.2], [0, 0], **arrow_prop_dict)
zax = Arrow3D([0, 0], [0, 0], [-1, 1.2], **arrow_prop_dict)

ax.add_artist(xax)
ax.add_artist(yax)
ax.add_artist(zax)

# arrow_prop_dict.update({'color': (187/255, 164/255, 97/255)})
# ph = Arrow3D([0, .75 * np.pi], [0, 0], [0, 0], **arrow_prop_dict)
# ax.add_artist(ph)

ax.view_init(elev=20, azim=-66)

xt = ax.text(14, 0, 0, 'x', zdir=None, fontsize=36)
yt = ax.text(0, 1.2, 0, 'y', zdir=None, fontsize=36)
zt = ax.text(0, 0, 1.2, 'z', zdir=None, fontsize=36)

fig.savefig('emr_wave.png', transparent=True, dpi=300)


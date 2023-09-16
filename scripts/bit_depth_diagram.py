import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


fig, ax = plt.subplots(1, 1, figsize=(8, 10))

ax.spines['right'].set_visible(False) # keep only the bottom axis visible
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

cmap = plt.cm.get_cmap('gray')

for pos, nbit in enumerate([1, 2, 4, 6, 8, 10, 12]): 
    norm = lambda x: x / (2**nbit-1) 
    for i in range(2**nbit): 
        rect = Rectangle((i/(2**nbit), pos+.55), 1/(2**nbit), 0.9, fc=cmap(norm(i))) 
        ax.add_patch(rect) 
    ax.add_patch(Rectangle((0, pos+0.55), 1, 0.9, fill=False, ec='k', lw=0.5))

ax.set_yticks(range(1,8))
ax.set_yticklabels([1, 2, 4, 6, 8, 10, 12], fontsize=24)

ax.invert_yaxis()

ax.set_xticks([0.0, 1.0])
ax.set_xticklabels(['dark', 'bright'], fontsize=24)

ax.set_ylim(7.53, 0.54)
ax.set_xlim(-.001, 1.001)

ax2 = ax.twinx()

ax2.spines['right'].set_visible(False) # keep only the bottom axis visible
ax2.spines['left'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

ax2.set_yticks(range(1,8))
ax2.set_yticklabels(['2$^1$ = 2', '2$^2$ = 4', '2$^4$ = 16', '2$^6$ = 64', '2$^8$ = 256', '2$^{10}$ = 1024', '2$^{12}$ = 4096'], fontsize=24)
ax2.set_ylim(7.53, 0.54)

fig.text(0.02, 0.9, 'bit depth', fontsize=24)
fig.text(0.9, 0.9, 'possible values', fontsize=24)

fig.savefig('BitDepths.png', bbox_inches='tight', dpi=200, transparent=True)

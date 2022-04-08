'''
The Spirals Module 
'''

import matplotlib as mp
import matplotlib.pyplot as plt
import mplcursors

import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg

import logging
import math as math
import numpy as np

#  fig, ax = plt.subplots()

    
def plt_init_polar():
    '''configure the MatPlotLib stateful plot engine'''
    mp.style.use('dark_background')


def spiral(n=144, cmap=mp.cm.YlGn, color_cycle=21, rev=False, offset=0):
    plt.cla()
    plt_init_polar()
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    for i in range(n):
        # radius = i * phi
        radius = n - i 
        ratio = (1 + math.sqrt(5)) / 2
        theta = 2 * np.pi * i * ratio
        # print(radius, theta)

        n_pad = str(n).zfill(4)
        cycle_pad = str(color_cycle).zfill(4)
    
        color_scale = (((i + offset) % color_cycle) / color_cycle)
        color_scale = color_scale + (1 / (color_cycle * 2))
        if rev:
            color_scale = 1 - color_scale
        color = cmap(color_scale)
        # print(color)
        title = f'G E O M E T O R • {cmap.name} • cycle: {cycle_pad} • n: {n_pad}'
        ax.set_title(title, fontdict={'color': '#960', 'size':'small'})
        ax.set_axis_off()

        ax.plot(theta, radius, marker='.', markersize=math.sqrt(radius)+4, color=color)

        
def spiral_params(params):
    '''take params in single dict for multiprocessing'''
    n = params['n']
    n_pad = str(n).zfill(4)
    color_cycle = params['color_cycle']
    cycle_pad = str(color_cycle).zfill(4)
    cmap = params['cmap']
    
    spiral(n=n, cmap=cmap, color_cycle=color_cycle)
    
    out = f'out/{cmap.name}-{cycle_pad}'
    if not os.path.isdir(out):
        os.mkdir(out)
    filename = f'{out}/{cmap.name}-{cycle_pad}-{n_pad}.png'
    plt.savefig(filename, dpi=300)
    return filename
'''
functions for working with color
'''
import matplotlib as mp

def get_colors(cmap_name, steps):
    '''
    return a list of colors n regular steps from a colormap
    '''
    cmap = mp.cm.get_cmap(cmap_name)
    colors = []
    offset = 1 / (2 * steps)
    for step in range(steps):
        color_scale = (((step + offset) % steps) / steps)
        #  color_scale = color_scale + (1 / (color_cycle * 2))
        #  if rev:
            #  color_scale = 1 - color_scale
        colors.append(cmap(color_scale))
    return colors


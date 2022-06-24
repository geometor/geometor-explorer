
import matplotlib as mp
import matplotlib.pyplot as plt
from ..utils import *
from ..render.utils import *

#  FIG_W = 16
#  FIG_H = 9

plt.rcParams['figure.figsize'] = [FIG_W, FIG_H]
plt.style.use('dark_background')



def plot_title(title, folder, filename, color='w', size=44):
    """TODO: Docstring for plot_title.

    :title: TODO
    :returns: TODO

    """
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)

    fig, ax = plt.subplots(1, 1)
    plt.tight_layout()
    ax.axis('off')
    ax.set_aspect('equal')
    ax.clear()
    ax.axis(False)
    ax.text(0.5, 0.5, title, ha='center', va='center', fontdict={'color': color, 'size': size})

    return snapshot_2(folder, filename)
    #  plt.show()

def plot_overlay(title, folder, filename, color='w', size=44):
    """TODO: Docstring for plot_overlay.

    :title: TODO
    :returns: TODO

    """
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)

    fontdict={'family': 'Fira Sans Condensed', 'color': color, 'size': size}

    fig, ax = plt.subplots(1, 1)
    plt.tight_layout()
    ax.axis('off')
    ax.set_aspect('equal')
    ax.clear()
    ax.axis(False)
    ax.text(0.15, 0.8, title, 
            ha='center', va='top', 
            fontdict={'color': color, 'size': size})

    return snapshot_2(folder, filename, transparent=True)
    #  plt.show()


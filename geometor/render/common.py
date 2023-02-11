
import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg
from sympy.abc import x, y

import matplotlib as mp
import matplotlib.pyplot as plt
import mplcursors

import math as math
import numpy as np
from collections import defaultdict
import logging

from itertools import permutations, combinations
from multiprocessing import Pool, cpu_count

from geometor.utils import *
#  from geometor.render import *

Z_POINT_HILITE = 1  #hilite under everything
Z_POINT_OUTER = 50  #dark ring
Z_POINT_INNER = 51  #light dot

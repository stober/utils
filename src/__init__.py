#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: __INIT__.PY
Date: Friday, March 23 2012
Description: Common utilities.
"""

from pickle_utils import load_or_compute,loaditer
from plot_utils import dual_scatter, lvl_scatter,scatter
from utils import create_cluster_colors, create_cluster_colors_rgb, find_duplicates, find_matches, rsme,incavg,consumer, debugflag, timerflag, sp_create, sp_create_data,chunk,flip, sp_create_dict
from axline import plot_line

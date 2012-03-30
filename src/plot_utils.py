#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: PLOTUTILS.PY
Date: Wednesday, April 21 2010
Description: Routines for common plot operations.
"""

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import matplotlib.patches as patches
import pdb

def save_show_no(plotfunc):
    # A function decorator that adds the option to save or show a plot
    # depending on whether a filename option is set.

    def decorate(*args,**kwargs):

        ax = plotfunc(*args)

        if 'filename' in kwargs.keys():

            plt.savefig(kwargs['filename'])

        elif 'show' in kwargs.keys():

            plt.show()

        else:

            return ax

    return decorate


@save_show_no
def scatter3d(x,y,z):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x,y,z)
    return ax

@save_show_no
def scatter3d_with_graph(x,y,z,adj):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x,y,z,color='b')

    # now draw edges between pts that are connected
    tmp = np.nonzero(adj)
    indices = []

    for pt in zip(tmp[0],tmp[1]):
        if pt[0] < pt[1]:
            indices.append(pt[0])
            indices.append(pt[1])

    zs = [z[i] for i in indices]
    vertices = [[x[i],y[i]] for i in indices]
    codes = [Path.MOVETO, Path.LINETO] * (len(indices) / 2)

    indx = range(len(indices))
    for i in indx[::2]:
        l,k = indices[i],indices[i+1]
        # just plot the single additional line
        ax.plot([x[l],x[k]],[y[l],y[k]],[z[l],z[k]],color='r')

    return ax

@save_show_no
def scatter(x,y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y)
    return ax

@save_show_no
def scatter_with_graph(x,y,adj):

    # start with a normal scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y,color='b')

    # now draw edges between pts that are connected
    tmp = np.nonzero(adj)
    indices = []

    for pt in zip(tmp[0],tmp[1]):
        if pt[0] < pt[1]:
            indices.append(pt[0])
            indices.append(pt[1])

    vertices = [[x[i],y[i]] for i in indices]
    codes = [Path.MOVETO, Path.LINETO] * (len(indices) / 2)

    path = Path(vertices, codes)
    patch = patches.PathPatch(path,lw=1,color='r')
    ax.add_patch(patch)

    return ax

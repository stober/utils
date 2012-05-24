#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: AXLINE.PY
Date: Wednesday, May 23 2012
Description: Plot arbitrary lines.
"""

import pylab

def project(x, pt):
    """
    Project a point onto a line in Ax + By + C = 0 form.
    x : [A,B,C] line parameters
    pt : (x,y) the point to project
    """

    i = pt[0] + -(x[0] * pt[0] + x[1] * pt[1] + x[2]) * x[0] / (x[0] ** 2 + x[1] ** 2)
    j = pt[1] + -(x[0] * pt[0] + x[1] * pt[1] + x[2]) * x[1] / (x[0] ** 2 + x[1] ** 2)

    return [i,j]

def plot_line(x, xlim, ylim):
    """
    like axhline and variants, but for lines with arbitrary slope.
    x : [A,B,C] line parameters.
    xlim,ylim: plot boundaries
    """

    pt1 = [xlim[0],ylim[0]]
    pt2 = [xlim[0],ylim[1]]
    pt3 = [xlim[1],ylim[0]]
    pt4 = [xlim[1],ylim[1]]

    # project corners of plot onto the line
    nt1 = project(x, pt1)
    nt2 = project(x, pt2)
    nt3 = project(x, pt3)
    nt4 = project(x, pt4)

    x = [i[0] for i in (nt1,nt2,nt3,nt4)]
    y = [i[1] for i in (nt1,nt2,nt3,nt4)]
    pylab.plot(x,y)

    # The trick is to now only show the part of the line we care about.
    pylab.gca().set_xlim(xlim)
    pylab.gca().set_ylim(ylim)


if __name__ == '__main__':

    pylab.plot([0,1],[1,0])
    line_params = np.array([-1,-1,1])

    pt = np.array([0.1,0.6])
    npt = project(line_params,pt)
    pylab.scatter(npt[0],npt[1])

    pt = np.array([0.6,0.1])
    npt = project(line_params,pt)
    pylab.scatter(npt[0],npt[1])

    pt = np.array([0.6,0.8])
    npt = project(line_params,pt)
    pylab.scatter(npt[0],npt[1])

    pylab.gca().set_xlim([0,1])
    pylab.gca().set_ylim([0,1])
    pylab.gcf().set_figwidth(8.0)
    pylab.gcf().set_figheight(8.0)

    pylab.show()

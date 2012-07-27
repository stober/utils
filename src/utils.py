#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: UTILS.PY
Date: Tuesday, March  8 2011
Description: Utility functions.
"""

import ImageColor
import numpy as np
import random as pr
import numpy.linalg as la
import scipy.misc
import cPickle as pickle
import bz2
import sys
import traceback
import time


# Decorators

def consumer(func):
    def start(*args,**kwargs):
        c = func(*args,**kwargs)
        c.next()
        return c
    return start

def timerflag(func):
    def wrapper(*args, **kwargs):
        if kwargs.has_key('timer') and kwargs['timer']:
            del kwargs['timer']
            starttime = time.time()
            result = func(*args, **kwargs)
            endtime = time.time()
            print "# seconds: ", endtime - starttime
        else:
            result = func(*args, **kwargs)

        return result
    return wrapper
    

def debugflag(func):
    def wrapper(*args, **kwargs):        
        if kwargs.has_key('debug') and kwargs['debug']:
            import pdb
            pdb.set_trace()

        if kwargs.has_key('debug'):
            del kwargs['debug']

        return func(*args, **kwargs)
    return wrapper

# End Decorators

def rsme(p,r):
    return np.sqrt( np.sum((x - y)**2 for x,y in zip(p,r)) / len(p) )


@consumer
def incavg(val = None):
    """
    Can optionally send the first value at initialization. .send returns the former avg. call .next after to get the current avg.
    """

    cnt = 0
    avg = 0
    
    if not val is None:
        cnt = 1
        avg = val

    while True:
        val = (yield avg)

        if val is None:
            pass # next was called
        elif cnt == 0: # first value
            cnt = 1
            avg = val
        else:
            cnt += 1
            avg = avg + (val - avg) / float(cnt)

def find_matches(s,t):
    n = len(s)
    m = len(t)
    for i in xrange(n):
        for j in xrange(m):
            if np.allclose(s[i], t[j]):
                yield i,j
    

def find_duplicates(l):
    n = len(l)
    for i in xrange(n):
        for j in xrange(i):
            if np.allclose(l[i],l[j]):
                yield i,j

def flip(p):
    if pr.random() < p:
        return True
    else:
        return False

def flat_dict(d):
    """
    Return a dict where sets are replaced by a single element of each
    set. Compose with create_rdict to reverse a 1-1 dict.
    """
    nd = {}
    for (key, value) in d.items():
        nd[key] = value.pop()

    return nd

def create_rdict(d):
    """
    Return a dictionary with each key mapping to a set of values.
    """
    rd = {}
    for (key,value) in d.items():

        v = rd.setdefault(value, set([]))
        v.add(key)

    return rd

def create_cluster_colors(n):
    # create n distinct colors in rgb format

    colors = []
    for i in range(n):
        h = int( float(i) / float(n) *  360.0 )
        s = 50
        l = 50
        colors.append(ImageColor.getrgb("hsl(%d,%d%%,%d%%)" % (h,s,l)) )

    return colors

def create_cluster_colors_rgb(n):
    # create n distinct colors in rgb format

    colors = []
    for i in range(n):
        h = int( float(i) / float(n) *  360.0 )
        s = 50
        l = 50
        colors.append(np.array(ImageColor.getrgb("hsl(%d,%d%%,%d%%)" % (h,s,l))) / 255.0 )

    return colors

def clusters(f,fd):
    clusters = {}
    rclusters = {}

    for (label,point) in zip(f,fd):
        if clusters.has_key(label):
            clusters[label].append(point)
        else:
            clusters[label] = [point]
        rclusters[tuple(point)] = label

    return clusters, rclusters

def find_centers(f,fd):
    points = {}
    for (cluster, point) in zip(f,fd):
        if points.has_key(cluster):
            points[cluster].append(point)
        else:
            points[cluster] = [point]

    centers = {}
    for i,v in points.items():
        centers[i] = np.mean(np.array(v),axis=0)

    return centers


def count(l):
    # note that there is a stdlib counting module in later versions

    tmp = {}
    for i in l:
 	if tmp.has_key(i):
            tmp[i] += 1
 	else:
            tmp[i] = 1
    return tmp

def create_cluster_colors_hsl(n):
    colors = []
    for i in range(n):
        h = int( float(i) / float(n) *  360.0 )
        s = 50
        l = 50
        colors.append("hsl(%d,%d%%,%d%%)" % (h,s,l))

    return colors

def generate_gradient_img(name, size = 100):
    img = np.zeros((size,size))
    center = np.array([size / 2, size / 2])

    for i in range(size):
        for j in range(size):
            d = la.norm(np.array([i,j]) - center)
            img[i,j] = 255 - 2 * d

    print img
    scipy.misc.imsave(name, img)

class USet(set):
    """
    A set that always returns True for "in" style membership queries.
    """
    def __contains__(self, item):
        return True

def load_or_compute(self,items,methods,filename,recompute=False):

    try:
        if recompute: raise Exception
        fp = bz2.BZ2File(filename)
        for var in items:
            setattr(self, var, pickle.load(fp))
    except:
        if recompute is True:
            print "Recompute is True! Recomputing all data in file %s." % filename
        else:
            # extra debuggin code
            # exctype,value = sys.exc_info()[:2]
            # print exctype, value
            # traceback.print_tb(sys.exc_info()[2])
            print "Error reading file: %s. Recomputing all data."  % filename
        fp = bz2.BZ2File(filename,"w")
        for method in methods:
            getattr(self,method)()
        for var in items:
            pickle.dump(getattr(self,var) ,fp, pickle.HIGHEST_PROTOCOL)

    fp.close()

if __name__ == '__main__':
    #generate_gradient_img('../ds/simple.jpg')
    #colors = create_cluster_colors_rgb(8)
    #print colors

    avg = incavg()
    print avg.next()
    
    for i in range(1,10):
        print avg.send(i)


    # print avg.next()
    # print np.mean(range(10))
    # print dir(avg)

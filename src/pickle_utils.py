#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: PICKLE_UTILS.PY
Date: Friday, March 23 2012
Description: Utilities for using pickle.
"""

import cPickle as pickle
import bz2

def loaditer(fp):
    # a load iter
    while True:
        try:
            yield pickle.load(fp)
        except EOFError:
            raise StopIteration

def load_or_compute(method, filename, recompute=False):

    try:
        if recompute: raise Exception
        fp = bz2.BZ2File(filename)
        return pickle.load(fp)
        fp.close()

    except:
        if recompute is True:
            print "Recompute is True! Recomputing all data in file %s." % filename
        else:
            print "Error reading file: %s. Recomputing all data."  % filename

        fp = bz2.BZ2File(filename, "w")
        item = method()
        pickle.dump(item, fp, pickle.HIGHEST_PROTOCOL)
        fp.close()
        return item

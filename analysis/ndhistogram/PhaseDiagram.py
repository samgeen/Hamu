'''
Created on Nov 27, 2012

@author: samgeen
'''

import numpy as np

class PhaseDiagram(object):
    '''
    A phase diagram in temperature and density, with selectable weighting methods
    '''


    def __init__(self, snap, length=128):
        '''
        Constructor
        snap - Pymses RamsesOutput snapshot object
        length - Number of pixels in density and temperature space
        '''
        self._snap = snap
        self._length = length
    
    def Plot(self, weighting="mass"):
        '''
        Plot the phase diagram
        weighting - text string indication weighting technique
                    TODO: Make this an object instead?
        '''
        im = np.rand((self._length,self._length))
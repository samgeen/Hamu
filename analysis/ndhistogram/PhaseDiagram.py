'''
Created on Nov 27, 2012

@author: samgeen
'''

import numpy as np
import matplotlib.pyplot as plt
    

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
        self._rangeD = None
        self._rangeT = None
    
    def Plot(self, weightingType="mass",rangeT=None,rangeD=None):
        '''
        Plot the phase diagram
        weightingType - Text string indication weighting technique
        rangeT/D      - Temperature/Density ranges (default: choose extents
        '''
        im = np.random.rand((self._length,self._length))
        self._MakePlot(im,_MakeWeighting(weightingType))
        
    def _MakePlot(self,image,weighting):
        # Set up figure
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        # Plot the image
        vmin = np.min(image)
        vmax = np.max(image)
        cax = ax.imshow(image, interpolation='nearest',vmin=vmin,vmax=vmax)
        # Add colour bar
        cbar = fig.colorbar(cax)
        cbar.set_label("Density / atoms/cm$^{3}$")
        plt.savefig("test"+".pdf",format="pdf")
        

def _SetupWeightings():
    '''
    Set up the possible weightings
    '''
    ws = dict()
    ws["mass"] = None # TODO: THIS!!!!
    return ws

weightingTechniques = _SetupWeightings()

def _MakeWeighting(label):
    '''
    Weighting technique factory method 
    '''
    return weightingTechniques[label] 
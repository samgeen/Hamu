'''
Created on Nov 27, 2012

@author: samgeen
'''

import numpy as np
import matplotlib.pyplot as plt

from HistoWeighting import SimpleWeighter, MassWeighter


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
        self._weighter = None
    
    def Plot(self, weightingType=SimpleWeighter(),rangeT=None,rangeD=None):
        '''
        Plot the phase diagram
        weightingType - Text string indication weighting technique
        rangeT/D      - Temperature/Density ranges (default: choose extents from data)
        '''
        self._rangeD = rangeD
        self._rangeT = rangeT
        # If the weightingType is a string, parse it into a dictionary object
        if type(weightingType)==type("THIS IS A STRING"):
            self._weighter = _MakeWeighting(weightingType)
        else:
            self._weighter = weightingType
        im = self._MakeHisto()
        self._MakePlot(im)
    
    def _MakeHisto(self):
        im = np.zeros((self._length,self._length))
        # Set up temperature, density and weightings
        dataT = np.log10(self._weighter.Temperature(self._snap))
        dataD = np.log10(self._weighter.Density(self._snap))
        vW = self._weighter.Weighting(self._snap)
        # Find the ranges in T and D
        rT = [np.min(dataT),np.max(dataT)]
        rD = [np.min(dataD),np.max(dataD)]
        self._rangeT = rT
        self._rangeD = rD
        # Find the data coords in T and D
        # The 0.99999 makes sure that the values don't overflow the image array bounds
        cT = (dataT - rT[0]) / (rT[1]-rT[0]) * self._length * 0.99999
        cD = (dataD - rD[0]) / (rD[1]-rD[0]) * self._length * 0.99999
        for t,d,w in zip(cT,cD,vW):
            im[int(d),int(t)]+=w
        return im
        
    def _MakePlot(self,image):
        # Set up figure
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        # Set the image extents in phase-space
        ax.set_xlim(self._rangeD)
        ax.set_ylim(self._rangeT)
        axes=[self._rangeD[0],self._rangeD[1],self._rangeT[0],self._rangeT[1]]
        aspect = (axes[1] - axes[0]) / (axes[3] - axes[2])
        # Plot the image
        image[np.where(image == 0)] = np.min(image[np.nonzero(image)])
        image = np.log10(image/np.sum(image)*100.0)
        vmin = np.min(image)
        vmax = np.max(image)
        cax = ax.imshow(image, interpolation='nearest',extent=axes,vmin=vmin,vmax=vmax,aspect=aspect)
        # Set axis labels
        ax.set_xlabel("log(n_{H} / atoms.cm$^{-3}$)")
        ax.set_ylabel("log(Temperature / K)")
        # Add colour bar
        cbar = fig.colorbar(cax)
        cbar.set_label("log(% "+self._weighter.Label()+")")
        plt.savefig("test"+self._weighter.Name()+".pdf",format="pdf")

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

if __name__=="__main__":
    p = PhaseDiagram(None)
    p.Plot(SimpleWeighter())
    p = PhaseDiagram(None)
    p.Plot(MassWeighter())
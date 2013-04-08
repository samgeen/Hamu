'''
Created on Nov 27, 2012

@author: samgeen
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import pymses
import Hamu

from HistoWeighting import SimpleWeighter, MassWeighter, KEWeighter, VolumeWeighter

def _SetupWeightings():
    '''
    Set up the possible weightings
    '''
    ws = dict()
    ws["count"] = SimpleWeighter()
    ws["mass"] = MassWeighter()
    ws["ke"] = KEWeighter()
    ws["volume"] = VolumeWeighter()
    return ws

def _MakeWeighting(label):
    '''
    Weighting technique factory method 
    '''
    return _SetupWeightings()[label]

def MakeHisto(snap, length, weighterName, rT, rD):
    '''
    Make the histogram image array
    (Made separate from PhaseDiagram to make Hamu implementation easier to understand)
    '''
    weighter = _MakeWeighting(weighterName)
    im = np.zeros((length,length))
    # Set up temperature, density and weightings
    dataT = np.log10(weighter.Temperature(snap))
    dataD = np.log10(weighter.Density(snap))
    weightings = weighter.Weighting(snap)
    # Find the ranges in T and D
    if not rT:
        rT = [np.min(dataT),np.max(dataT)]
    if not rD:
        rD = [np.min(dataD),np.max(dataD)]
    # Find the data coords in T and D
    # The 0.99999 makes sure that the values don't overflow the image array bounds
    print dataT.shape
    cT = (dataT - rT[0]) / (rT[1]-rT[0]) * length * 0.99999
    cD = (dataD - rD[0]) / (rD[1]-rD[0]) * length * 0.99999

    # Cull values that lie outside the data range
    im = np.histogram2d(dataT,dataD,(length,length),\
                           range=[rT,rD],weights=weightings)

    # Flip image to match plotting
    #im = np.fliplr(im)

    '''
    for t,d,w in zip(cT,cD,weightings):
        # NOTE1 - NUMPY ARRAYS SEEM TO DO COLUMN THEN ROW, SO Y = 1ST ELEMENT, X = 2ND
        # NOTE2 - IMAGES SEEM TO HAVE ZERO AT THE TOP, RATHER THAN THE BOTTOM, SO T NEEDS FLIPPING
        
        #im[length-int(t)-1,int(d)]+=w 
        t = length-int(t)-1
        d = int(d)
        #if t >= 0 and t < length and d >= 0 and d < length:
        im[t,d]+=w 
    '''
    return (rD, rT, im)

class PhaseDiagram(object):
    '''
    A phase diagram in temperature and density, with selectable weighting methods
    '''

    def __init__(self, snap, length=128,rangeT=None,rangeD=None):
        '''
        Constructor
        snap - Hamu snapshot object
        length - Number of pixels in density and temperature space
        rangeT/D - Temperature/Density ranges 
                   (default: choose extents from data)
       '''
        self._snap = snap
        self._length = length
        self._rangeT = rangeT
        self._rangeD = rangeD
        self._weighter = None
    
    def PlotPhase(self, weightingType=SimpleWeighter()):
        '''
        Plot the phase diagram
        weightingType - Text string indicating weighting technique
         '''
        # If the weightingType is a string, parse it into a dictionary object
        if type(weightingType)==type("THIS IS A STRING"):
            self._weighter = _MakeWeighting(weightingType)
        else:
            self._weighter = weightingType
        
        # Set up file name
        os.system("mkdir phases")
        outnum = '%(num)05d' % {'num': self._snap.OutputNumber()}
        fileout = "plots/phases/phase"+self._weighter.Name()+outnum+".pdf"
        # Only run if the file doesn't already exist
        MakeHistoPlot = Hamu.Algorithm(MakeHisto)
        self._rangeD, self._rangeT, im = MakeHistoPlot(self._snap, self._length, self._weighter.Name(), self._rangeT, self._rangeD)
        im, blah, blah = im # since np.histogram2d returns a tuple
        im = np.flipud(im)
        self._MakePlot(im, fileout)
    
    def _MakePlot(self,image,fileout):
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
        ax.set_xlabel("log(n$_{H}$ / atoms.cm$^{-3}$)")
        ax.set_ylabel("log(Temperature / K)")
        # Add colour bar
        cbar = fig.colorbar(cax)
        cbar.set_label("log(% "+self._weighter.Label()+")")
        plt.savefig(fileout,format="pdf")

if __name__=="__main__":
    loc = "./"
    sim = Hamu.Simulation(loc)
    for out in sim.Outputs():
        if out > 1:
            print out
            snap = pymses.RamsesOutput(loc,out)
            p = PhaseDiagram(snap)
            #p.Plot(SimpleWeighter())
            p.Plot(MassWeighter())
            p.Plot(VolumeWeighter())
            p.Plot(KEWeighter())
    print "Done!"

'''
Created on 18 Feb 2013

@author: samgeen
'''

import abc

import Settings
from Hamu.Utils.Directory import Directory
from HamuIterable import HamuIterable

# NOTE: THIS IS AN ABSTRACT CLASS; YOU CAN'T INSTANTIATE IT
#       CHECK THE Codes FOLDER FOR CONCRETE CLASSES OF THIS TYPE

class Snapshot(HamuIterable):
    '''
    A simulation snapshot/output at a given time
    Abstract class providing an interface for different simulation analysis codes to implement
    See, e.g. http://pymotw.com/2/abc/ for a description of how Python's abc module works
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        # NOTE: THIS IS A DEFAULT VALUE; SHOULD BE PUT INSIDE A SIMULATION
        #dir = Directory(Settings.Settings()["DataDir"]+"/Default/")
        self._cachepath = None# dir.Path()
    
    ### GENERIC SNAPSHOT METHODS TO BE IMPLEMENTED BY ANALYSIC CODE INTERFACES ###
        
    @abc.abstractmethod
    def RawData(self):
        '''
        Return the raw simulation data container
        This is usually a snapshot/output object in the given code's native analysis code
        '''
        return
    
    @abc.abstractmethod
    def OutputNumber(self):
        '''
        Return the output number
        '''
        return
    
    @abc.abstractmethod
    def Time(self):
        '''
        Return the output time (for comparing outputs)
        TODO: Make this concept more concrete (i.e. make sure units/measurement methods match)
        '''
        return
    
    @abc.abstractmethod
    def Path(self):
        '''
        Return the folder/file path for the raw snapshot data
        '''
        return
    
    ### HAMU FUNCTIONS FOR DATA CACHING AND PROCESSING ###
    
    def Snapshots(self):
        '''
        Return all the snapshots in this collection
        PATHOLOGICAL CASE - ALLOWS ALGORITHMS TO INPUT ANY HamuIterable OBJECT
        '''
        return [self]
    
    def CachePath(self):
        '''
        Return the location of the cache path for Hamu data
        '''
        if not self._cachepath:
            print "Cache path not set in output", self._outnum
            raise ValueError
        return self._cachepath
    
    def SetupCache(self, simCachePath):
        '''
        Runs when the snapshot is added to a Simulation object
        simCachePath - path of cached data for the Simulation object
        '''
        self._cachepath = Directory(simCachePath+"/snap"+str(self.OutputNumber())+"/").Path()
        
        

'''
Created on 15 Feb 2013

@author: samgeen
'''

import os, re, collections, importlib
import cPickle as pik

from Utils.Directory import Directory
import Settings
import Simulations
import HamuIterable

class Simulation(HamuIterable.HamuIterable):
    '''
    A simulation object; stores snapshots
    NOTE: CURRENTLY IT DOES NOT SAVE SNAPSHOTS - INSTEAD, IT RE-LOADS THEM EVERY TIME THE SIMULATION IS INSTANTIATED
          DO WE WANT A MORE NUANCED APPROACH TO THIS - E.G. IF SNAPSHOTS ARE DELETED BUT WE STILL WANT TO ANALYSE THE DATA?
    '''

    def __init__(self,name,path=None,codeModule=None):
        '''
        Constructor
        name: Name of the simulation (to be used to refer to the simulation from here on)
        path: Path of raw simulation data - NOTE: MUST BE INCLUDED THE FIRST TIME A SIMULATION IS USED BY HAMU
        codeModule: Python module used to generate simulation data for a given code - NOTE: AS ABOVE
        '''
        self._name = name
        self._path = path
        self._codeModule = codeModule
        self._cachedir = None
        self._snapshots = collections.OrderedDict()
        self._Setup()
        
    def Name(self):
        '''
        Returns the name of the simulation
        '''
        return self._name
    
    def Path(self):
        '''
        Returns the path of the raw simulation data
        '''
        return self._path
    
    def CodeModule(self):
        '''
        Returns the code module used to generate the raw simulation data
        '''
        return self._codeModule
    
    def Snapshot(self, outputNumber):
        '''
        Returns a snapshot with a given output number
        '''
        return self._snapshots[outputNumber]
    
    def Snapshots(self):
        '''
        Returns a list of all snapshots in the simulation
        '''
        return self._snapshots.values() # Note: values() gets a list from the OrderedDict
    
    def _Setup(self):
        '''
        Runs when the object is created
        '''
        sims = Simulations.Simulations()
        # Check to see if the simulation exists
        if not sims.Exists(self._name):
            # Create it!
            # First, check that we've been given enough data to work with
            if not self._codeModule or not self._path:
                print "Error: No code/path inputted into non-existent simulation with name", self._name
                print "       Current workspace:", Settings.Settings()["CurrentWorkspace"]
                raise ValueError
            # Add self to list of cached simulations
            self._cachedir = sims.AddSimulation(self)
        else:
            # Load the simulation cache data
            self._cachedir = sims.CachePath(self.Name())
            self._Load()
        # Locate all the snapshots in the raw data folder
        self._UpdateSnapshots()
        self._Save()
                
            
    def _UpdateSnapshots(self):
        '''
        Find the snapshots inside the raw data folder and update the snapshots list
        '''
        stub = self._codeModule.OutputStub(self._path)
        items = Directory(self._path).ListItems()
        self._snapshots.clear()
        for item in items:
            # Does the item match an output?
            if stub in item:
                # Strip out the item's digits and find the output number
                num = int(re.sub("\D", "", item))
                snap = self._codeModule.MakeSnapshot(self._path,num)
                snap.SetupCache(self._cachedir)
                # Add the snapshot to the array
                self._snapshots[num] = snap
                
    def _Save(self):
        '''
        Save the data to a pickle file
        '''
        filename = self._CacheFilename()
        pikfile = open(filename,"wb")
        pik.dump(self._name,pikfile)
        pik.dump(self._path,pikfile)
        pik.dump(self._codeModule.__name__,pikfile)
        pik.dump(self._cachedir,pikfile)
        #pik.dump(self._snapshots,pikfile)
        pikfile.close()
        
    def _Load(self):
        '''
        Load the data from the pickle file
        '''
        filename = self._CacheFilename()
        if os.path.exists(filename):
            pikfile = open(filename,"rb")
            self._name = pik.load(pikfile)
            self._path = pik.load(pikfile)
            codeModuleName = pik.load(pikfile)
            self._cachedir = pik.load(pikfile)
            #self._snapshots = pik.load(pikfile)
            pikfile.close()
            self._codeModule = importlib.import_module(codeModuleName)
            
    def _CacheFilename(self):
        '''
        Returns the name of the cache file
        '''
        return self._cachedir+"Simulation"+self._name+".cache"
            
            
        
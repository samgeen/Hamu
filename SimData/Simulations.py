'''
Created on 19 Feb 2013

@author: samgeen
'''

import Simulation
import Settings
from Hamu.Utils.Directory import Directory

class Simulations(object):
    '''
    A class that manages simulations with cached data
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # Set up directory to use for simulations
        self._dir = Directory(Settings.Settings()["DataDir"]+"/Simulations/")
        # Open list of simulations
        self._simNames = self._dir.ListItems()
        
    def Exists(self, name):
        '''
        Does a simulation with this name exist?
        '''
        return name in self._simNames
    
    def CachePath(self, simName=None):
        '''
        Path that the simulation cache data is stored in
        simName: If set, return the path of that simulation's cache folder
        '''
        path =  self._dir.Path()
        if simName:
            path+=simName+"/"
        return path
        
    def AddSimulation(self, sim):
        '''
        Add this simulation to the list of simulations
        '''
        name = sim.Name()
        # Make the simulation directory
        cachedir = self._dir.MakeSubdir(name)
        # Add simulation to list of simulations
        self._simNames.append(name)
        return cachedir.Path()

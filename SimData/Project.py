'''
Created on 19 Feb 2013

@author: samgeen
'''

import os
import cPickle as pik

import Settings
import Workspace
import Simulation
import Simulations
import HamuIterable
from Hamu.Utils.Directory import Directory



def __call__(name):
    '''
    Convenience factory method; allows users to call the module to instantiate a new object
    '''
    return Project(name)

class Project(HamuIterable.HamuIterable):
    '''
    A Hamu project; contains multiple simulations
    Note: different projects can contain the same simulations
    '''

    def __init__(self,name):
        '''
        Constructor
        name: Name of the project
        '''
        #HamuIterable.HamuIterable.__init__()
        self._name = name
        self._simnames = list()
        # Open workspace
        wsname = Settings.Settings()["CurrentWorkspace"]
        wspath = Settings.Settings()["WorkspacePath"]
        #self._workspace = Workspace.Workspace(wsname)
        # Set up project
        self._dir = Directory(wspath+"/"+self._name+"/")
        # Load simulation names if a save file already exists
        self._Load()
        
    def Name(self):
        '''
        Returns the project's name
        '''
        return self._name
        
    def Simulation(self, name, path=None, codeModule=None):
        '''
        Return the simulation with a given name in the project
        TODO: BETTER TO SAVE LIST OF SIMULATION OBJECTS INSIDE CLASS INSTEAD TO SAVE TIME?
        '''
        return Simulation.Simulation(name, path, codeModule)
        
    def SimNames(self):
        '''
        Return a list of simulation *names* in the project
        '''
        return self._simnames

    def Simulations(self):
        '''
        Return a list of simulations in the project
        TODO: BETTER TO SAVE LIST OF SIMULATION OBJECTS INSIDE CLASS INSTEAD TO SAVE TIME?
        '''
        sims = list()
        for name in self._simnames:
            sims.append(Simulation.Simulation(name))
        return sims
        
    def Snapshots(self):
        '''
        Return a list of all the snapshots in the project
        '''
        snaps = list()
        for sim in self.Simulations():
            snaps += sim.Snapshots()
        return snaps
        
    def Add(self, simulation):
        '''
        Add a simulation to the project
        simulation: Can be either a Simulation object or a string containing a simulation name
        '''
        # Find the name of the simulation (depending on whether we're inputting the name or the simulation)
        name = None
        if type(simulation) != type(""):
            name = simulation.Name()
        else:
            name = simulation
        # Add simulation to the project (NOTE: ONLY SAVES THE NAMES)
        if not name in self._simnames:
            self._simnames.append(name)
        # Save the simulations already in the project
        self._Save()
        
    def Remove(self, simulation):
        '''
        Remove a simulation from the project
        simulation: Can be either a Simulation object or a string containing a simulation name
        '''
        # Find the name of the simulation (depending on whether we're inputting the name or the simulation)
        name = None
        if type(simulation) != type(""):
            name = simulation.Name()
        else:
            name = simulation
        # Add simulation to the project (NOTE: ONLY SAVES THE NAMES)
        if name in self._simnames:
            self._simnames.remove(name)
        # Save the simulations already in the project
        self._Save()

    def _CacheFilename(self):
        return self._dir.Path()+"Project"+self._name+".cache"
        
    def _Save(self):
        '''
        Save the project data to cache
        '''
        filename = self._CacheFilename()
        pikfile = open(filename,"wb")
        pik.dump(self._simnames,pikfile)
        pikfile.close()
        
    def _Load(self):
        '''
        Load the project data from cache
        '''
        filename = self._CacheFilename()
        if os.path.exists(filename):
            pikfile = open(filename,"rb")
            self._simnames = pik.load(pikfile)
            pikfile.close()

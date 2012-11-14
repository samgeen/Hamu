'''
Created on 2 Mar 2012

@author: samgeen
'''

from Simulation import Simulation
#from Hamu.Utils.Directory import Directory

# A suite of simulations
class Suite(object):

    # workingDirectory: Place where the data produced by Hamu is stored
    def __init__(self, workingDirectory):
        self._dir = workingDirectory
        self._simulations = dict()

    def __iter__(self):
        return self._simulations.itervalues()
    
    def iteritems(self):
        return self._simulations.iteritems()
        
    # name: Name given by user to label this suite
    # folder: Folder where simulation resides
    def MakeSimulation(self, name, folder):
        # Make the suite's save location
        self._simulations[name] = Simulation(folder)
        
    # [ ] OPERATORS : USED TO GET/SET SIMULATIONS IN THE SUITE
    # TODO: USE A FACTORY METHOD INSTEAD???
    # name: Name given by user to label this suite
    def __setitem__(self,name, sim):
        # Make the suite's save location
        self._simulations[name] = sim
            
    # name: Name given by user to label this suite 
    def __getitem__(self,name):
        # Make the suite's save location
        return self._simulations[name]
    
    # Returns a dictionary of snapshots for each simulation with the outputs nearest to time
    # TODO: Add errors to interface
    # time: time in code units
    def FindTime(self, time):
        outs = dict()
        for name, sim in self.iteritems():
            snap = sim.FindAtTime(time)
            outs[name] = snap
        return outs
            

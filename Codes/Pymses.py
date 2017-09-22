'''
Created on 20 Feb 2013

@author: samgeen

Functions and classes that implement Hamu for Ramses data
'''

import os, sys, StringIO, Hamu
import Hamu.SimData.Snapshot as Snapshot
import Hamu.SimData.Workspace as Workspace
import Hamu.SimData.Algorithm as Algorithm

import pymses

# This is to deal with the fact that loading a snapshot in 
#    Pymses 4.0 is slow, so FindAtTime is very slow
def _PymsesCacheTimeHamu(snap):
    return snap.info["time"]
CacheTime = Hamu.Algorithm(_PymsesCacheTimeHamu)

def MakeSimulation(name, folder=os.getcwd(),workspace=None):
    # Set the workspace if necessary
    if workspace:
        Workspace.Workspace(workspace)
    return Hamu.Simulation(name,folder,sys.modules[__name__],forceSetup=True)

def MakeSnapshot(folder, outputNumber):
    '''
    This function returns a snapshot object in a given folder with a given number
    '''
    return PymsesSnapshot(folder,outputNumber)
    
def OutputStub(folder):
    '''
    Returns a string that can be used to search for all snapshots/outputs in a folder
    e.g. "output_", "snapshot", etc
    This allows Hamu to search the data folder for outputs and create a list of snapshots to cycle through
    Inputs:
    folder - Name of folder inputted (can be useful for some multi-code analysis tools, such as yt)
    
    TODO: IF THIS FUNCTION IS ABSENT IN SOME CODES, BEST-GUESS WHAT THE OUTPUT STUB IS AND WARN THE USER ABOUT THIS
    '''
    return "output_"

class PymsesSnapshot(Snapshot.Snapshot):
    def __init__(self, folder, outputNumber):
        Snapshot.Snapshot.__init__(self)
        '''
        folder: The folder containing the data
        output: The number of the snapshot/output
        '''
        # Note: DO NOT REFER TO _snapshotPYMSES; USE _snapshot !!!
        self._folder = folder
        self._outputNumber = outputNumber
        self._snapshotPYMSES = None
        self._setup = False

    @property
    def _snapshot(self):
        '''
        Return the snapshot object - allows us to 
        '''
        # THIS STOPS THE ANNOYING PRINT STATEMENTS IN THE PYMSES.RAMSESOUTPUT CONSTRUCTOR
        if not self._setup:
            # Run constructor
            #actualstdout = sys.stdout
            #sys.stdout = StringIO.StringIO()
            try:
                self._snapshotPYMSES = pymses.RamsesOutput(self._folder,self._outputNumber)
            except KeyError:
                print "Key Error loading snapshot! Folder, output number:", self._folder,self._outputNumber
                import pdb; pdb.set_trace()
            # Add self to this object to allow tracking back up 
            #   and using Algorithm
            self._snapshotPYMSES.hamusnap = self
            # Reset stdout
            #sys.stdout = actualstdout   
            # Done!
            self._setup = True
        return self._snapshotPYMSES

    # ### IMPLEMENTATION OF ABSTRACT FUNCTIONS FOUND IN Snapshot ###
        
    def RawData(self):
        '''
        Return the raw simulation data container
        This is usually a snapshot/output object in the given code's native analysis code
        '''
        return self._snapshot
    
    def OutputNumber(self):
        '''
        Return the output number
        '''
        return self._outputNumber #self._snapshot.iout
    
    def Time(self):
        '''
        Return the output time (for comparing outputs)
        TODO: Make this concept more concrete (i.e. make sure units/measurement methods match)
        '''
        # 
        return CacheTime(self) #self._snapshot.info["time"]
    
    def Path(self):
        '''
        Return the folder/file path for the raw snapshot data
        '''
        return self._folder # self._snapshot.output_repos
        
    

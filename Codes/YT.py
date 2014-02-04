'''
Created on 20 Feb 2013

@author: samgeen

Functions and classes that implement Hamu for YT snapshots
NOTE: FUNCTION OutputStub ONLY WORKS WITH RAMSES OUTPUTS SO FAR!!!
'''

import yt.mods, os, sys, StringIO, Hamu
import Hamu.SimData.Snapshot as Snapshot

def MakeSimulation(name, folder=os.getcwd()):
    return Hamu.Simulation(name,folder,sys.modules[__name__])

def MakeSnapshot(folder, outputNumber):
    '''
    This function returns a snapshot object in a given folder with a given number
    '''
    print "WARNING: Only works with RAMSES in current version!"
    print "         Requires file discovery to be more generic for other codes"
    return YTSnapshot(folder,outputNumber)
    
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

class YTSnapshot(Snapshot.Snapshot):
    def __init__(self, folder, outputNumber):
        Snapshot.Snapshot.__init__(self)
        '''
        folder: The folder containing the data
        output: The number of the snapshot/output
        '''
        # THIS STOPS THE ANNOYING PRINT STATEMENTS IN THE PYMSES.RAMSESOUTPUT CONSTRUCTOR
        actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        # Run constructor
        # HACK - ONLY WORKS FOR RAMSES OUTPUTS!!
        ramnum = str(outputNumber).zfill(5)
        ramname = folder+"/output_"+ramnum+"/info_"+ramnum+".txt"
        self._snapshot = yt.mods.load(ramname)
        # Reset stdout
        sys.stdout = actualstdout        
        # Add self to this object to allow tracking back up and using Algorithm 
        self._snapshot.hamusnap = self


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
        # HACK - MAY ONLY WORK WITH RAMSES
        return int(self._snapshot.directory[-5:])
    
    def Time(self):
        '''
        Return the output time (for comparing outputs)
        TODO: Make this concept more concrete (i.e. make sure units/measurement methods match)
        '''
        return self._snapshot.current_time
    
    def Path(self):
        '''
        Return the folder/file path for the raw snapshot data
        '''
        return self._snapshot.fullpath+"/"
        
    

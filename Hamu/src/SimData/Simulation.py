# A simulation class, used to iterate through outputs
# Sam Geen, March 2012

import numpy as np
import subprocess
import pymses
import os

# Very simple factory method
def Make(name,location=""):
    return Simulation(name,location)

# Simulation class
class Simulation(object):
    def __init__(self,name,location="."):
        self._name = name
        self._location = location
        self._outputs = list()
        self._snapshots = dict()
        self._times = list()
        self._itercount = -1
        self._prepared = False

    # Simulation location
    def Location(self):
        return self._location
    
    # Simulation name
    def Name(self):
        return self._name
    
    # outputNumber: integer output number
    def __getitem__(self, outputNumber):
        self._Prepare()
        # Find the output number by key
        # TODO: Add exceptions if the output number given is bad?
        return self._snapshots[outputNumber]

    # Return list of outputs
    def Outputs(self):
        self._Prepare()
        return self._outputs
    
    # Return the list of output times
    def Times(self):
        self._Prepare()
        return self._times

    # Iterator stuff
    def __iter__(self):
        self._itercount = -1
        self._Prepare() 
        return self 

    def next(self):
        self._itercount += 1
        if self._itercount == len(self._outputs):
            raise StopIteration
        # This is a little convoluted, but it keeps outputs in order.
        return self._snapshots[self._outputs[self._itercount]]
    
    # Find a snapshot at a given time
    # TODO: Refactor a bit, this code works but is a bit messy
    # TODO: Pass out the % error somehow as something other than text
    def FindAtTime(self, time):
        self._Prepare()
        # Find the snapshot time with the minimum difference to the required time
        times = np.array(self._times)
        diff = np.abs(times - time)
        best = np.where(diff == np.min(diff))
        best = self._outputs[best[0][0]]
        pdiff = (times[best-1]-time) / time * 100.0
        snap = self._snapshots[best]
        print "Found match with output",best,", %diff: ",pdiff, "at time ",times[best-1]
        return snap
    
    # PROTECTED AUXILIARY METHODS

    # Locate all the outputs, general simulatin preparation
    def _Prepare(self):
        if not self._prepared:
            print "Preparing simulation for reading... ",
            # Run through all the outputs
            self._outputs = list()
            for nout in self._FindOutNums():
                snap = pymses.RamsesOutput(self._location, nout)
                # Add to the containers
                self._outputs.append(nout)
                self._times.append(snap.info["time"])
                self._snapshots[nout] = snap
            print "Done!"
            self._prepared = True

    # Find a list of output folders in the simulation folder
    def _FindOutNums(self):
        # Find a list of outputs as a text list
        outs = subprocess.check_output("ls -d "+self.Location()+"/output_*",shell=True)
        # Process the list into a set of output numbers
        nums = list()
        outs = outs.split("\n")
        for out in outs:
            if len(out) > 0:
                # This finds the last 5 characters (the output number) and casts them to an int
                nums.append( int(out[len(out)-5:]) )
        # Sort the array and return the results
        nums = sorted(nums)
        return nums

    # Output folder name from output number  
    def _Outfolder(self, nout):
        outstr = '%(num)05d' % {'num': nout}
        return self.Location()+"/output_"+outstr



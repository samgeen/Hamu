# A simulation class, used to iterate through outputs
# Sam Geen, March 2012

import pymses
import os

# Factory method
def Make(location=""):
    return Simulation(location)

# Simulation class
class Simulation(object):
    def __init__(self,location=""):
        self._location = location
        self._outputs = list()
        self._snapshots = list()
        self._itercount = -1

    # Return list of outputs
    def Outputs(self):
        self._Prepare()
        return self._outputs

    # Iterator stuff
    def __iter__(self):
        self._itercount = -1
        self._Prepare() 
        return self 

    def next(self):
        self._itercount += 1
        if self._itercount == len(self._outputs):
            raise StopIteration
        return self._snapshots[self._itercount]
    
    # PROTECTED AUXILIARY METHODS

    # Locate all the outputs, general simulatin preparation
    def _Prepare(self):
        print "Preparing simulation for reading... ",
        # Run through all the outputs
        nout = 1
        self._outputs = list()
        while os.path.isdir(self._Outfolder(nout)):
            self._outputs.append(nout)
            self._snapshots.append(pymses.RamsesOutput(self._location, nout))
            nout += 1
        print "Done!"

    # Output folder name from output number  
    def _Outfolder(self, nout):
        outstr = '%(num)05d' % {'num': nout}
        return "output_"+outstr



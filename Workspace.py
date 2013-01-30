'''
Created on 2 Mar 2012

@author: samgeen
'''

# TODO: CREATE ".Hamu" FOLDER TO ACT AS CACHE STORAGE

from SimData.Suite import Suite
from Utils.Directory import Directory

# Top level object; stores suites and a list of algorithms
class Workspace(object):
    
    # workingDirectory: Place where the data produced by Hamu is stored
    def __init__(self, workingDirectory):
        self._suites = dict()
        self._dir = workingDirectory
        
    # name: Name given by user to label this suite
    def MakeSuite(self,name):
        # Make the suite's save location
        folder = Directory((self._dir,name))
        self._suites[name] = Suite(folder)
        return self._suites[name]
            
    # name: Name given by user to label this suite 
    def FindSuite(self,name):
        # Make the suite's save location
        return self._suites[name]
    
if __name__=="__main__":
    workspace = Workspace(".")
        

'''
Created on 2 Mar 2012

@author: samgeen
'''

import os, sys

#import setup

import Settings
import Project
from Hamu.Utils.Directory import Directory

def __call__(name):
    '''
    Convenience factory method; allows users to call the module to instantiate a new object
    '''
    return Workspace(name)

# Top level object; stores suites and a list of algorithms
class Workspace(object):
    
    # Name: Workspace name
    def __init__(self, name):
        self._projects = dict()
        self._name = name
        # Set up the workspace
        self._Setup()
        
    # Return the working directory
    def Directory(self):
        return self._dir
        
    # name: Name given by user to label this suite
    def Project(self,name):
        # Make the suite's save location
        if not name in self._projects:
            folder = Directory(self._dir.Path()+name)
            self._projects[name] = Project.Project(name)
        return self._projects[name]
            
    # name: Name given by user to label this suite 
    #def FindSuite(self,name):
    #    # Make the suite's save location
    #    return self._suites[name]
    
    def _Setup(self):
        '''
        Set up the workspace
        '''
        settings = Settings.Settings()
        home = settings["DataDir"]
        path = home+"workspaces/"+self._name+"/"
        # Make a directory with this workspace in it
        self._dir = Directory(path)
        # Set the current workspace to this one
        settings["CurrentWorkspace"] = self._name
        settings["WorkspacePath"] = self._dir.Path()
        print "Current workspace set to", self._name
        print "Workspace data written to", self._dir.Path()
        # Find the projects in this workspace
        projects = self._dir.ListItems()
        for project in projects:
            self._projects[project] = Project.Project(project)
    
if __name__=="__main__":
    workspace = Workspace(".")
    

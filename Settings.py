'''
Created on 13 Feb 2013

@author: samgeen
'''

import os
import cPickle as pik

from Utils.Directory import Directory
import SimData.Workspace as Workspace

HOMEPATH = os.getenv("HOME")+"/.hamu/"

class Settings(object):
    '''
    Settings class; uses the $HOME/.hamu folder to synchronise the settings with what's on the HDD
    NOTE: IF PARALLELISING, REFACTOR THIS SO THAT IT LOCKS THE FILE ACCESS PROPERLY
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._filename = HOMEPATH+"settings.pik"
        self._settings = dict()
        # Check to see if the settings exist, and if not, set them up
        if not os.path.exists(self._filename):
            self._Setup()
    
    def __setitem__(self, item, value):
        '''
        Set an item in the global settings
        '''
        self._LoadSettings()
        self._settings[item] = value
        self._SaveSettings()
        
    def __getitem__(self, item):
        '''
        Get an item in the global settings
        '''
        self._LoadSettings()
        return self._settings[item]
    
    def _LoadSettings(self):
        '''
        Load the settings
        '''
        if os.path.exists(self._filename):
            pikfile = open(self._filename,"rb")
            self._settings = pik.load(pikfile)
            pikfile.close()
        
    def _SaveSettings(self):
        '''
        Save the settings
        '''
        pikfile = open(self._filename,"wb")
        pik.dump(self._settings,pikfile)
        pikfile.close()
        
    def _Setup(self):
        print '''
        Welcome to
        
          /\  /\__ _ _ __ ___  _   _ 
         / /_/ / _` | '_ ` _ \| | | |
        / __  / (_| | | | | | | |_| |
        \/ /_/ \__,_|_| |_| |_|\__,_|
        
        Helping your simulations to hug and make up
        Written by Sam Geen, 2013
        
        For use as-is; no responsibility accepted for damage to your computer, person or family pets
        ---------------------------------------------------------------------------------------------------
        Now setting up the work environment...
        '''
        print "Installing Hamu by default to",HOMEPATH
        dir = Directory(HOMEPATH)
        self["DataDir"] = dir.Path()
        wsname = "MyWorkspace"
        # Set up workspace with this name
        Workspace.Workspace(wsname)
        print "You're good to go!"
        
'''
Created on Dec 5, 2012

@author: samgeen
'''

#import analysis
#import SimData
#import figures
import Utils
# HAMU SIMULATION MANAGEMENT AND DATA CACHING IMPORTS
from SimData.Algorithm import Algorithm
from SimData.Project import Project
from SimData.Simulation import Simulation
from SimData.Snapshot import Snapshot
from SimData.Workspace import Workspace
from SimData.MakeSim import MakePymses
# CONVENIENCE IMPORTS; BRINGS SLICES AND PROFILES UP THE CHAIN OF MODULES
#from analysis.visualisation import slices
#from analysis.profiles import profiles

def ListSimulations():
    '''
    Print a list of all simulation names in the current workspace
    '''
    import os
    import SimData.Simulations
    sims = SimData.Simulations.Simulations()
    path = sims.CachePath()
    os.system("ls "+path)

def CurrentWorkspace():
    '''
    Return the current workspace's name
    '''
    return SimData.Settings.Settings()["CurrentWorkspace"]

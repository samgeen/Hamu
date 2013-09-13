'''
Created on 06 Sept 2013

@author: samgeen
'''

import os
import Simulation

def MakePymses(simname):
    '''
    Make a Pymses simulation
    This uses the current working directory 
    simname - The simulation name to use
    '''
    from Hamu.Codes import Pymses
    cwd = os.getcwd()
    sim = Simulation.Simulation(simname,cwd,Pymses)
    return sim

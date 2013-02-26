'''
Created on 14 Feb 2013

@author: samgeen

An example script
'''

import Codes.Pymses as Pymses
from SimData.Workspace import Workspace
from SimData.Project import Project
from SimData.Algorithm import Algorithm
from SimData.Simulation import Simulation

def TestFunc(snap):
    return snap.output_repos, snap.iout

if __name__ == '__main__':
    workspace = Workspace("ExampleWorkspace")
    # Load a project from the current workspace, ExampleWorkspace
    # NOTE: You can also call project = workspace.Project("ExampleProject")
    project = Project("ExampleProject")
    # Open a simulation
    simpath = "/data/Simulations/Disk/Runs/lvl7"
    sim = Simulation("TestSimulation",simpath, Pymses)
    # Add the simulation to the 
    project.AddSimulation(sim)
    # Find a snapshot and print its output number
    snap = sim.Snapshot(6)
    print "Sample output number: ", snap.OutputNumber()
    
    # Run a simple test function on all snapshots in the project
    # NOTE: THIS FUNCTION IS NATIVE TO THE GIVEN CODE (IN THIS CASE, PYMSES)
    func = Algorithm(TestFunc)
    for snap in project.Snapshots():
        print func(snap)
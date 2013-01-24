# Measure the shockfront from a list of profiles
# Sam Geen, February 2012

from Hamu.SimData.Simulation import Simulation
from analysis.profiles import profiles
import os
import numpy
import matplotlib.pyplot as plt

# Return a list of profile/output time pairs from a simulation
# alwaysbigger: If True, the shock radius should always be bigger than the last 
#               (prevents reverse shock from being used)
# allabovebackground: If True, use all the points above the background density
def ProfileMax(sim,alwaysbigger=False,allabovebackground=False):
    radii = list()
    rmax = -1
    #print len(sim.Outputs())
    rfloor = 0.
    for out in sim.Outputs():
        rmax = SnapProfileMax(out,sim.Location(),alwaysbigger,allabovebackground,rfloor)
        if alwaysbigger:
            rfloor = 0.5*rmax
        radii.append(rmax)
    return radii

def SnapProfileMax(snap,location,alwaysbigger=False,allabovebackground=False,rfloor=0.0):
    '''
    Find the max value in the profile for one snapshot
    alwaysbigger: If True, the shock radius should always be bigger than the last 
                  (prevents reverse shock from being used)
    allabovebackground: If True, use all the points above the background density
    '''
    prof = profiles.ReadPickle("pressure",snap.iout,location+"/")
    r = prof.radius
    p = prof.profile
    # Set a floor on radius
    cr = r >= rfloor
    rr = r[cr]
    pr = p[cr]
    # Find the pressure at the background
    pback = pr[len(pr)-1]
    # Find the max radius that lies above this (with a 5% noise filter)
    try:
        cr = pr > pback+0.1
        rr = rr[cr]
        rmax = numpy.max(rr)
    except:
        rmax = 0.0
    # Find max inside this
    #cp = pr == numpy.max(pr)
    #rmax = rr[cp]
    #rmax = rmax[0]
    # Reduce rmax to a single value (since it'll be an array currently)
    # Use every point above the background density?
    if allabovebackground:
        # Get background density
        init = profiles.ReadPickle("density",1,location+"/")
        bckg = numpy.max(init.profile[1:len(init.profile)])
        cp = pr > bckg # add a floor to ignore noise in background
        if len(rr[cp]) > 0:
            rmax = rr[cp]
            rmax = numpy.max(rmax)
    if alwaysbigger:
        # NOTE: USING *roughly* BIGGER TO ALLOW FLUCTUATING STATIC SHOCKS
        rfloor = 0.5*rmax
    return rmax
        
def ShockGraph(sim,allabovebackground=False,alwaysbigger=True):
    print "Processing simulation",sim.Location()
    # Run through the simulation, finding the highest pressure peak
    times = list()
    # Get radii
    radii = ProfileMax(sim,alwaysbigger,allabovebackground)
    # Get times
    i = 1
    for snap in sim:
        #print "output:", i
        times.append(snap.info["time"])
        i += 1
    print "Processed", i-1, "outputs"    
    return (radii, times)

def run(folder="."):
    # Open a simulation in a folder
    sim = Simulation(folder)
    # Find the radii for the shock front and times in each output
    radii, times = ShockGraph(sim)
    # Plototot
    plt.figure()
    xtitle = "Time / Myr"
    ytitle = "Shock radius / kpc"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    #print len(times), len(radii)
    #print times, radii
    plt.plot(times,radii)
    # Save pdf
    plt.savefig("shockfront.pdf",format="pdf")


if __name__=="__main__":
    run()

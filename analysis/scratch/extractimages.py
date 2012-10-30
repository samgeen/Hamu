# Extract images from a simulation at given times
# Sam Geen, Feb 2012

# GAH IMPERATIVE PROGRAMMING

import numpy as np
from pymses import RamsesOutput
import findoutput
import os
import profiles
import pylab
import matplotlib.pyplot as plt

# Run profile
def runprofile(proftype, outnum,timestr):
    # Run for profiles
    plot = profiles.prof(outnum,proftype)
    oldprof = "profiles_"+proftype+"/profile_"+str(outnum)+"_"+proftype+".pdf"
    newprof = "timeslices/prof_"+proftype+timestr+".pdf"
    os.system("cp "+oldprof+" "+newprof)
    return plot

# Main function
# instab - Focus on instabilties too?
def run(instab=False,corner=False,doprofiles=True):
    snapfolder = "."
    # Make directory
    os.system("mkdir timeslices")
    # Times to output (in Myr)
    times = np.array([5.,10.,14.,15.,20.])
    if instab: times = np.append(times,np.array([11.,12.,13.]))
    times.sort()
    print times
    profiles.corner = corner
    dens = list()
    temp = list()
    titles = list()
    # Find the output number for this timestep
    for time in times:
        outnum = findoutput.fromtime(time)
        outstr = "%(num)05d" % {'num':outnum}
        timestr = str(time)
        timestr = timestr.replace(".","p")
        oldname = "slices/slice"+outstr+"_1.png"
        newname = "timeslices/time_"+timestr+".png"
        os.system("cp "+oldname+" "+newname)
        # Run profiles
        if doprofiles:
            runprofile("density",outnum,timestr)
            runprofile("temperature",outnum,timestr)

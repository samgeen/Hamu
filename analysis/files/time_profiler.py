# Profile the time that a simulation takes from the timestamps of the outputs
# Sam Geen, October 2012


import os, time
import numpy as np
from copy import copy

import Hamu
from SimData.Simulation import Simulation

second = 1.0
minute = 60.0
hour = minute * 60.0
day = hour * 24.0

def strtime(time,format=""):
    '''
    Convert seconds into a string in seconds, hours or days
    time: Time in seconds to convert
    format: Can be "days", "hours", or "seconds"
    '''
    if len(format) == 0:
        if time > day:
            format = "days"
        elif time > hour:
            format = "hours"
        elif time > minute:
            format = "minutes"
        else:
            format = "seconds"
    if format == "days":
        return str(time / day)+" days"
    elif format == "hours":
        return str(time / hour)+" hours"
    elif format == "minutes":
        return str(time / minute)+" minutes"
    else:
        return str(times)+" seconds"

def comparediffs(diffs,idiff):
    '''
    Compute fractional difference between this value and its neighbours
    NOTE: 1st value in diffs is zero, so don't count that
    '''
    # If you want to understand what these letters mean, ask Romain Teyssier
    m = diffs[idiff]
    # Check for array boundary errors
    if idiff == 1: 
        return m / diffs[idiff+1]
    elif idiff == len(diffs)-1:
        return m / diffs[idiff-1]
    else:
        g = diffs[idiff-1]
        d = diffs[idiff+1]
        return 0.5 * m * ((g + d) / (g * d))

def run(simfolder,idlethresh=20.0):
    '''
    Inputs:
    simfolder - A location containing output_????? folders
    idlethresh - Threshold over mean difference between outputs to consider
                 the simulation to be idle, and to correct this difference
    '''
    # Load a simulation
    print "Loading simulation"
    sim = Simulation("",simfolder)
    # Get list of folders
    print "Making list of folders:"
    folders = sim.Folders()
    outs = sim.Outputs()
    print "Analysing simulation at", simfolder
    print "Simulation has",len(outs),"outputs"
    # Find folder creation times
    times = list()
    for folder in folders:
        #print "last modified: %s" % time.ctime(os.path.getmtime(file))
        times.append(os.path.getctime(folder))
    times = np.array(times)
    print times
    times -= times[0]
    numtimes = len(times)
    rawtime = times[numtimes-1]
    print "Total time from first to last output: ", strtime(rawtime)
    # Calculate timestep differences and correct for inactivity in outputs
    # Inactivity is usually caused by the simulation being stopped and restarted
    diffs = times[1:numtimes]-times[0:numtimes-1]
    diffs = np.concatenate((np.zeros(1),diffs))
    #print "Time differences:\n", diffs
    meandiff = np.mean(diffs)
    corrdiff = copy(diffs)
    corrected = False
    for idiff in range(1,numtimes):
        if comparediffs(diffs,idiff) > idlethresh:
            print "Output",outs[idiff],\
                "at time",times[idiff],\
                "with diff",diffs[idiff],\
                "has inactivity after it; correcting..."
            print comparediffs(diffs,idiff)
            # Simple correction; use previous value
            # NOTE: This can add some inaccuracy!
            corrdiff[idiff] = diffs[idiff-1]
            corrected = True
    # Print corrected time
    corrtime = np.sum(corrdiff)
    if corrected:
        print "Corrected total time (with inactivity removed):", \
            strtime(corrtime)
        print "NOTE: CORRECTED TIME MAY NOT BE COMPLETELY ACCURATE! "+\
        "USE AT YOUR OWN RISK"
    else:
        print "Simulation times not corrected; no inactivity detected"
    # Now compute CPU hours from rawtime and corrtime
    # Find number of cpus
    ncpu = 1
    for snap in sim:
        ncpu = snap.info["ncpu"]
        break
    print "Number of CPU hours (start to end estimate):", \
        strtime(rawtime*ncpu,"hours")
    if corrected:
        print "Number of CPU hours (corrected estimate):", \
            strtime(corrtime*ncpu,"hours")

if __name__=="__main__":
    run("./")

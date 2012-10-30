# Returns a snapshot number from the time inputted
# Uses internal time units
# TODO: Allow use of units, e.g. Myr, etc
# Sam Geen, Feb 2012

import numpy as np
from pymses import RamsesOutput

def fromtime(time,snapfolder="."):
    # Make a list of all the snapshots we can find
    # I seriously need a better routine for this
    # Better still, PYMSES needs one
    # Lazy feckers
    # Oh also find the output time
    snaps = list()
    times  = list()
    inds = range(1,99999)
    for outnum in inds:
        try:
            # Open snapshot
            snap = RamsesOutput(snapfolder, outnum)
            snaps.append(snap)
            # Now find the time
            times.append(snap.info["time"])
        except:
            print "Last output:", outnum-1
            break
    # Now find the output closest to the time given
    times = np.array(times)
    diff = np.abs(times - time)
    best = np.where(diff == np.min(diff))
    print best
    best = inds[best[0][0]]
    pdiff = (times[best-1]-time) / time * 100.0
    print "Found match with output",best,", %diff: ",pdiff
    return best

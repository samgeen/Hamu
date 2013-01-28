# Measure the total energy in the system to compare resolutions
# Sam Geen, February 2012

from Hamu.SimData.Simulation import Simulation
import analysis.profiles
import os
import numpy
import matplotlib.pyplot as plt

# Return a list of profile/output time pairs from a simulation
# alwaysbigger: If True, the shock radius should always be bigger than the last 
#               (prevents reverse shock from being used)
# allabovebackground: If True, use all the points above the background density
def ProfileTotal(sim,alwaysbigger=False,allabovebackground=False):
    values = list()
    rmax = -1
    #print len(sim.Outputs())
    rfloor = 0.
    kB = 1.3806488e-16 # in ergs/K
    gamma = 1.4 # is this in the nml.nml file
    X = 0.74 # hydrogen fraction, roughly
    mH = 1.67e-24 # hydrogen mass in g
    tscale = gamma * kB / (mH / X) # temperature -> energy scaling
    for out in sim.Outputs():
        profs = dict()
        hydros = ["density","temperature","velocity_radial",\
              "velocity_turbulent"]
        for hydro in hydros:
            profs[hydro] = profiles.ReadPickle(hydro,out,sim.Location()+"/")
        r = profs["density"].radius
        d = profs["density"].profile
        t = profs["temperature"].profile
        vr = profs["velocity_radial"].profile
        vt = profs["velocity_turbulent"].profile
        v = numpy.sqrt(vr*vr+vt*vt)
        ek = 0.5*(v*1e5)**2.0
        et = tscale * 10.0**t
        ek = ek[numpy.isfinite(ek)]
        et = et[numpy.isfinite(et)]
        energy = numpy.nansum(ek)+numpy.nansum(et)
        #print et
        values.append(energy)
    return values

def TotalEnergyGraph(sim,allabovebackground=False,alwaysbigger=True):
    print "Processing simulation",sim.Location()
    # Run through the simulation, finding the highest pressure peak
    times = list()
    # Get radii
    values = ProfileTotal(sim,alwaysbigger,allabovebackground)
    # Get times
    i = 1
    for snap in sim:
        #print "output:", i
        times.append(snap.info["time"])
        i += 1
    print "Processed", i-1, "outputs"    
    return (values, times)

def run(folder="."):
    # Open a simulation in a folder
    sim = Simulation(folder)
    # Find the radii for the shock front and times in each output
    radii, times = TotalEnergyGraph(sim)
    # Plototot
    plt.figure()
    xtitle = "Time / Myr"
    ytitle = "Total energy / units?"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    #print len(times), len(radii)
    #print times, radii
    plt.plot(times,radii)
    # Save pdf
    plt.savefig("totalenergy.pdf",format="pdf")


if __name__=="__main__":
    run()

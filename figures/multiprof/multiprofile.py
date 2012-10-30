# Plot multiple profiles for different times in each simulation listed
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import profiles
import matplotlib.pyplot as plt
import numpy as np
import findoutput

profiles.corner = True

# Run for 1 simulation
def runsim(sim,hydroname,simname):
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    labels = list()
    plots = list()
    outputs = [8,9,10,11,15]
    times = list()
    boxlen = sim[1].info["boxlen"]*1000.0
    boxlen = 60. # HARD CODING
    for out in outputs:
        times.append(sim[out].info["time"])
    colours = ('b','g','r','c','m','y','k','w')
    print sim.Location()
    for time, colour, outnum in zip(times,colours,outputs):
        timestr = str(int((time-14.125)*1e6))+"yr"
        prof = profiles.ReadPickle(hydroname,outnum,sim.Location())
        x, y = prof.radius, prof.profile
        print outnum, min(y), max(y)
        plot = ax.plot(x*1000,y,label=timestr,color=colour)
        ax.set_xlim([0.0,boxlen])
        if hydroname == "density":
            ax.set_ylim([0.0,3.0])
        if hydroname == "temperature":
            ax.set_ylim([-1.0,8.0])
        if hydroname == "velocity_radial":
            ax.set_ylim([-700.0,1000.0])
        plots.append(plot)
        labels.append(timestr)
    ax.legend(plots, labels,loc=4)
    xtitle = "Radius / pc"
    if hydroname == "density":
        ytitle = "log (Density / atoms/cc)"
    if hydroname == "temperature":
        ytitle = "log (Temperature / K)"
    if hydroname == "velocity_radial":
        ytitle = "Radial Velocity / km/s"
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    plt.savefig("earlyvrad"+simname+".pdf",format="pdf")
    plt.clf()
        
def run():
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/Production/09_Thornton_corner_hllc_c0p5/"
    sims = list()
    sims.append(top+"02_coolsn/")
    names = ["coolsn"]
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("thornton_coolsn")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        suite[name] = Simulation(sim)

    # Run for each simulation
    for name, sim in suite.iteritems():
        runsim(sim,"velocity_radial",name)

if __name__=="__main__":
    run()

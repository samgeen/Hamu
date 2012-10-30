# Plot multiple profiles for different times in each simulation listed
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import profiles
import matplotlib.pyplot as plt
import numpy as np
import findoutput

profiles.corner = False

# Run for 1 simulation
def runsim(sim,hydroname,simname):
    times = np.array([5.,10.,15.,20.])
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    labels = list()
    plots = list()
    colours = ('b','g','r','c','m','y','k','w')
    for time, colour in zip(times,colours):
        timestr = str(int(time))+"Myr"
        outnum = findoutput.fromtime(time,sim.Location())
        prof = profiles.ReadPickle(hydroname,outnum,sim.Location())
        x, y = prof.radius, prof.profile
        plot = ax.plot(x*1000,y,label=timestr,color=colour)
        ax.set_xlim([0.0,50.0])
        if hydroname == "density":
            ax.set_ylim([0.0,3.0])
        if hydroname == "temperature":
            ax.set_ylim([1.0,8.0])
        plots.append(plot)
        labels.append(timestr)
    ax.legend(plots, labels,loc=4)
    xtitle = "Radius / pc"
    if hydroname == "density":
        ytitle = "log (Density / atoms/cc)"
    if hydroname == "temperature":
        ytitle = "log (Temperature / K)"
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    plt.savefig("multiprofile"+simname+"_"+hydroname+".pdf",format="pdf")
    plt.clf()
    
        
def run():
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/HighDensity/02_thermal_wind_test/"
    sims = list()
    sims.append(top+"07_20rad_windsphere/")
    sims.append(top+"21_hybrid_windmetalcool/")
    sims.append(top+"30_quirk_vhigh/")
    sims.append(top+"36_hll_test/")
    names = ["nohybrid","smallthresh","largethresh","hll"]
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("hybridtest")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        suite[name] = Simulation(sim)

    # Run for each simulation
    for name, sim in suite.iteritems():
        runsim(sim,"density",name)
        runsim(sim,"temperature",name)

if __name__=="__main__":
    run()

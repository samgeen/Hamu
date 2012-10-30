# Multiple shock front test
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import shockfront
import matplotlib.pyplot as plt
import numpy as np

def run():
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/HighDensity/02_thermal_wind_test/"
    sims = list()
    sims.append(top+"07_20rad_windsphere")
    sims.append(top+"21_hybrid_windmetalcool")
    sims.append(top+"30_quirk_vhigh")
    sims.append(top+"36_hll_test")
    names = ["nohybrid","smallthresh","largethresh","hll"]
    labels = ["HLLC", "Hybrid0.5", "Hybrid50", "HLL"]
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("hybridtest")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        suite[name] = Simulation(sim)
    
    # Run shockfront for each sim
    graphs = list()
    for name in names:
        sim = suite[name]
        graphs.append(shockfront.ShockGraph(sim))
    
    # PLOT
    plt.figure()
    xtitle = "Time / Myr"
    ytitle = "Shock radius / pc"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.xlim((0,20))
    plots = list()
    for radii,times in graphs:
        plot = plt.plot(times,np.array(radii)*1000.)
        plots.append(plot)
    # The legend of the legend of the legend
    plt.legend(plots, labels,loc=2)
    # Save pdf
    plt.savefig("shockfront.pdf",format="pdf")

if __name__=="__main__":
    run()

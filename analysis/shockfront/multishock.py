# Multiple shock front test
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import shockfront
import matplotlib.pyplot as plt

def run():
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/HighDensity/02_thermal_wind_test/"
    sims = list()
    sims.append(top+"07_20rad_windsphere")
    sims.append(top+"21_hybrid_windmetalcool")
    sims.append(top+"30_quirk_vhigh")
    sims.append(top+"36_hll_test")
    names = ["nohybrid","smallthresh","largethresh","hll"]
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("hybridtest")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        suite[name] = Simulation(sim)
    
    # Run shockfront for each sim
    graphs = list()
    for sim in suite:
        graphs.append(shockfront.ShockGraph(sim))
    
    # PLOT
    plt.figure()
    xtitle = "Time / Myr"
    ytitle = "Shock radius / kpc"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    for radii,times in graphs:
        plt.plot(times,radii)
    # Save pdf
    plt.savefig("shockfront.pdf",format="pdf")

if __name__=="__main__":
    run()

# Resolution test shock front comparison
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import shockfront
import totalenergy
import matplotlib.pyplot as plt

def run(mode="shock"):
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/Jan2013/02_gravparttest/"
    sims = list()
#    sims.append("/home/samgeen/SN_Project/runs/Production/09_Thornton_corner_hllc_c0p5/03_windcoolsn")
    sims.append(top+"03_windcoolsn")
    sims.append(top+"04_windcoolsn_nopart")
#    sims.append(top+"03_lvl10_resim")
    names = ["part","nopart"]
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("hybridtest")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        suite[name] = Simulation(name,sim)
    names = list()
    for sim in suite:
        names.append(sim.Name())

    # ONLY CHECK CENTRAL 1/16!
    scale = 1.0/16.0
    
    # Run shockfront for each sim
    graphs = list()
    if mode == "shock":
        for sim in suite:
            graphs.append(shockfront.ShockGraph(sim,scale=scale))
        outname = "shockfront"
    elif mode == "totalenergy":
        for sim in suite:
            graphs.append(totalenergy.TotalEnergyGraph(sim))
        outname = "totalenergy"

    # PLOT
    plt.figure()
    xtitle = "Time / Myr"
    ytitle = "Shock radius / kpc"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    iname = 0
    for radii,times in graphs:
        plt.plot(times,radii,label=names[iname])
        iname += 1
    plt.legend()
    # Save pdf
    plt.savefig(outname+".pdf",format="pdf")

if __name__=="__main__":
    run()
    #run("totalenergy")

# Resolution test shock front comparison
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import shockfront
import matplotlib.pyplot as plt

def run():
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/ResTest/01_Thornton/"
    sims = list()
    sims.append("/home/samgeen/SN_Project/runs/Production/09_Thornton_corner_hllc_c0p5/03_windcoolsn")
    sims.append(top+"01_lvl10")
    sims.append(top+"02_lvl9")
    sims.append(top+"04_lvl8")
    sims.append(top+"03_lvl10_resim")
    names = ["11 levels", "10 levels","9 levels","8 levels","10 level resim"]
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("hybridtest")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        suite[name] = Simulation(name,sim)
    
    # Run shockfront for each sim
    graphs = list()
    for sim in suite:
        graphs.append(shockfront.ShockGraph(sim,allabovebackground=True))
    
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
    plt.savefig("shockfront.pdf",format="pdf")

if __name__=="__main__":
    run()

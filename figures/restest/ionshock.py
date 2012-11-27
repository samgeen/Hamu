# Resolution test ionisation front comparison
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import shockfront
import totalenergy
import matplotlib.pyplot as plt

def run(mode="shock"):
    # Simulations to use
    top = "/home/samgeen/SN_Project/runs/Lvl9/01_Thornton/"
    sims = list()
#    sims.append("/home/samgeen/SN_Project/runs/Production/09_Thornton_corner_hllc_c0p5/03_windcoolsn")
#    sims.append(top+"X8_ionfronttest")
#    sims.append(top+"X9_ionfrontwind")
    sims.append(top+"X0_bigboxgravtest")
    sims.append(top+"03_windcoolsn")
#    sims.append(top+"04_lvl8")
#    sims.append(top+"03_lvl10_resim")
    names = list()
#    names.append("ion with wind"])
#    names.append("ion no wind")
    names.append("big box")
    names.append("smallbox")
    # Make suite
    hamu = Hamu.Hamu(".")
    suite = hamu.MakeSuite("hybridtest")
    for i in range(0,len(names)):
        sim = sims[i]
        name = names[i]
        print sim, name
        suite[name] = Simulation(name,sim)
    names = list()
    for sim in suite:
        names.append(sim.Name())
    
    # Run shockfront for each sim
    graphs = list()
    if mode == "shock":
        for sim in suite:
            graphs.append(shockfront.ShockGraph(sim))
        outname = "shockfront"
    elif mode == "totalenergy":
        for sim in suite:
            graphs.append(totalenergy.TotalEnergyGraph(sim))
        outname = "totalenergy"

    # PLOT
    plt.figure()
    xtitle = "Time / Myr"
    ytitle = "Shock radius / kpc"
    if mode == "totalenergy":
        ytitle = "Total Energy / uh huh"
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
    run("totalenergy")
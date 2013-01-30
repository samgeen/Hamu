# Resolution test shock front comparison
# Sam Geen, March 2012

from Hamu.Workspace import Workspace
from Hamu.SimData.Simulation import Simulation
from Hamu.analysis.shockfront import shockfront
import totalenergy
import matplotlib.pyplot as plt

def run(mode="shock"):
    # Simulations to use
    #top = "/home/samgeen/SN_Project/runs/ResTest/02_ThorntonCentred/"
    #sims = list()
    #sims.append(top+"01_lvl10")
    #sims.append(top+"02_lvl9")
    #sims.append(top+"04_lvl8")
    #names = ["10 levels","9 levels","8 levels"]
    # NEW SIMULATIONS
    top = "/home/samgeen/SN_Project/runs/Jan2013/01_Thornton/"
    #sims = [top+"03_windsncool",top+"H3_windcoolsn_HIRES"]
    sims = [top+"03_windsncool",top+"F3_windkintest"]
    names=["13 levels","14 levels"]
    # Make suite
    hamu = Workspace(".")
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
            graphs.append(totalenergy.TotalEnergyGraph(sim,scale=scale))
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
    run("totalenergy")

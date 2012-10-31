# Plot radial profiles for videos
# Uses radials.py routine
# Sam Geen, October 2012

import Hamu
from SimData.Simulation import Simulation
import numpy as np
import radials

radials.imgtype = "png"
radials.folder = "radialplots"

def run():
    '''
    Plot various hydro variables radially at various timesteps 
    Inputs:
    runtype: "sn" - starts from the SN event
             "wind" - starts from star birth
             "windrt" - special case, pick last output (simulation in progress)
    imgtype: File ending (e.g. pdf) for pyplot to output to
    '''
    # Simulations to use
    wind = True
    windrt = False

    # Set up simulation folders and names
    top = "/home/samgeen/SN_Project/runs/"
    resfold = top+"ResTest/01_Thornton/"
    mainfold = top+"Production/09_Thornton_corner_hllc_c0p5/03_windcoolsn/"
    simlocs = list()
    simnames = list()
    # NOTE: SUPPRESSED AS THESE ARE ALREADY DONE
    #simlocs.append(mainfold)
    #simnames.append("full_res")
    resruns = ["01_lvl10", "02_lvl9", "03_lvl10_resim", "04_lvl8"]
    for run in resruns:
        simlocs.append(resfold+run)
        simnames.append(run)

    # Times to output at
    times = np.array([1e4,1e5,2e5,1e6])+14.125e6
    timestrs = ["1e4yr","1e5yr","2e5yr","1e6yr"]
    rawtimes = np.arange(1e4,1e6,1e4)
    times = np.array(rawtimes)+14.125e6
    timestrs = [str(x) + "yr" for x in times]    
    times /= 1e6 # Internal units are Myr
    if wind:
        times = np.array([5.0,10.0,12.0,14.0,15.125])
        timestrs = ["5e6yr","10e6yr","12e6yr","14e6yr","sn1e6"]
    if windrt:
        # HACK! RIDICULOUS VALUE! CHOOSE TIME OF LAST OUTPUT
        times = [1e9]
        timestrs = ["latest"]
    
    # Make suite
    #hamu = Hamu.Hamu(".")
    #suite = hamu.MakeSuite("hybridtest")
    #for sim, name in zip(sims, names):
    #    suite[name] = Simulation(sim)

    # Run radial profiles
    nums = range(0,len(times))
    boxlen = 100.0
    corner = True
    for sim, name in zip(simlocs, simnames):
        for time, num in zip(times, nums):
            numstr = '%(num)05d' % {'num': num}
            print "Plotting for run", name, "at", time,"yr"
            print "Folder:", sim
            print "Run in corner?", str(corner)
            plotter = radials.Radials(Simulation(name,sim),\
                                          name+"_"+numstr,\
                                          time,\
                                          corner,boxlen,wind)
            plotter.Run()

if __name__=="__main__":
    run()

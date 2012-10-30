# Plot profiles for density, temperature, radial velocity, fractional radial to non-radial velocity squared (i.e. energy fraction) against radius for a given time
# Sam Geen, March 2012

import Hamu
from SimData.Simulation import Simulation
import profiles
import matplotlib.pyplot as plt
import numpy as np
import findoutput
import os
import plotslice

profiles.corner = False
imgtype = "pdf"

class Radials(object):

    # Set up radial plot set
    def __init__(self,sim,simname,time,corner,boxlen,wind):
        self._simname = simname
        self._time = time
        self._sim = sim
        self._snap = sim.FindAtTime(time)
        self._outnum = self._snap.iout
        self._folder = "plots/"
        self._boxlen = boxlen
        self._corner = corner
        self._wind = wind

    # Main function of functionoid
    def Run(self):
        # Make folder to dump plots into
        if not os.path.isdir(self._folder):
            os.system("mkdir "+self._folder)
        # Set up hydronames
        hydros = ["density","temperature","velocity_radial","pressure",\
                      "velocity_turbulent"]
        # HACKY set font size
        plt.rc('text', fontsize=20)
        #plt.font.size=20
        # Make profiles of each name, including some special plots
        profs = dict()
        rads = dict()
        for hydroname in hydros:
            # Get profile
            profiles.corner = self._corner
            prof = profiles.ReadPickle(hydroname,self._outnum,\
                                           self._sim.Location())
            x, y = prof.radius, prof.profile
            # Save profile to be used later
            profs[hydroname] = y
            rads[hydroname] = x
            # Plot profile
            self.PlotProfile(x, [y], hydroname,labels=[str(self._time)+"yr"])
        # Make plot of energy in the same figure
        self.PlotEnergy(profs, rads, hydros)
        # Plot slice
        self.PlotSlices(self._sim.Location(), self._outnum,\
                            "density",self._boxlen)
        # Output log
        logfile = self._folder+"log_"+self._simname+".txt"
        f = open(logfile, 'w')
        f.write("simname: "+self._simname+"\n")
        f.write("actual time of output: "+str(self._time)+"yr"+"\n")
        f.write("output number: "+str(self._outnum)+"\n")
        f.write("original data at: "+self._sim.Location()+"\n")
        f.close()

    # Make one profile
    def PlotProfile(self, x, ys, hydroname,labels=[],legpos=4):
            plt.clf()
            fig = plt.figure()
            #ax = fig.add_subplot(111)
            # [left, bottom, width, height] where each value is between 0 and 1
            ax = plt.Axes(fig, [.2,.1,.7,.8])
            fig.add_axes(ax) 
            colours = ('b','g','r','c','m','y','k','w')
            if len(labels) == 0:
                for y in ys:
                    labels.append("")
            plots = list()
            for y, label in zip(ys,labels):
                plot = ax.plot(x*1000,y,label=label)
                plots.append(plot)
            # Set X-AXIS attributes
            radfact = 1.0
            if self._wind:
                if self._corner:
                    radfact = 0.3
                else:
                    radfact = 0.5
            if self._corner:
                ax.set_xlim([0.0,float(self._boxlen)*radfact])
            else:
                ax.set_xlim([0.0,0.5*float(self._boxlen)*radfact])
            xtitle = "Radius / pc"
            # Set Y-AXIS attributes by hydroname
            ylog = True
            if hydroname == "density":
                # HACK - USE NOT CORNER TO MEAN HIGH-DENSITY
                if not self._corner:
                    ax.set_ylim([-6.0,3.0])
                else:
                    ax.set_ylim([-6.0,1.0])
                ytitle = "Density / atoms/cm$^3$"
            if hydroname == "temperature":
                ax.set_ylim([-1.0,8.0])
                ytitle = "Temperature / K"
            if hydroname == "velocity_radial":
                # HACK - USE NOT CORNER TO MEAN HIGH-DENSITY
                if not self._corner:
                    ax.set_ylim([-200.0,200.0])
                else:
                    ax.set_ylim([-200.0,800.0])
                ytitle = "Radial Velocity / km/s"
                ylog = False
            if hydroname == "pressure":
                # HACK - USE NOT CORNER TO MEAN HIGH-DENSITY
                if not self._corner:
                    ax.set_ylim([-14.0,-11.0])
                else:
                    ax.set_ylim([-16.0,-13.0])
                ytitle = "Pressure / ergs/cm$^3$"
                pass
            if hydroname == "velocity_turbulent":
                ax.set_ylim([-100.0,100.0])
                ytitle = "Turbulent Velocity / km/s"
                ylog = False
            if hydroname == "fractional_energy":
                ax.set_ylim([-4,0.0])
                ytitle = "log$_{10}$(E$_{kin,turb,therm}$/E$_{tot})$"
                ylog = False
            if hydroname == "turbulent_energy":
                ax.set_ylim([49.0,51.0])
                ytitle = "E$_{turb}$ / erg"
            if hydroname == "kinetic_energy":
                ax.set_ylim([49.0,51.0])                
                ytitle = "E$_{kin}$ / erg"
            if hydroname == "thermal_energy":
                ax.set_ylim([49.0,51.0])
                ytitle = "E$_{therm}$ / erg"
            # Legend?
            if len(ys) > 1:
                # LEGEEEEND!
                ax.legend(plots,labels,legpos)
            # Make plot and save to file
            ax.set_xlabel(xtitle)
            ax.set_ylabel(ytitle)
            pname = self._folder+"profile_"+self._simname+"_"+hydroname
            plt.savefig(pname+"."+imgtype,format=imgtype)
            plt.clf()

    # Make plot of energy in the same figure
    def PlotEnergy(self, profs, rads, hydros):
        # Calculate *relative* energies
        # Constants
        kB = 1.3806488e-16 # in ergs/K
        gamma = 1.4 # is this in the nml.nml file
        X = 0.74 # hydrogen fraction, roughly
        mH = 1.67e-24 # hydrogen mass in g
        tscale = gamma * kB / (mH / X) # temperature -> energy scaling
        # All the radii should be the same, so pick one
        rad = rads["density"]
        # Find KE / unit mass (convert to cgs from km/s, too)
        pturb = 0.5*(profs["velocity_turbulent"]*1e5)**2.0
        pvrad = 0.5*(profs["velocity_radial"]*1e5)**2.0
        # Find thermal energy / unit mass
        ptherm = tscale * 10.0**profs["temperature"]
        # Find total energy per radial bin and scale it
        ptot = ptherm + pturb + pvrad
        fturb  = np.log10(pturb  / ptot)
        fvrad  = np.log10(pvrad  / ptot)
        ftherm = np.log10(ptherm / ptot)
        # PLOT IT UP
        x = rad
        ys = [fvrad,fturb,ftherm]
        hydroname = "fractional_energy"
        labels = ["E${kin}$/E${tot}$",\
                      "E${turb}$/E${tot}$",\
                      "E${therm}$/E${tot}$"]
        self.PlotProfile(x, ys, hydroname,labels)

    # Make plot of energy in the same figure
    def PlotSlices(self, folder, outnum,hydroname,boxlen):
        savename = self._folder+"slice_"+self._simname+"_"+hydroname
        plotslice.plot(outnum,folder,savename,self._boxlen,self._corner)
        plt.clf()

def run(runtype="sn",imgtype="pdf"):
    '''
    Plot various hydro variables radially at various timesteps 
    Inputs:
    runtype: "sn" - starts from the SN event
             "wind" - starts from star birth
             "windrt" - special case, pick last output (simulation in progress)
    imgtype: File ending (e.g. pdf) for pyplot to output to
    video:   If True, plot multiple outputs
    '''
    # Simulations to use
    wind = False
    windrt = False
    if runtype == "wind":
        wind = True
    if runtype == "windrt":
        windrt = True

    top = "/home/samgeen/SN_Project/runs/Production/"
    # TODO: PUT BACK IN WINDS
    runstubs = ["01_onlysn","02_coolsn"]
    runtitles = ["onlysn","coolsn"]
    snonly = [True,True]
    if wind:
        runstubs  = ["03_windcoolsn"]
        runtitles = ["windcoolsn"]
        snonly = [False]
    if windrt:
        runstubs  = ["05_windrtcoolsn"]
        runtitles = ["windrtsn"]
        snonly = [False]
    simnames = ["08_standard_noise_10K","09_Thornton_corner_hllc_c0p5"]
    simtitles = ["cloud","thornton"]
    boxlens = list()
    sims = list()
    names = list()
    corners = list()

    # Make lists of simulation locations and names
    for sim, stit in zip(simnames, simtitles):
        for run, rtit in zip(runstubs, runtitles):
            sims.append(top+sim+"/"+run+"/")
            names.append(stit+"_"+rtit)
            if stit == "cloud":
                corners.append(False)
                boxlens.append(50.0)
            else:
                corners.append(True)
                boxlens.append(100.0)

    # Times to output at
    times = np.array([1e4,1e5,2e5,1e6])+14.125e6
    times /= 1e6 # Internal units are Myr
    timestrs = ["1e4yr","1e5yr","2e5yr","1e6yr"]
    if video:
        temp = np.arange(1e4,1e6,1e4)
        times = np.array(temp)+14.125e6
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
    for sim, name, corner, boxlen in zip(sims, names, corners,boxlens):
        for time, tstr in zip(times, timestrs):
            print "Plotting for run", name, "at", time,"yr"
            print "Folder:", sim
            print "Run in corner?", str(corner)
            plotter = Radials(Simulation(sim),name+"_"+tstr,time,\
                                  corner,boxlen,wind)
            plotter.Run()

if __name__=="__main__":
    run()

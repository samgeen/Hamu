# Graphs of quantities over time in the system
# Sam Geen, March 2012

#import Hamu
from Hamu.SimData.Simulation import Simulation
from Hamu import profiles
import matplotlib.pyplot as plt
import numpy as np
import os
import Hamu.analysis.visualisation.plotslice as plotslice
import Hamu.analysis.shockfront.shockfront as shockfront

profiles.corner = False

class Times(object):

    # Set up the time series plotting
    def __init__(self,sim,simname,corner,boxlen,onlysn=True):
        self._sim = sim
        self._simname = simname
        self._folder = "plots/"
        self._boxlen = boxlen
        self._corner = corner
        self._logfile = open(self._folder+"timelog_"+simname+".dat","w")
        self._onlysn = onlysn

    # Rununun
    def Run(self):
        # Make plot directory
        if not os.path.isdir(self._folder):
            os.system("mkdir "+self._folder)
        # Get shock front
        #radii, times = shockfront.ShockGraph(self._sim,\
        #                                     allabovebackground=True,\
        #                                     alwaysbigger=False)
        alwaysbigger = False
        #if self._onlysn == False:
        #    alwaysbigger = True # had some problems with reverse shocks before
        rshock, times = shockfront.ShockGraph(self._sim,\
                                             allabovebackground=False,\
                                             alwaysbigger=alwaysbigger)
        radii = rshock # Give up on the idea of measuring over background
        radii = np.array(radii)
        times = np.array(times)
        rshock = np.array(rshock)
        # Remove any times before SN if only the SN is plottoted
        if self._onlysn:
            print "ONLY SUPERNOVA BEING PLOTTED"
            tsn = 14.125
            isn = times >= tsn
            times = times[isn] - tsn
            radii = radii[isn]
            rshock = rshock[isn]
        # DEBUG SHOCK RADIUS?
        #plt.plot(times*1e6, radii*1000)
        #plt.savefig("DEBUG_"+self._simname+".pdf",format="pdf")

        # Use these to find the energy inside the shock
        hydros = ["density","velocity_radial","velocity_turbulent",\
                  "temperature"]
        eTherm = list()
        eKin = list()
        eTurb = list()
        masses = list()
        print "Number of outputs", len(times)
        for out, radius, time in zip(self._sim.Outputs(), radii, times):
            profs = dict()
            rads = dict()
            for hydroname in hydros:
                # Get profile
                profiles.corner = self._corner
                prof = profiles.ReadPickle(hydroname,out,\
                                               self._sim.Location())
                x, y = prof.radius, prof.profile
                # Save profile to be used later
                profs[hydroname] = y
                rads[hydroname] = x
            
            # Find radial masses, energies
            therm, kin, turb, mass = self.FindEnergy(profs,rads,radius)
            eTherm.append(therm)
            eKin.append(kin)
            eTurb.append(turb)
            masses.append(mass)
        
        # Print *final* mass, energy, radius, time
        self._logfile.write("log: Mass / Msolar, "+ \
                                "etherm, ekin, eturb, etot / erg, "+ \
                                "radius / pc, time / yr\n")
        log10 = np.log10
        etot = kin+therm
        self._logfile.write(str(log10(mass/1.98892e33))+" "+\
                            str(log10(therm))+" "+\
                            str(log10(kin))+" "+\
                            str(log10(turb))+" "+\
                            str(log10(etot))+" "+\
                            str(log10(radius*1000))+" "+\
                            str(log10(time*1e6))+"\n")
        self._logfile.write("fraction: etherm, ekin, eturb / etot, "+\
                                "eturb/ekin\n")
        self._logfile.write(str(therm/etot)+" "+\
                            str(kin/etot)+" "+\
                            str(turb/etot)+" "+\
                            str(turb/kin)+"\n")

        # Plot energies
        self.PlotEnergies(times, eTherm, eKin, eTurb)

        # Plot the shock radius and mass
        self.PlotRadiusMass(times, rshock, masses)

    
    # Find the energy at a given output
    def FindEnergy(self, profs, radii, rlimit):
        # Constants
        kB = 1.3806488e-16 # in ergs/K
        gamma = 1.4 # is this in the nml.nml file
        deg_free = 2.0 / (gamma - 1.0) # degrees of freedom
        X = 0.76    # hydrogen fraction, roughly
        Z = 0.06667
        Y = 1.0 - X - Z
        mu = 1.0/(2.0*X + 0.75*Y + 0.5*Z)

        mH = 1.67e-24 # hydrogen mass in g
        kpc = 3.08568025e21 # 1kpc in cm
        # All the radii dict values should be the same, so pick one
        rad = radii["density"]*kpc
        # Get the radii either side of each radial bin
        rlow = np.append([0],rad)
        # NOTE: 2*rad[len(rad)-1]-rad[len(rad)-2] is a guess of radius N+1
        rhigh = np.append(rad,[2*rad[len(rad)-1]-rad[len(rad)-2]])
        rmean = 0.5*(np.array(rlow)+np.array(rhigh))
        # Volume of each radial shell
        volmean = 4.0/3.0*np.pi*rmean**3.0
        volshell = volmean[1:len(volmean)] - volmean[0:len(volmean)-1]
        # Mass (NB - density profile is log10)
        massshell = np.array((10.0**profs["density"])*volshell*mu*mH)
        tscale = massshell * deg_free * kB / (mu*mH) # T->E scaling
        vscale = 0.5*massshell # v^2->E scaling
        # Find KE / unit mass (convert to cgs from km/s, too)
        pturb = vscale*(profs["velocity_turbulent"]*1e5)**2.0
        pvrad = vscale*(profs["velocity_radial"]*1e5)**2.0
        pkin = pturb + pvrad
        # Compensate for not measuring radial turbulent motion
        # NOTE! THIS ASSUMES THAT:
        # - THE NON-RADIAL V = TURBULENCE
        # - SOME OF THE RADIAL V OF EQUAL MAGNITUDE IS ALSO TURBULENCE
        # HENCE ASSUMING WE'RE ONLY MEASURING 2 OF 3 AXES + COMPENSATE
        pturb *= 1.5
        # Find thermal energy / unit mass (NB - T profile is log10)
        ptherm = tscale * 10.0**profs["temperature"]
        # Find radius of shock (plus a few % as it's not that sharp) 
        #    and cut inside that
        rlimit = rlimit*1.01
        ishock = rad/kpc < rlimit
        # Kill infinite temperature elements (happens apparently)
        # Just interpolate over neighbouring elements here
        prev = 0.
        ielem = 0
        for elem in ptherm:
            if elem > 1e100:
                l = ptherm[ielem-1]
                r = ptherm[ielem+1]
                if l > 1e100:
                    l = ptherm[ielem-2]
                if r > 1e100:
                    r = ptherm[ielem+2]
                ptherm[ielem] = 0.5*(l+r)
            ielem += 1
        etherm = np.nansum(ptherm[ishock])
        ekin = np.nansum(pkin[ishock])
        eturb = np.nansum(pturb[ishock])
        mass = np.nansum(massshell[ishock])
        if etherm > 1e70:
            import pdb
            pdb.set_trace()
        #print etherm, ekin, eturb
        return (etherm, ekin, eturb, mass)

    # Power law (well, linear as these are log inputs) fit
    def PowerLaw(self, x, y):
        newx = []
        newy = []
        inf = np.inf
        nan = np.nan
        # I have finally cracked and gone mad
        for i in range(0,x.size):
            if x[i] != -inf and y[i] != -inf and \
               x[i] !=  inf and y[i] !=  inf and \
               x[i] !=  nan and y[i] !=  nan:
                newx.append(x[i])
                newy.append(y[i])
        newx = np.array(newx)
        newy = np.array(newy)
        fit = np.polyfit(newx,newy,1)
        self._logfile.write(str(fit[0])+" * x + "+str(fit[1])+"\n")

    # Plot the shock radius
    def PlotRadiusMass(self, times, radii, masses):
        legpos = 4
        # HACKY set font size
        plt.rc('text', fontsize=20)
        plt.clf()

        # Constants
        msolar = 1.98892e33 # msolar in cgs

        # Set up time coord
        x = np.log10(times*1e6)

        # RAY DE OOS
        fig = plt.figure()
        # [left, bottom, width, height] where each value is between 0 and 1
        ax = plt.Axes(fig, [.2,.1,.7,.8])
        fig.add_axes(ax) 
        colours = ('b','r','g','k')#,'m','y','c','w')
        # PLOTOTOT THE LINININES
        y = np.log10(radii*1000)
        print "Minmax log radius / pc", np.min(y), np.max(y)
        plot = ax.plot(x,y,label="Shock Radius")
        # Set X-AXIS attributes
        ax.set_xlim([4.5,6.0])
        xtitle = "log10(Time / yr)"
        # Set Y-AXIS attributes by hydroname
        #ax.set_ylim([-2.0,2.0])
        ytitle = "log10(Shock Radius / pc)"
        # Make plot and save to file
        ax.set_xlabel(xtitle)
        ax.set_ylabel(ytitle)
        pname = self._folder+"times_"+self._simname+"_radius"
        plt.savefig(pname+".pdf",format="pdf")
        plt.clf()

        # Find time-radius power law fit
        self._logfile.write("time-radius power law fit:")
        self.PowerLaw(x,y)

        # MAAAAARSE
        # RAY DE OOS
        legpos = 4
        fig = plt.figure()
        # [left, bottom, width, height] where each value is between 0 and 1
        ax = plt.Axes(fig, [.2,.1,.7,.8])
        fig.add_axes(ax) 
        colours = ('b','r','g','k')#,'m','y','c','w')
        # PLOTOTOT THE LINININES
        y = np.log10(masses)-np.log10(msolar)
        plot = ax.plot(x, y,label="Remnant Mass")
        # Set X-AXIS attributes
        ax.set_xlim([4.5,6.0])
        xtitle = "log10(Time / yr)"
        # Set Y-AXIS attributes by hydroname
        #ax.set_ylim([-2.0,10.0])
        ytitle = "log10(Remnant Mass / M$_{\odot}$)"
        # Make plot and save to file
        ax.set_xlabel(xtitle)
        ax.set_ylabel(ytitle)
        pname = self._folder+"times_"+self._simname+"_mass"
        plt.savefig(pname+".pdf",format="pdf")
        plt.clf()

        # Find time-mass power law fit
        self._logfile.write("time-mass power law fit:")
        self.PowerLaw(x,y)
        
    # Plot the energies in a line
    def PlotEnergies(self, times, etherm, ekin, eturb):
        legpos = 4
        # HACKY set font size
        plt.rc('text', fontsize=20)
        plt.clf()
        fig = plt.figure()
        # [left, bottom, width, height] where each value is between 0 and 1
        ax = plt.Axes(fig, [.2,.1,.7,.8])
        fig.add_axes(ax) 
        colours = ('b','r','g','k')#,'m','y','c','w')
        # PLOTOTOT THE LINININES
        plots = list()
        labels = ["E$thermal$", "E$kinetic$", "E$turbulent$","E$total$"]
        times = np.log10(times*1e6)
        etot = np.log10(np.array(etherm)+\
                        np.array(ekin))
        etherm = np.log10(etherm)
        ekin = np.log10(ekin)
        eturb = np.log10(eturb)
        print "Minmax time, etherm, ekin, eturb, etot"
        print np.min(times), np.max(times)
        print np.min(etherm), np.max(etherm)
        print np.min(ekin), np.max(ekin)
        print np.min(eturb), np.max(eturb)
        print np.min(etot), np.max(etot)
        plot = ax.plot(times, etherm,label=labels[0])
        plots.append(plot)
        plot = ax.plot(times, ekin,label=labels[1])
        plots.append(plot)
        plot = ax.plot(times, eturb,label=labels[2])
        plots.append(plot)
        plot = ax.plot(times, etot,label=labels[3])
        plots.append(plot)
        # Set X-AXIS attributes
        ax.set_xlim([4.5,6.5])
        xtitle = "log10(Time / yr)"
        # Set Y-AXIS attributes by hydroname
        ax.set_ylim([40.0,52.0])
        ytitle = "log10(Energy / erg)"

        # LEGEEEEND!
        ax.legend(plots,labels,legpos)
        # Make plot and save to file
        ax.set_xlabel(xtitle)
        ax.set_ylabel(ytitle)
        pname = self._folder+"times_"+self._simname+"_energy"
        plt.savefig(pname+".pdf",format="pdf")
        plt.clf()

def run(wind=False):
    # Folder where all my neat stuff is stashed
    top = "/home/samgeen/SN_Project/runs/Production/"
    # Run parameter stuff
    runstubs = ["01_onlysn","02_coolsn"]#,"03_windcoolsn"]
    runtitles = ["onlysn","coolsn"]#,"windcoolsn"]
    snonly = [True,True]
    if wind:
        runstubs  = ["03_windcoolsn"]
        runtitles = ["windcoolsn"]
        snonly = [False]
    # Sim-you-lay-tea-on initial condition stuff
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
                boxlens.append(100.0)
            else:
                corners.append(True)
                boxlens.append(200.0)

    # Simulations
    for sim in sims:
        print sim

    # Run radial profiles
    onlysn = not wind
    for sim, name, corner, boxlen in zip(sims, names, corners,boxlens):
        print "Plotting for run", name
        print "Folder:", sim
        print "Run in corner?", str(corner)
        plotter = Times(Simulation(name, sim),name,corner,boxlen,onlysn)
        plotter.Run()

if __name__=="__main__":
    run()

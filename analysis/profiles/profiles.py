# Display gas property profiles
# Sam Geen, Jan 2012

from pymses import RamsesOutput
from ProfileMaker import ProfileMaker
from pymses.utils import constants as C
import matplotlib.pyplot as plt
import numpy as np
import os
import cPickle as pik

corner = True

# Structure for storing pickle data
class Pickle(object):
    def __init__(self,radius,profile,hydroname,xtitle,ytitle):
        self.radius = radius
        self.profile = profile
        self.xtitle = xtitle
        self.ytitle = ytitle

def ReadPickle(hydroname, outnum,folder="./"):
    filename = Prefile(hydroname,outnum,False,folder)+".pik"
    # Write profile if it doesn't exist
    if not os.path.isfile(filename):
        prof(outnum,hydroname,folder)
    file   = open(filename,"rb")
    r      = pik.load(file)
    p      = pik.load(file)
    xtitle = pik.load(file)
    ytitle = pik.load(file)
    file.close()
    return Pickle(r,p,hydroname,xtitle,ytitle)

# File prefix
def Prefile(hydroname,outnum,makefolder=False,folder="./"):
    folder += "/profiles_"+hydroname+"/"
    if not os.path.isdir(folder):
        os.system("mkdir "+folder)
    prefile = folder+"profile_"+str(outnum)+"_"+hydroname
    return prefile

# This is oh so hacky, if you're using this and your name isn't Sam Geen 
#                                                      THEN GOD HELP YOOOUUU
def prof(outnum=100,name="mach",snaplocation="./"):
    # Print location we're saving to
    print "Saving to: ", Prefile(name,outnum,False,snaplocation)
    # Open output
    snap = RamsesOutput(snaplocation, outnum)
    # Get profiles for relevant variables
    gamma = 5./3.
    pmaker = ProfileMaker(snap)
    # Set profile region
    centre = [0.5,0.5,0.5]
    radius = 0.5
    ylog = True
    if corner==True:
        centre = [0.0,0.0,0.0]
        radius = 1.0
    pmaker.Shape(centre, radius)
    # Switch betwen different uses
    if name == "mach":
        r,dens = pmaker.MakeProfile("rho")
        r,pres = pmaker.MakeProfile("P")
        r,spd  = pmaker.MakeProfile("spd")
        # Calculate mach number profile
        prof = np.sqrt(spd**2. * dens / (gamma * pres))
    if name == "pressure":
        r,prof = pmaker.MakeProfile("P")
        ytitle = "Pressure"
        prof *= snap.info["unit_pressure"].express(C.dyne)
    if name == "metal":
        r,prof = pmaker.MakeProfile("Z")
        ytitle = "Metallicity / Zsolar"
    if name == "velocity_radial":
        ylog = False
        r,prof = pmaker.MakeProfile("vrad")
        ytitle = "Radial Velocity"
        prof *= snap.info["unit_velocity"].express(C.km/C.s)
    if name == "velocity_turbulent":
        ylog = False
        r,prof = pmaker.MakeProfile("vturb")
        ytitle = "Turbulent Velocity"
        prof *= snap.info["unit_velocity"].express(C.km/C.s)
    if name == "speed":
        ylog = False
        r,prof = pmaker.MakeProfile("spd")
    if name == "temperature":
        r,P = pmaker.MakeProfile("P")
        r,rho = pmaker.MakeProfile("rho")
        prof =  P / rho * snap.info["unit_temperature"].express(C.K)
        ytitle = "Temperature / K"
    if name == "density":
        r,prof = pmaker.MakeProfile("rho")
        #prof *= snap.info["unit_density"].express(C.H_cc)
        #print "Y-AXIS UNITS:",snap.info["unit_density"].express(C.H_cc)
        #print "MIN/MAX PROF:", np.min(prof), np.max(prof)
        ytitle = "Density / atoms/cc"
    # NOTE: "quirk" refers to Quirk 1994; pressure difference between cells 
    if name == "quirk":
        r,pres = pmaker.MakeProfile("P")
        lp = len(pres)
        pright = np.array(pres[1:lp])
        pleft = np.array(pres[0:lp-1])
        rright = np.array(r[1:lp])
        rleft = np.array(r[0:lp-1])
        prof = np.abs((pright - pleft)/(rright-rleft))
        r = rright
    # This calculates the approximate Field length in Koyama + Inutsuka 2004
    if name == "field":
        r,pres = pmaker.MakeProfile("P")
        r,dens = pmaker.MakeProfile("rho")
        dens *= snap.info["unit_density"].express(C.H_cc)
        temp = pres/dens * snap.info["unit_temperature"].express(C.K)
        # In pc
        field = 1.4e-2 * temp**0.35 / dens
        temp = np.array(temp)
        r = np.array(r)
        field = np.array(field)
        prof = field
        inr = np.where(temp < 8000) and np.where(temp > 100)
        r = r[inr]
        prof = field[inr]

    # Recast radius units
    r *= snap.info["boxlen"]
    xtitle = "Radius / kpc"

    #print len(r), len(vel)
    #print vel.shape
    if ylog:
        prof = np.log10(np.array(prof))
        ytitle = "log("+ytitle+")"
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plot = plt.plot(r,prof)
    # Save pickle file
    prefile = Prefile(name,outnum,True,snaplocation)
    file = open(prefile+".pik","wb")
    print "Exporting as pickle..."
    pik.dump(r,file)
    pik.dump(prof,file)
    pik.dump(xtitle,file)
    pik.dump(ytitle,file)
    file.close()
    # Save pdf
    print "Saving profile to",prefile+".pdf"
    plt.savefig(prefile+".pdf",format="pdf")
    print "DONE"
    return plot

def runall():
    for snap in range(1,99999):
        prof(snap, "temperature")
        plt.clf()
        prof(snap, "density")
        plt.clf()
        prof(snap, "velocity_radial")
        plt.clf()
        prof(snap, "velocity_turbulent")
        plt.clf()
        prof(snap, "pressure")

if __name__=="__main__":
    # Pick an arbitrary output number
    prof(20)

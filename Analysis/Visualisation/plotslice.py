# Plot multiple images for different times in each simulation listed
# Sam Geen, March 2012

import Hamu
from Hamu.SimData.Simulation import Simulation
from Hamu import profiles
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

# Plot a single image with axes and everything
def plot(outnum,snaploc,savename,boxlen=100.,corner=True,frac=1.0):
    # Set up figure
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    # Load image
    # REQUIRES TESTSLICE.PY TO HAVE BEEN RUN FIRST
    outstr = "%(num)05d" % {'num':outnum}
    loc = snaploc+"/slices/slice"+outstr+"_1.png"
    im = mpimg.imread(loc)
    # Display imagex
    br = boxlen / 2
    if corner:
        extent=(0,boxlen,boxlen,0)
    else:
        extent=(-br,br,-br,br)
    if frac < 1.0:
        if corner:
            c = len(im) # ASSUMES A SQUARE!!!
            c = int(c*frac)
            im = im[0:c,0:c]
        else:
            print "Centre frac code not implemented yet"
            raise NotImplementedError
    imrange = (-4.5,6.0)
    d,u = imrange
    cax = ax.imshow(im, interpolation='nearest',\
                        extent=extent,vmin=d,vmax=u)
    # Add colour bar
    cbar = fig.colorbar(cax)
    cbar.set_label("Density / atoms/cm$^{3}$")
    plt.savefig(savename+".pdf",format="pdf")


'''
class MultiImage(object):
    
    def __init__(self):
        self._snaps = list()
        self._locs = list()

    # Make an image from a set of snapshots
    def MakeImage(self,name):
        fig = plt.figure()
        ifig = 0
        l = 1024
        xarr = [0,l,0,l]
        yarr = [0,0,l,l]
        iarr = 0
        extent=(-50,50,-50,50)
        imrange = (-4.5,6.0)

        # Make subplots
        fig = plt.figure(figsize=(8.3,9.7))
        ax  = fig.add_subplot(111)
        # Run through subplots
        allim = np.zeros([2*l,2*l,4])
        for snap in self._snaps:
            # Open an image file from the snapshot
            # REQUIRES TESTSLICE.PY TO HAVE BEEN RUN FIRST
            outnum = snap.iout
            outstr = "%(num)05d" % {'num':outnum}
            snaploc = snap.output_repos
            loc = snaploc+"/slices/slice"+outstr+"_1.png"
            im = mpimg.imread(loc)
            d,u = imrange
            im = np.array(im)
            x = xarr[iarr]
            y = yarr[iarr]
            allim[x:x+l,y:y+l,:] = im
            # Add to figure
            #ifig += 1
            #ax = fig.add_axes([0.05+x, 0.10+y, 0.40, 0.4])
            #imaxis = ax.imshow(im, interpolation='nearest',extent=extent,\
            #                       vmin=d,vmax=u)
            iarr += 1

        # Plot superimage
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        imaxis = ax.imshow(allim, interpolation='nearest',extent=extent,\
                               vmin=d,vmax=u)
        # Colouuuuur bar
        #cax = fig.add_axes([0.87, 0.1, 0.03, 0.8])
        #cbr = fig.colorbar(imaxis)
        
        cbarax = fig.add_axes([0.05, 0.475, 0.90, 0.05])
        cbar = fig.colorbar(imaxis, cbarax, orientation='horizontal')
        cbar.set_label("Density / atoms/cc")

        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        plt.savefig("multiimage"+name+".pdf",format="pdf", bbox_inches='tight')
            
    def Run(self):
        # Simulations to use
        top = "/home/samgeen/SN_Project/runs/HighDensity/02_thermal_wind_test/"
        sims = list()
        sims.append(top+"07_20rad_windsphere/")
        sims.append(top+"21_hybrid_windmetalcool/")
        sims.append(top+"30_quirk_vhigh/")
        sims.append(top+"36_hll_test/")
        names = ["nohybrid","smallthresh","largethresh","hll"]
        # Make suite
        hamu = Hamu.Hamu(".")
        suite = hamu.MakeSuite("hybridtest")
        for i in range(0,len(names)):
            sim = sims[i]
            name = names[i]
            suite[name] = Simulation(sim)

        # Make plots for each time
        times = [5.,10.,14.,15.,20.]
        for time in times:
            # Make an image for a single time
            timestr = str(int(time))+"Myr"
            snaps = suite.FindTime(time)
            # Remap snaps to be in the same order as "names"
            snaplist = list()
            for name in names:
                snaplist.append(snaps[name])
            self._snaps = snaplist
            # MAEK IMUGJ
            self.MakeImage(timestr)
            
def run():
    m = MultiImage()
    m.Run()
'''
if __name__=="__main__":
    plot(100,".","plotslice_test")

#! /usr/bin/env python
# Scratch space for making slices of the SNe
# DEPRECATED, USE slices.py AND SliceMaker.py


# THIS SO HORRIBLE OH GOD

#import SnapMovie
import numpy as np
import pymses
from pymses.analysis.visualization import Camera, SliceMap, ScalarOperator
import pylab
import cPickle as pik

corner=True

fixmin = -4.5
fixmax = 6.0
#fixmin = 0
#fixmax = 0

#fixmin = -2.5
#fixmax = 5.0
#fixmin = -4.0
#fixmax = -3.0

def MinMax(minin, maxin):
    fixmin = minin
    fixmax = maxin

# Filename prefix (i.e. file = prefix.pik, prefix.png, etc)
def Prefix(snapnum, slicenum,hydroname):
    imfile = "slice"
    name = ""
    if hydroname != "rho":
        name = hydroname
    # Make slice folder
    import os
    if not os.path.isdir("slices"+name):
        os.system("mkdir slices"+name)
    snapstr = '%(num)05d' % {'num': snapnum}
    return "slices"+name+"/"+imfile+snapstr+"_"+str(slicenum)

# Scales images by max/min density over all of them and outputs them
# INPUT: Slice number (integer)
def ScaleImages(slicenum, hydroname,outrange=range(1,99999)):
    # Find image min/max
    maxim = -1e30
    minim = 1e30
    maps = []
    print fixmin, fixmax

    # Fuck it, just run until it breaks
    print "Finding max/min in snapshot..."
    for snap in outrange:
        try:
            print snap
            prefile = Prefix(snap, slicenum, hydroname)
            file = open(prefile+".pik","rb")
            map = pik.load(file)
            file.close()
            maps.append(map)
                #pylab.imsave(prefile+".png", map,format="png")
            maxim = np.max([np.max(map),maxim])
            minim = np.min([np.min(map),minim])
        except:
            print "Done (or an error...)!"
            break
        print "Min/max over whole simulation:", minim, maxim
    if (fixmin != 0 or fixmax != 0) and hydroname == "rho":
        # Use fixed min/max
        maxim = fixmax
        minim = fixmin
    
    rngim = maxim - minim
    # Now output images
    isnap = 0
    for map in maps:
        snap = outrange[isnap]
        # Scale map
        scmap = (map - minim) / rngim
        # Output scaled map
        prefile = Prefix(snap, slicenum,hydroname)
        print "Saving image: ", prefile+".png"
        pylab.imsave(prefile+".png", scmap,format="png", \
                     vmin = 0, vmax = 1)#, \
                     #cmap=pylab.get_cmap("prism"))
        # Next snapshot number
        isnap = isnap+1
            
def run(cornerIn=True,hydroname="rho"):
    runrange(range(1,99999),cornerIn,hydroname)

def runrange(outrange=range(1,99999),cornerIn=True,hydroname="rho"):
    corner = cornerIn
    if corner==True:
        print "SN in corner"
    else:
        print "SN in centre"
    # Get data
#    snapfolder = "/home/samgeen/SN_Project/runs/Pre-Oxford-22Nov2011/" + \
#        "03_lvl10_M15/08_rt_wind_sn/"
    #snapfolder = "/home/samgeen/SN_Project/runs/Pre-Oxford-22Nov2011/" + \
    #    "03_lvl10_M15/09_wind_sn_centre/"
    #snapfolder="/home/samgeen/SN_Project/runs/HighDensity/01_scaling_test_windcool_norad/02_024proc/"
#    snapfolder = "/home/samgeen/SN_Project/runs/Pre-Oxford-22Nov2011/" + \
#        "03_lvl10_M15/07_sn_only_nocool/"
#    snapfolder="/home/samgeen/SN_Project/runs/HighDensity/01_scaling_test_windcool_norad/03_36proc_lotsofoutputs/"
#    snapfolder="/home/samgeen/SN_Project/runs/HighDensity/02_thermal_wind_test/02_10rad_wind_cool_nort/"
    # Use current working directory
    snapfolder="./"
    print "Running with hydro variable: ", hydroname
    # Fuck it, just run until it breaks
    # TODO: Actually find a list of outputs in the folder
    # Does Pymses allow you to access this data? Probably.
    for i in outrange:
        # Make file name
        snapnum = i
        prefile = Prefix(snapnum, 1,hydroname)
        # Do we not already have the .pik file?
        import os
        if os.path.isfile(prefile+".pik"):
            print "Already file"+prefile+".pik ; skipping..."
        else:
            try:
                print "Reading output ", snapnum, " in : ", snapfolder
                ro = pymses.RamsesOutput(snapfolder, snapnum)
                amr = ro.amr_source([hydroname])
                # Make camera + slice function
                print "Setting up data slice"
                cam  = Camera(center=[0.5, 0.5, 0.5], line_of_sight_axis='z', \
                                  region_size=[1.0, 1.0],\
                                  up_vector='y', map_max_size=1024, log_sensitive=True)
                rho_op = ScalarOperator(lambda dset: dset[hydroname])
                # create a density slice map at various depth positions
                # TODO: Figure out why only negative z-values work
                print "Plotting data slice"
                islice = 0
                #zarr = np.arange(0.1,-0.1001,-0.05)
                zarr = [0.0]
                if corner:
                    zarr = [-0.5]
                for iz in zarr:
                    islice += 1
                    # HACK
                    map = SliceMap(amr, cam, rho_op, z=iz)
                    print "Map min/max: ", np.min(map), np.max(map)
                    prefile = Prefix(snapnum, islice,hydroname)
                    # Pickle instead so we can reload and make a movie 
                    # with the same scaling
                    file = open(prefile+".pik","wb")
                    print "Exporting as pickle..."
                    pik.dump(map,file)
                    file.close()
                    print "Exported!"
            except:
                print "Done (or an error...)!"
                break

    ScaleImages(1,hydroname,outrange)
    return

if __name__=="__main__":
    run()
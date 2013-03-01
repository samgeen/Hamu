#! /usr/bin/env python
# A revised version of testslice.py that uses the Hamu framework
# Provides a helper class that processes slices

import numpy as np
import pymses
from pymses.analysis.visualization import Camera, SliceMap, ScalarOperator
import pylab
import cPickle as pik
from SimData.Simulation import Simulation
from copy import copy

corner=True

fixmin = -4.5
fixmax = 6.0

class SliceMaker(object):
    def __init__(self,sim,hydrovar="rho",min=0.0,max=0.0,\
                     corner=True,scale=1.0):
        # Simulation name
        self._sim = sim
        # Hydro variables
        self._hydrovar = hydrovar
        # Range to set the colour bar with
        self._range = [min,max]
        # Temporary slice store
        self._slices = dict()
        # Align the slice with the corner?
        # TODO: Allow more fluid slice geometry
        self._corner = corner
        # Scale of box to display in
        # (1.0 is the whole box, 0.5 is half the box, etc)
        self._scale = scale

    # PUBLIC METHODS--------------

    # Make slices for all of the objects in a simulation
    def MakeAll(self):
        self._RunThroughSlices(self._sim)

    # Make slices for just one output
    def MakeSingle(self, nout):
        # Find snapshot at the given output number
        snap = self._sim[nout]
        # Run through this one snapshot
        self._RunThroughSlices([snap])

    # PROTECTED METHODS-----------

    # Internal function that runs through the slices in a container
    def _RunThroughSlices(self, snaps):
        # Run through all the snapshots
        print "Loading slice maps"
        for snap in snaps:
            print "Output: ", snap.iout
            # Pre-process the slices (makes float arrays)
            self._PreProcess(snap)
            # Find the min/max if our range is zero
            range = [1]
            if self._range[0] == self._range[1]:
                snaprange = self._FindMinMax(snap)
                if len(range) == 1:
                    range = snaprange
                else:
                    range = [np.min(range[0],snaprange[0]), \
                             np.max(range[1],snaprange[1])]
            else:
                range = copy(self._range)
        # Run through them all again now that we have the range
        print "Making images"
        for snap in snaps:
            # Make the images
            self._MakeImage(snap, range)
        # Clean up
        print "Cleaning up"
        self._slices.clear()
        print "Done"

    # Pre-process the slices
    def _PreProcess(self, snap):
        var = self._hydrovar
        prefile = self._Prefix(snap)
        # Do we not already have the .pik file?
        import os
        pikfilename = prefile+".pik"
        if os.path.isfile(pikfilename):
            file = open(pikfilename,"rb")
            map = pik.load(file)
            file.close()
        else:
            amr = snap.amr_source([var])
            # Make camera + slice function
            print "Setting up data slice"
            cam  = Camera(center=[0.5, 0.5, 0.5], line_of_sight_axis='z', \
                          region_size=[self._scale, self._scale],\
                          up_vector='y', map_max_size=1024, log_sensitive=True)
            rho_op = ScalarOperator(lambda dset: dset[var])
            # Start plotting the density slice
            print "Plotting data slice"
            islice = 0
            zarr = [0.0]
            # Measure the slice from the corner of the box?
            if self._corner:
                zarr = [-0.5]
            # Step through slices (currently only doing the central slice)
            # TODO: self_Prefix WILL MESS UP IF len(zarr) > 1
            for iz in zarr:
                map = SliceMap(amr, cam, rho_op, z=iz)
                # Save data as a pickle
                file = open(pikfilename,"wb")
                pik.dump(map,file)
                file.close()
        # Load map into temporary memory
        self._slices[snap.iout] = map

    # Find the min/max of an image
    # NOTE: _Preprocess MUST ALREADY HAVE BEEN CALLED TO LOAD self._slices
    def _FindMinMax(self, snap):
        map = self._slices[snap.iout]
        maxim = np.max(map)
        minim = np.min(map)
        return [minim, maxim]

    def _MakeImage(self, snap, range):
        print "SNAP.IOUT: ", snap.iout
        map = self._slices[snap.iout]
        scmap = (map - range[0]) / (range[1] - range[0])
        # Output scaled map
        prefile = self._Prefix(snap)
        print "Saving image: ", prefile+".png"
        pylab.imsave(prefile+".png", scmap,format="png", \
                     vmin = 0, vmax = 1)

    # Filename prefix (i.e. file = prefix.pik, prefix.png, etc)
    def _Prefix(self, snap):
        snapnum = snap.iout
        slicenum = 1 # TODO: ALLOW DIFFERENT SLICE POSITIONING
        imfile = "slice"
        name = ""
        if self._hydrovar != "rho":
            name = self._hydrovar
        # Make slice folder
        import os
        if not os.path.isdir("slices"+name):
            os.system("mkdir slices"+name)
        snapstr = '%(num)05d' % {'num': snapnum}
        return "slices"+name+"/"+imfile+snapstr+"_"+str(slicenum)

from pymses import RamsesOutput
from pymses.utils.regions import Sphere
from pymses.filters import CellsToPoints
from pymses.analysis import sample_points
from pymses.analysis import bin_spherical
from pymses.filters import RegionFilter
from pymses.filters import CellsToPoints
from pymses.sources.ramses.octree import RamsesOctreeReader as ROR
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pik

# Turns velocities in Pymses classes into speeds
# Note to self: Do not make up function names while tired
def SpeedMachine(source,posns):
    # Get velocity
    v = source["vel"]
    # Find speed
    speed = np.sqrt(v[:,0]**2. + v[:,1]**2. +v[:,2]**2.)
    # Insert new data source
    source.add_vectors("spd",speed)
    # Done!

# Turns velocities in Pymses classes into radial velocities
def VRad(source,posns):
    # Get velocity and position
    v = source["vel"]
    p = posns
    # Find radial velocity
    vp = v[:,0]*p[:,0] + v[:,1]*p[:,1] + v[:,2]*p[:,2]
    pmag = np.sqrt(p[:,0]**2. + p[:,1]**2. +p[:,2]**2.)
    vrad = vp / pmag
    # Insert new data source
    source.add_vectors("vrad",vrad)
    # Done!

# Turns velocities in Pymses classes into "turbulent" velocities
# This is all non-radial 
def VTurb(source,posns):
    # Find speed
    SpeedMachine(source,posns)
    VRad(source,posns)
    # Get radial velocity and all-velocity
    vr = source["vrad"]
    s = source["spd"]
    # Turbulent velocity = all non-radial velocity
    # NOTE: speed = v_rad^2 + v_perp^2
    # TODO: DO WE MULTIPLY THIS BY 3/2 TO INCLUDE RADIAL TURBLENT MOTION? !!!
    vturb = np.sqrt(s**2. - vr**2.)
    # Insert new data source
    source.add_vectors("vturb",vturb)
    # Done!

# TODO - Polymorphic with particles, make non-spherical?
class ProfileMaker(object):
    def __init__(self, snap):
        self._snap = snap
        self._centre = [0.5,0.5,0.5]
        self._radius = 1.

    def Shape(self, centre, radius):
        self._centre = centre
        self._radius = radius

    # Make a profile with a given hydro var
    def MakeProfile(self, hydrovar,):
        specials = ["spd","vrad","vturb"]
        # Get data from snapshot
        # If the field is speed ("spd"), derive it from vel

        # Add MEETAAAAAAALS
        if hydrovar == "Z":
            ROR.fields_by_file = {"hydro" : [ ROR.Scalar("rho", 0), \
                                              ROR.Vector("vel", [1, 2, 3]), \
                                              ROR.Scalar("P", 4), \
                                              ROR.Scalar("Z", 5) ],\
                                  "grav"  : [ ROR.Vector("g", [0, 1, 2]) ]}
        if not hydrovar in specials:
            amr = self._snap.amr_source([hydrovar])
        else:
            amr = self._snap.amr_source(["vel"])
        # Monte-carlo sample AMR cells
        sphere = Sphere(self._centre,self._radius)
        points = sphere.random_points(1.0e6)
        # If corner, cull -ve positions
        if np.max(self._centre) == 0.0:
            pve = points[:,0] >= 0.0
            points = points[pve,:]
            pve = points[:,1] >= 0.0
            points = points[pve,:]
            pve = points[:,2] >= 0.0
            points = points[pve,:]
        samples = sample_points(amr, points)
        posns = points - self._centre
        # HACK - DEBUG POSNS
        '''
        import matplotlib as pyplot
        plt.scatter(posns[:,0],posns[:,1])
        plt.savefig("testpoints.pdf",format="pdf")
        import pdb
        pdb.set_trace()
        '''
        if hydrovar == "spd":
            # Find speed
            SpeedMachine(samples,posns)
        if hydrovar == "vrad":
            # Find speed
            VRad(samples,posns)
        if hydrovar == "vturb":
            # Find speed
            VTurb(samples,posns)
        # Make bins
        weight_func = lambda dset: dset[hydrovar]
        r_bins = np.linspace(0.0, self._radius, 200)
        # Make profile
        profile = bin_spherical(samples, self._centre,weight_func, r_bins, divide_by_counts=True)
        r_bins = r_bins[1:len(r_bins)]
        return (r_bins,profile)

    # Sample amr cells
    def _SampleCells(self,sample):
        cell_source = CellsToPoints(amr)
        return cell_source.flatten()

'''
Created on Nov 28, 2012

@author: samgeen
'''

import numpy as np
from analysis.shockfront.shockfront import SnapProfileMax
from pymses.utils.regions import Sphere
from pymses.analysis import sample_points
from pymses.utils import constants as C

class HydroSamples(object):
    '''
    Object that preloads and holds hydro data from Pymses to prevent multiple/unnecessary loads
    '''
    def __init__(self, snap, variables, points, numSamples = 1e6):
        self._vars = variables
        self._points = points
        self._numSamples = numSamples
        # Set up access dictionaries (leave data empty for now; fill on demand)
        self._amrs = dict()
        self._data = dict()
        for var in self._vars:
            self._amrs[var] = snap.amr_source([var])
        
    def __getitem__(self, var):
        '''
        Get a data item and, if necessary, get the data first
        '''
        if not var in self._vars:
            print "No variable of name '"+var+"' in this HydroSamples object"
            print "Valid values:", self._vars
            raise KeyError
        if not var in self._data:
            self._data[var] = sample_points(self._amrs[var], self._points)
        # Note: The double [var][var] is because Pymses needs to know the variable type, too
        return self._data[var][var]
            
    def NumSamples(self):
        return self._numSamples
            

class SimpleWeighter(object):
    '''
    Simple, "default" weighter
    '''
    def __init__(self):
        self._name = "count"
        self._label = "Count"
        self._setup = False
        self._data = None
        self._points = None
        self._numSamples = 1e5
        self._snap = None
    
    def Name(self):
        '''
        Simple name to use in the code as an ID
        '''
        return self._name
    
    def NumSamples(self):
        return self._numSamples
    
    def _SetupData(self,snap):
        '''
        Set up the snapshot data for sampling by the functions in this object
        '''
        if not self._setup or snap != self._snap:
            # Get random points inside the maximum radius extent
            # NOTE: THIS IS A HUGE HACK DEPENDING ON WHAT YOU'RE PLOTTING A HISTOGRAM OF
            #       ONLY WORKS FOR BOX-CENTRE SPHERICAL SHOCK SIMULATIONS
            rmax = SnapProfileMax(snap,snap.output_repos)
            sphere = Sphere([0.5,0.5,0.5],rmax)
            self._points = sphere.random_points(self._numSamples)
            # Make a data object for loading the data on demand
            self._data = HydroSamples(snap,["P","rho","vel"],self._points)
            self._setup = True
    
    def Label(self):
        '''
        Label to print on plots, etc
        '''
        return self._label
    
    def Weighting(self, snap):
        '''
        Return the weight in a snapshot
        '''
        self._SetupData(snap)
        return np.zeros(self._numSamples)+(1.0 / self.NumSamples())
    
    def Temperature(self, snap):
        '''
        Snapshot temperature array
        '''
        self._SetupData(snap)
        T = self._data["P"] / self._data["rho"] \
                * snap.info["unit_temperature"].express(C.K)
        return T
    
    def Density(self, snap):
        '''
        Snapshot density array
        '''
        self._SetupData(snap)
        D = self._data["rho"] * snap.info["unit_density"].express(C.H_cc)
        return D
    
    def Velocity(self, snap):
        '''
        Snapshot velocity array
        '''
        self._SetupData(snap)
        D = self._data["vel"] \
            * snap.info["unit_length"].express(C.cm)/snap.info["unit_time"].express(C.s)
        return D

class MassWeighter(SimpleWeighter):
    '''
    Weight by mass
    '''
    def __init__(self):
        SimpleWeighter.__init__(self)
        self._name = "mass"
        self._label = "Mass"
    
    def Weighting(self, snap):
        '''
        Return the weight in a snapshot
        '''
        dens = self.Density(snap)
        return dens / np.sum(dens)
    
class KEWeighter(SimpleWeighter):
    '''
    Weight by kinetic energy fraction
    '''
    def __init__(self):
        SimpleWeighter.__init__(self)
        self._name = "ke"
        self._label = "Kinetic Energy Fraction"
    
    def Weighting(self, snap):
        '''
        Return the weight in a snapshot
        '''
        kBcgs = 1.3806488e-16
        vel = self.Velocity(snap)
        temp = self.Temperature(snap)
        # Finds the speed squared by summing over vel*vel in each 3-vector element
        spdSqrd = np.sum(vel*vel,1) 
        # Now find the partition of KE / (KE + TE) where TE = (3/2).kB.T and KE = (1/2)|v|^2 
        partition = 1.0 / (1.0 + (3.0*kBcgs*temp/spdSqrd))
        return partition / np.sum(partition)
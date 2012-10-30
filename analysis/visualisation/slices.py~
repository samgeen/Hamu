# Access script for making slices
# Uses SliceMaker.py
# Sam Geen, May 2012

from SliceMaker import SliceMaker
from SimData.Simulation import Simulation

# Default location is the pwd, use corner slices by default
def runall(corner=True,location=".",hydrovar="rho"):
    # Give the simulation a blank name
    sim = Simulation("",location)
    # Run the SliceMaker
    sm = SliceMaker(sim,hydrovar,corner=corner)
    sm.MakeAll()

# Default location is the pwd, use corner slices by default
def runone(nout,corner=True,location=".",hydrovar="rho"):
    # Give the simulation a blank name
    sim = Simulation("",location)
    # Run the SliceMaker
    sm = SliceMaker(sim,hydrovar,corner=corner)
    sm.MakeSingle(nout)

# DEFAULT: Run runall with default settings
if __name__=="__main__":
    runall()

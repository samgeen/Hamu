# Compare two profiles from 2 simulations
# Sam Geen, Feb 2012

from pymses import RamsesOutput
from ProfileMaker import ProfileMaker
import matplotlib.pyplot as plt

# sim1,sim2 are tuples of form:
# (outputname,outputnumber) e.g. (102,"./mysim1")
# Hydrovar is a string of one of the variables accepted by ProfileMaker
def comparesims(sim1,sim2,hydrovar):
    # Unpack tuples
    out1,name1 = sim1
    out2,name2 = sim2
    # Load snapshots
    snap1 = RamsesOutput(name1, out1)
    snap2 = RamsesOutput(name2, out2)
    # Load profiles
    pm1 = ProfileMaker(snap1)
    pm2 = ProfileMaker(snap2)
    r,p1 = pm1.MakeProfile(hydrovar)
    r,p2 = pm2.MakeProfile(hydrovar)
    # Difference the shit out of them
    fracdiff = 2.*(p2-p1)/(p2+p1)
    # THE SHIT OUT OF THEM
    # THE SHIT
    # SHIT
    # I forgot what I was doing. Oh yeah.
    # Plot frac diff
    plt.plot(r,fracdiff)
    plt.savefig("compareprof_frac.pdf",format="pdf")
    plt.clf()
    # Plot p1
    plt.plot(r,p1)
    plt.savefig("compareprof_p1.pdf",format="pdf")
    plt.clf()
    # Plot p2
    plt.plot(r,p2)
    plt.savefig("compareprof_p2.pdf",format="pdf")
    plt.clf()
    # END
    print "Donenated." 


def UnitTest():
    sim1 = (178,"./13_adiaconst_exactsolver")
    sim2 = (164,"./19_hybrid_superlowthresh")
    comparesims(sim1,sim2,"P")

if __name__=="__main__":
    UnitTest()

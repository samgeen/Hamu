# Field length profile plotter
# Let's try using YT this time

from yt.mods import * # set up our namespace

def Field(outnum):


    numstr = "%(num)05d" % {"num": outnum}

    fn = "output_"+numstr+"/info_"+numstr+".txt" # parameter file to load
    
    pf = load(fn) # load data

    pc = PlotCollection(pf, [0.05, 0.05, 0.05])
    d = pc.add_profile_sphere(1.0, "pc", # how many of which unit at pc.center
                          ["Radiuspc", "Density"], # x, y, weight
                          x_bounds = (1e-1, 10.0))  # cut out zero-radius and tiny-radius cells
# But ... weight defaults to CellMassMsun, so we're being redundant here!
    
    p = pc.add_profile_sphere(1.0, "mpc", # how many of which unit at pc.center
                          ["Radiuspc", "Pressure"], # x, y, weight
                          x_bounds = (1e-1, 10.0))  # cut out zero-radius and tiny-radius cells

    pc.save(fn) # save all plots

    #import pdb
    #pdb.set_trace()
    

if __name__=="__main__":
    Field(100)

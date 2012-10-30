# Removes all outputs not ending in "1" from the pwd
# Sam Geen, May 2012

import os
import subprocess as sup
import shlex

def killfile(filename,verbose=False):
    if not os.path.isfile(filename):
        if verbose:
            print "Killing file "+filename
        os.system("rm -rf "+filename)
    else:
        if verbose:
            print "No file "+file

def run(verbose=False):
    outs = list()
    # Find all files not ending in "_1"
    for i in [0,2,3,4,5,6,7,8,9]:
        outstr = "ls -d output_????"+str(i)
        out = sup.check_output(outstr,shell=True)
        for o in out.split("\n"):
            if len(o) > 0:
                outs.append(o)
    outs = sorted(outs)
    # REMOVE THE LAST OUTPUT FROM THE KILL LIST
    outs.pop()
    # KILL ALL FILES NOT ENDING IN "_1"
    for out in outs:
        killfile(out,verbose)



if __name__=="__main__":
    run()

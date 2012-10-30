# Take a slice and build a profile out of it

import cPickle as pik
import testslice as t
import matplotlib.pyplot as plt

if __name__=="__main__":
    
            prefile = t.Prefix(200, 1, "rho")
            file = open(prefile+".pik","rb")
            map = pik.load(file)
            file.close()
            profile = map[:,512]
            r = range(-512,512)
            for i in range(0,1024):
                r[i] /= 512.
                r[i] *= 0.05
            print len(r),len(profile)
            plt.plot(r,profile)
            plt.xlabel("radius / kpc")
            plt.ylabel("log(density / atoms/cc)")

            #plt.show()
            plt.savefig("scratch_sliceprofiler.pdf",format="pdf")

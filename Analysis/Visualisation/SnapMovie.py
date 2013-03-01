# Make a movie from a snapshot with varying output times
# Does this by copying multiple frames for long timesteps

import numpy as np
import os

class SnapMovie(object):
    # IMTYPE - Image file type (default: ".png")
    def __init__(self, imtype=".png"):
        self._imtype = ".png"
        self._images = np.array([])
        self._times = np.array([])
        self._folder = "./"
        # Max number of times to multiply a single frame
        self._maxmult = 20

    # Set the maximum number of frames allowed to multiply by
    # (A bigger number gives a better approximation but uses more time/space)
    def MaxMultiplier(self, multiplier):
        self._maxmult = np.max(np.array([multiplier, 1]))

    # Set the folder which the temporary files are put
    # (Default: "./", i.e. this directory)
    def SetFolder(self, foldername):
        self._folder = foldername

    # Append an image with a given timestamp (can be in any unit)
    # NOTE: time is the *absolute* time, not the length of the snapshot
    def Append(self, imagefilename, time):
        self._images.append(imagefilename)
        self._times.append(time)

    # Make the movie!
    def MakeMovie(self, moviefilename):
        # Find the multiples of each frame to use
        mults = self._FrameMultipliers()
        imnum = 1

        # Step through each image and make the input images
        for im,mult in zip(images, mults):
            # Copy the file by the number of times required
            for loop in range(0,mult):
                numstr = '%(num)05d' % {'num': imnum}
                os.system("cp "+im+" "+self._folder+$
                          "temporaryimage"+numstr+self._imtype)
                imnum = imnum+1

        # Call ffmpeg to make movie
        os.system("ffmpeg -r "+fps+\
            " -b 1800 "+\
            "-i %05d. "+self._imtype+\
            self._folder+moviefilename+".mp4")
        # TODO: CLEAN UP
        return
            

    # PROTECTED FUNCTIONS ONLY SNAPMOVIE CAN USE

    # Determine the number of frames to use for each image
    def _FrameMultipliers(self):
        # Find the time differences
        lengths = self._TimeDiff()
        # Determine the max/min lengths
        minr = np.min(lengths)
        maxr = np.max(lengths)
        # Find the multipliers from this
        # Min = 1, Max = self._maxmult
        mults = np.cast['float'](self._maxmult-1)*(lengths-minr)/(maxr-minr)
        # The above scales from 0 to self._maxmult-1, so add 1 to fix this 
        mults = np.cast['int'](mults)+1
        return mults
                               
    # Return the difference in times between each output
    def _TimeDiff(self):
        # Copy the absolute time list
        diffs = self._times.copy()
        i = 0
        prev = 0
        # diff[i] = t[i] - t[i-1] for i = 1..N-1
        for itt in times:
            if i > 0:
                itt -= prev
            i = i+1
            prev = itt
        # Return the result
        return diffs

# TODO: Write this
def UnitTest():
    pass

# Merge plot images and make a video
# Sam Geen, October 2012

import os
import Image

def mergeimages(name, num):
    numstr = '%(num)05d' % {'num': num}
    stub = name+numstr+"_"
    merged = stub+"merged.png"
    if not os.path.isfile(merged):
        # Open existing plots
        dens = Image.open(stub+"density.png")
        temp = Image.open(stub+"temperature.png")
        vrad = Image.open(stub+"velocity_radial.png")
        engy = Image.open(stub+"fractional_energy.png")
        # Make new big image
        width, height = dens.size
        blank_image = Image.new("RGB", (2*width,2*height))
        # Paste in old images
        blank_image.paste(dens, (0,0))
        blank_image.paste(temp, (width,0))
        blank_image.paste(vrad, (0,height))
        blank_image.paste(engy, (width,height))
        # Save big image
        blank_image.save(merged)

if __name__=="__main__":
    # Set up filenames
    stubs = ["profile_thornton_onlysn_",\
             "profile_cloud_onlysn_"]
    nums = range(0,99)
    for stub in stubs:
        print stub
        # Merge images
        for num in nums:
            print num
            mergeimages(stub,num)
        # Make movie
        print "Making movie for stub", stub
        os.system("convert "+stub+"*_merged.png "+stub+"plotsmovie.gif")

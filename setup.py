'''
Created on 13 Feb 2013

@author: samgeen
'''

import os
import sys

from Settings import Settings

# NOTE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ALL THIS CODE IS DEPRECATED AS SETTINGS.PY DOES THIS AUTOMATICALLY NOW!!!!!!!!!!!1
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

HOMEPATH = os.getenv("HOME")+"/.hamu/"

def Setup(path):
    # Set up home directory
    if not os.path.exists(path):
        print "No existing Hamu installation; setting up directory now"
        try:
            os.system("mkdir "+path)
            print "Hamu workspace installed to", path
        except:
            sys.exit("Error: Could not set up directory"+path)
    else:
        print "Directory "+path+ " exists; continuing with setup"
    # Set up settings file
    settings = Settings()
    settings["DataDir"] = HOMEPATH
    settings["CurrentWorkspace"] = "MyWorkspace"

if __name__=="__main__":
    print '''
      /\  /\__ _ _ __ ___  _   _ 
     / /_/ / _` | '_ ` _ \| | | |
    / __  / (_| | | | | | | |_| |
    \/ /_/ \__,_|_| |_| |_|\__,_|
    
    Helping your simulations to hug and make up
    Written by Sam Geen, 2013
    
    For use as-is; no responsibility accepted for damage to your computer, person or family pets
    NOTE: THIS IS CURRENTLY NOT A COMPLETE SETUP SCRIPT, BUT SOMETHING TO SET UP YOUR HAMU ENVIRONMENT
    ---------------------------------------------------------------------------------------------------
    '''
    # Set up directory to use
    Setup(HOMEPATH)


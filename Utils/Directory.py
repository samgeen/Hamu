'''
Created on 2 Mar 2012

@author: samgeen
'''

import os, sys
import subprocess as sp

# TODO: FILTER OUT REPEAT BACKSLASHES IN DIRECTORY NAMES

# Finds directories, makes directories, etc
class Directory(object):
    '''
    classdocs
    '''
    
    # path = directory's path in the file system (can be relative or absolute, provided you're consistent)
    def __init__(self,path=""):
        '''
        Constructor
        '''
        self._path = path+"/"
        # Make the directory if it doesn't already exist
        self._MakeDir()
    
    def Path(self):
        '''
        Return the directory path
        '''
        return self._path
    
    def ListItems(self):
        '''
        List items inside the directory (i.e. "ls DIRNAME")
        '''
        # Get search string in a list separated by spaces
        #search = "ls "+self._path
        #search = search.split(" ")
        # Get list of items found
        out = sp.check_output("ls "+self._path,shell=True).split("\n")
        # Remove empty item that always comes up in this function
        out = filter(None, out)
        return out
    
    def MakeSubdir(self, folder):
        '''
        Make a subdirectory of this directory
        '''
        return Directory(self._path+"/"+folder+"/")
    
    def _MakeDir(self,verbose=False):
        folders = self._path.split("/")
        if self._path[0] == "~":
            currdir = "~/"
            folders = folders[1:len(folders)]
        else:
            currdir = "/"
        for folder in folders:
            if len(folder)> 0:
                currdir += folder+"/"
                if not os.path.exists(currdir):
                    if verbose:
                        print "Making directory "+currdir+" now"
                    try:
                        os.system("mkdir "+currdir)
                        if verbose:
                            print "Directory", currdir, "made"
                    except:
                        sys.exit("Error: Could not set up directory "+currdir)
                else:
                    if verbose:
                        print "Directory "+currdir+ " exists already"

    def __str__(self):
        return self.Path()

if __name__=="__main__":
    path = "~/eggs/"
    dir = Directory(path)
    print Directory("~/Programming").ListItems()
    
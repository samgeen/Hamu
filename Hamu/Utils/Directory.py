'''
Created on 2 Mar 2012

@author: samgeen
'''

# Finds directories, makes directories, etc
class Directory(object):
    '''
    classdocs
    '''
    
    # location = directory's location in the file system (can be relative or absolute, provided you're consistent)
    def __init__(self,location=""):
        '''
        Constructor
        '''
        # Is the location iterable, i.e. a list of directories to concatenate?
        # Also, make sure we have a directory "/" at the end
        try:
            self._location = ""
            for loc in location:
                self._location += loc+"/"
        except TypeError:
            self._location = location+"/"

        
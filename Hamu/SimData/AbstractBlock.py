'''
Created on 2 Mar 2012

@author: samgeen
'''

# Abstract chunk of Hamu (e.g. Suite, Simulation, etc)
# Sets up a generic chunk with file location, allows the creation of children objects, etc
class AbstractBlock(object):
    '''
    classdocs
    '''

    # storeLocation: Where to store temporary data and dump figures?
    def __init__(self,storeLocation):
        '''
        Constructor
        '''
        self._storeLocation = storeLocation
        self._prepared = False
        self._children = list()
        
    # Initialise class
    def CheckPrepared(self):
        if not self._prepared:
            self._Prepare()
            self._prepared = True
            
    # Prepare the object for use; concrete class will need to instantiate this
    # DO NOT CALL THIS, CALL CHECKPREPARED INSTEAD
    def _Prepare(self):
        raise NotImplementedError
            
    # Add child; to be wrapped by the concrete class to be more descriptive (e.g. AddSnapshot, AddSimulation)
    def _AddChild(self, child):
        self._children.append(child)
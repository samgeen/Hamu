'''
Created on 19 Feb 2013

@author: samgeen
'''

import abc

class HamuIterable(object):
    '''
    Generic iterable for Hamu hierarchy objects
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @abc.abstractmethod
    def Snapshots(self):
        '''
        Return all the snapshots in this collection
        '''
        return
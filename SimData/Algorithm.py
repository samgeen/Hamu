'''
Created on 18 Feb 2013

@author: samgeen
'''

# Cache file imports
import hashlib
import cPickle as pik
import os

class CacheFile(object):
    def __init__(self, snapshot, algorithm):
        self._snapshot = snapshot
        self._algorithm = algorithm
        self._folder = snapshot.CachePath()
    
    def Save(self, data):
        # Save algorithm settings to a text file (for reference)
        pikfile = open(self._Filename("info"),"w")
        pik.dump(str(self._algorithm),pikfile)
        pikfile.close()
        # Save the output data to a binary file
        pikfile = open(self._Filename("data"),"wb")
        pik.dump(data,pikfile)
        pikfile.close()
        
    def Load(self):
        # Load the (binary) data file
        if self.Exists():
            pikfile = open(self._Filename("data"),"rb")
            print self._Filename("data")
            output = pik.load(pikfile)
            pikfile.close()
            return output
        else:
            return None
        
    def Exists(self):
        '''
        Does the cache file exist?
        '''
        return os.path.exists(self._algorithm.CacheFilename())
        
    def _Filename(self,ext="data"):
        '''
        Cache file's filename
        '''
        return self._folder+self._algorithm.CacheFilename(ext)

class Algorithm(object):
    '''
    A wrapper class around a function that enables us to run functions and store their outputs for later use
    '''

    def __init__(self, function, *args, **kwargs):
        '''
        Constructor
        function: A Python function object to call that accepts snapshot.RawData() as its first argument, and arg/kwarg after
        arg, kwarg: arguments accepted by function (see, e.g., http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/)
        ''' 
        self._function = function
        self._args = args
        self._kwargs = kwargs
        
    def Run(self, snap):
        '''
        Run for a single snapshot
        '''
        # First, get the cache filename and compare against existing files
        cache = CacheFile(snap, self)
        # Check to see if a cached dataset exists
        if cache.Exists():
            output = cache.Load()
        else:
            output = self._RunAlgorithm(snap)
            cache.Save(output)
        return output
        
    def _RunAlgorithm(self, snapshot):
        '''
        Unpack the algorithm and call the native python code
        '''
        raw = snapshot.RawData()
        output = self._function(raw, *self._args, **self._kwargs)
        return output
    
    def __str__(self):
        '''
        Parse this algorithm as a string (for writing to text file)
        '''
        out = ""
        out += "Function: "+self._function.__name__
        out += "\n"
        out += "Arguments: "+str(self._args)
        out += "\n"
        out += "Keyword Arguments: "+str(self._kwargs)
        out += "\n"
        return out
    
    def __call__(self, snapshot):
        '''
        Allows the algorithm to be called like a function
        '''
        return self.Run(snapshot)
    
    def CacheFilename(self, ext="data"):
        '''
        Return the name of this algorithm's cache file
        Uses a hash function to hash the arguments of the function
        ext - File extension (used for writing multiple cache files; default is ".data")
        '''
        objName = self._function.__name__
        hash = hashlib.sha1(str(self._args)).hexdigest()
        hash += hashlib.sha1(str(self._kwargs)).hexdigest()
        filepre = objName+hash
        return filepre+"."+ext
    
    # DEPRECATED - RUN CODE ON ALL OBJECTS IN A HamuIterable
    #def Run(self, hamuIterable):
    #    '''
    #    Run for all snapshots in a given iterable
    #    '''
    #    # Check to see whether this snapshot already has data
    #    outputs = list()
    #    for snap in hamuIterable.Snapshots():
    #        outputs.append(self.RunForSnap(snap))
    #    return outputs
    
'''
Load options from the command line
Sam Geen, July 2013
'''

import sys

def Arg1(default=None):
    '''
    Read the first argument
    default: Default value to return if no argument is found
    Return: First argument in sys.argv (minus program name) or default if none
    '''
    if len(sys.argv) < 2:
        return default
    else:
        return sys.argv[1]

if __name__=="__main__":
    print "Test Arg1():"
    print Arg1()
    print Arg1("Bumface")

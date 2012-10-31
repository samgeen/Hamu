# RAMLOG.PY - ANALYSES THE RAMSES LOG FILE FOR PERFORMANCE
from RamLogParser import RamLogParser
import getopt
import sys

# Run through each line of the file and create the array of data
def Run(inname,outname) :
    print "Running Ramses log file parser"
    # Create ramses log file parser
    parser = RamLogParser()
    print "Parsing log file ", inname
    parser.ParseFile(inname)
    print "Outputting to ", outname
    parser.Output(outname)
    print "Done!"
    # Open file and run through each line
    return

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:],"")
    Run(args[0],args[1])

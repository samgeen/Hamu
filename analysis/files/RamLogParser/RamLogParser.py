#! /usr/bin/env python
# Parses a line of a ramses log file  (i.e. the screen text dump)
#    and puts the results into an array

import numpy as np
import getopt
import sys

class RamLogParser(object):
    '''
    Parses a line of a Ramses log file
    '''

    def __init__(self):
        self._table = np.empty([5,100000],dtype=float)
        self._currline = 0

    # Parse a RAMSES log file
    def ParseFile(self, filename):
        infile = open(filename)
        filetxt = infile.read()
        infile.close()
        for line in filetxt.split('\n') :
            self.ParseLine(line)
        
    # Find a variable in a string
    def FindVar(self, line, name, name2="step="):
        i = 0
        done = false
        spl = line.split(" ")
        while not done:
            # Check name (and 2nd name?)
            if spl[i] == name:
                if spl[i+1] == name2 or name2 == "":
                    # BLEH.
                    pass

    # Strip out empty string list entries
    def _StripEmpty(self, spl):
        newSpl = list()
        for its in spl:
            if len(its) > 0:
                newSpl.append(its)
        return newSpl

    # Import a line of text and parse it
    # FORMAT: 
    # Fine step=  1361 t= 5.39164E-03 dt= 3.988E-06 a= 1.000E+00 mem= 2.2%
    def ParseLine(self, line):

        # Run through to find each variable
        #fineStep = FindVar(line, "Fine", "step=")

        spl = line.split(" ")
        
        # Strip empty entries
        spl = self._StripEmpty(spl)

        # Safety check the upcoming loop
        if len(spl) < 3:
            return

        # Check for valid line (VERY dodgy diagnostic...)
        if spl[0] == "Fine" and spl[1] == "step=":
            # DEBUG
            #i = 0
            #for its in spl:
            #    print its, i
            #    i += 1
            # Pick numbers (TODO: More robust selection!)
            fineStep = spl[2]
            time = spl[4]
            dt = spl[6]
            scale = spl[8]
            # Check whether memory number is included in its string
            memstr = spl[9]
            if len(memstr) > 4:
                mempc = memstr[4:]
            else:
                mempc = spl[10]
            # We need to parse mem specially, e.g. mem=11.6% -> 11.6
            # (there's no space after the = and strip the % sign)
            mempc = mempc[0:len(mempc)-1]
            #print fineStep, time, dt, scale, mempc
            self._table[0,self._currline] = fineStep
            self._table[1,self._currline] = time
            self._table[2,self._currline] = dt
            self._table[3,self._currline] = scale
            self._table[4,self._currline] = mempc
            # Increment the current line number
            self._currline += 1

    # Output to ascii file
    def Output(self, filename):
        # Open file
        outfile = open(filename,'w')
        # Print table headers
        print >> outfile, "Fine_step Time dt scale_factor Memory%"
        # Loop through lines
        for i in range(0,self._currline+1):
            print >> outfile, \
                self._table[0,i], \
                self._table[1,i], \
                self._table[2,i], \
                self._table[3,i], \
                self._table[4,i]
        # CLOSE FILE. CLOSE IT CLOSEAAAAARGH-
        outfile.close()
        # -There. It's done.
        return

# Run through each line of the file and create the array of data
def Run(inname,outname) :
    print "Running Ramses log file parser"
    print "------------------------------"
    # Create ramses log file parser
    parser = RamLogParser()
    print "Parsing log file", inname
    parser.ParseFile(inname)
    print "Outputting to", outname
    parser.Output(outname)
    print "Done!"
    # Open file and run through each line
    return

if __name__ == '__main__':
    # Set up input filenames
    opts, args = getopt.getopt(sys.argv[1:],"")
    inname = args[0]
    outname = ""
    if len(args) < 2:
        outname = "log.txt"
    else:
        outname = args[1]
    # Run!
    Run(inname, outname)

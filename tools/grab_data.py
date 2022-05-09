#!/usr/bin/python3

#####################################################################################
# Copyright (c) 2021 Marijn Heule, Randal E. Bryant, Carnegie Mellon University
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
########################################################################################

import sys
import re

# Generate csv of number specified on target line
# Extracts problem size from file name.

def usage(name):
    print("Usage: %s [nth] tphrase file ...")
    print(" nth: Look for nth numeric field in line (count from 1)")


# Will grep for line containing trigger phrase.
# This should be provided as the first argument to the program.
# If it contains a space, be sure to quote it.

# Check first argument.  If has any sequence of digits, then assume this is a number
# to indicate the numeric field number for the triggering line.
# (Numbered from 1)

triggerField = 1
triggerPhrase = "Total Clauses"

def trim(s):
    while len(s) > 0 and s[-1] == '\n':
        s = s[:-1]
    return s

# Sequence of one or more digits
inumber = re.compile('[\d]+')

dashOrDot = re.compile('[.-]')
def ddSplit(s):
    return dashOrDot.split(s)

colonOrSpace = re.compile('[\s:]+')
def lineSplit(s):
    return colonOrSpace.split(s)

def nthNumber(fields, n = 1):
    count = 0
    for field in fields:
        try:
            val = int(field)
            count += 1
            if count == n:
                return val
        except:
            try:
                val = float(field)
                count += 1
                if count == n:
                    return val
            except:
                if field[-1] == 's':
                    field = field[:-1]
                    try:
                        val = float(field)
                        count += 1
                    except:
                        continue
                else:
                    continue
    return -1


# Extract clause data from log.  Turn into something useable for other tools
def extract(fname):
    # Try to find size from file name:
    try:
        m = re.search(inumber, fname)
        n = int(m.group(0))
    except:
        print("Couldn't extract problem size from file name '%s'" % fname)
        return None
    try:
        f = open(fname, 'r')
    except:
        print("Couldn't open file '%s'" % fname)
        return None
    val = None
    for line in f:
        line = trim(line)
        if triggerPhrase in line:
            fields = lineSplit(line)
            val = nthNumber(fields, triggerField)
    f.close()
    if val is None:
        return None
    return (n, val)

def usage(name):
    print("Usage: %s tphrase file1 file2 ..." % name)
    sys.exit(0)

def run(name, args):
    if len(args) < 2 or args[0] == '-h':
        usage(name)
        return
    global triggerPhrase
    global triggerField
    vals = {}
    try:
        triggerField = int(args[0])
        triggerPhrase = args[1]
        names = args[2:]
    except:
        triggerPhrase = args[0]
        names = args[1:]
    for fname in names:
        pair = extract(fname)
        if pair is not None:
            if pair[0] in vals:
                vals[pair[0]].append(pair)
            else:
                vals[pair[0]] = [pair]
    for k in sorted(vals.keys()):
        for p in vals[k]:
            print("%s,%s" % p)

if __name__ == "__main__":
    run(sys.argv[0], sys.argv[1:])

            
        
                

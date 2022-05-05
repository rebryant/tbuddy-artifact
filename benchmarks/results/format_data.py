
#####################################################################################
# Copyright (c) 2022 Randal E. Bryant, Carnegie Mellon University
# Last edit: May 08, 2022
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
import csv

# Generate tabbed data of numbers specified on target lines
# Extracts problem size from file name

experiments = [
    "chess-scan",
    "pigeon-scan",
    "chew-bucket",
    "chew-gauss",
    "urquhart-bucket",
    "urquhart-gauss",
]

measurements = [
    # Name of .csv file, column heading, field width
    (None, "Benchmark"),  # Leftmost field
    (None, "Size"),
    ("input-variables", "In Var"),
    ("input-clauses", "In Cls"),
    ("sat-seconds", "SAT Sec"),
    ("proof-clauses", "Pf Cls"),
    ("check-seconds", "Chk Sec"),
]

# Field widths
widths = [
    len('urquhart-bucket') + 2,
    8,
    10,
    12,
    10,
    12,
    10
]

# Generate fixed width representations of int's, floats, and strings
class Justify:
    left, right, center = range(3)
    defaultWidth = 8
    decimals = 1
    insertCommas = True
    justification = None

    def __init__(self, width = None, decimals = None, commas = None, defaultJustification = None):
        if width is not None:
            self.defaultWidth = width
        if decimals is not None:
            self.decimals = decimals
        if commas is not None:
            self.insertCommas = commas
        self.defaultJustification = self.left if defaultJustification is None else defaultJustification

    def jstring(self, s, width = None, justification = None):
        width = self.defaultWidth if width is None else width
        if justification is None:
            if self.justification is not None:
                justification = self.justification
            elif self.defaultJustification is not None:
                justification = self.defaultJustification
            else:
                justification = self.center

        if len(s) > width:
            s = s[:width]

        length = len(s)
        spacing = width-length
        lspace = 0
        rspace = 0
        if justification == self.left:
            rspace = spacing
        elif justification == self.right:
            lspace = spacing
        else:
            lspace = spacing//2
            rspace = spacing-lspace
        return " " * lspace + s + " " * rspace
        
    def stringify(self, o):
        if type(o) == type(123):
            s = str(o)
            if self.insertCommas:
                ns = ""
                while len(s) > 3:
                    right = s[-3:]
                    s = s[:-3]
                    ns = ',' + right + ns
                s = s + ns
            self.justification = self.right
        elif type(o) == type(123.0):
            fstring = "%." + str(self.decimals) + "f"
            s = fstring % o
            self.justification = self.right
        else:
            s = str(o)
            self.justification = None
        return s

    def format(self, o, width = None, justification = None):
        s = self.stringify(o)
        return self.jstring(s, width, justification)

    def delimit(self, symbol = '-', width = None):
        width = self.defaultWidth if width is None else width
        return symbol * (width) 

def header():
    jfy = Justify(defaultJustification = Justify.center)
    s = ""
    for idx in range(len(measurements)):
        m = measurements[idx]
        width = widths[idx]
        field = m[1]
        s += jfy.format(field, width = width)
    return s
    
def delimiter(symbol = '-'):
    jfy = Justify()
    s = ""
    for idx in range(len(measurements)):
        width = widths[idx]
        s += jfy.delimit(symbol = symbol, width = width)
    return s

def formatLine(args):
    jfy = Justify()
    s = ""
    for idx in range(len(args)):
        arg = args[idx]
        width =  widths[idx]
        s += jfy.format(arg, width = width)
    return s
    
def csvName(experiment, measurement):
    if measurement is None:
        return None
    return experiment + '/' + experiment + '-' + measurement + ".csv"

def convert(s):
    try:
        obj = int(s)
        return obj
    except:
        try:
            obj = float(s)
            return obj
        except:
            return s

def grab(experiment, measurement, mdict):
    fname = csvName(experiment, measurement)
    try:
        f =  open(fname, 'r')
    except:
        print("ERROR: Couldn't open file '%s'" % fname)
        return
    c = csv.reader(f)
    for fields in c:
        if len(fields) < 1:
            continue
        args = [convert(field) for field in fields]
        key = args[0]
        if key not in mdict:
            mdict[key] = [key]
        for arg in args[1:]:
            mdict[key].append(arg)
    f.close()
    
def process(experiment):
    mdict = {}
    for m in measurements[2:]:
        grab(experiment, m[0], mdict)
    klist = sorted(mdict.keys())
    for k in klist:
        args = [experiment] + mdict[k]
        print(formatLine(args))

def run():
    dlim = delimiter()
    print(header())
    for e in experiments:
        print(dlim)
        process(e)
    print(dlim)

if __name__ == "__main__":
    run()

            
        
                

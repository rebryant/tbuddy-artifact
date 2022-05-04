#!/usr/bin/python
#####################################################################################
# Copyright (c) 2022 Randal E. Bryant, Carnegie Mellon University
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


# Convert CNF file containing only xor declarations into
# schedule file that converts these into pseudo-Boolean equations
# triggers Gauss-Jordan elimination
# and loads any remaining clauses.
# The solver should then shift to bucket elimination

import getopt
import sys
import glob
import datetime

import exutil

def csvWrite(csvFile, ls):
    slist = [str(v) for v in ls]
    csvFile.write(",".join(slist) + '\n')

def usage(name):
    exutil.ewrite("Usage: %s [-v VLEVEL] [-h] [-c] [-l CFILE] [-i IN.cnf] [-o OUT.schedule] [-d DIR] [-m MAXCLAUSE]\n" % name, 0)
    exutil.ewrite("  -h       Print this message\n", 0)
    exutil.ewrite("  -v VERB  Set verbosity level (1-4)\n", 0)
    exutil.ewrite("  -c       Careful checking of CNF\n", 0)
    exutil.ewrite("  -l CFILE Write data in CSV format to file\n", 0)
    exutil.ewrite("  -i IFILE Single input file\n", 0)
    exutil.ewrite("  -o OFILE Single output file\n", 0)
    exutil.ewrite("  -p PATH  Process all CNF files with matching path prefix\n", 0)
    exutil.ewrite("  -m MAXC  Skip files with larger number of clauses\n", 0)

startTime = None


class Xor:
    # Input clauses
    clauses = []
    # Mapping from list of variables to the clauses containing exactly those variables
    varMap = {}
    msgPrefix = ""
    variableCount = 0
    # Generate CSV version of data
    csvFile = None
    dataList = []

    def __init__(self, clauses, iname, nvar, csvFile = None):
        self.clauses = clauses
        self.variableCount = nvar
        self.varMap = {}
        self.csvFile = csvFile
        if iname is None:
            self.msgPrefix = iname
            dataList = [""]
        else:
            self.msgPrefix = "File %s: " % iname
            dataList = [iname]
        for idx in range(1, len(clauses)+1):
            clause = self.getClause(idx)
            clause.sort(key = lambda lit : abs(lit))
            vars = tuple(sorted([abs(l) for l in clause]))
            if vars in self.varMap:
                self.varMap[vars].append(idx)
            else:
                self.varMap[vars] = [idx]

    def getClause(self, idx):
        if exutil.careful and (idx < 1 or idx > len(self.clauses)):
            raise self.msgPrefix + "Invalid clause index %d.  Allowed range 1 .. %d" % (idx, len(self.clauses))
        return self.clauses[idx-1]

    # Given set of clause IDs  over common set of variables,
    # Return partitioning into three sets: xors, xnors, other
    def classifyClauses(self, idlist):
        xorClauses = []
        xnorClauses = []
        otherClauses = []
        xorNvals = []
        xnorNvals = []
        if len(idlist) == 0:
            return (xorClauses, xnorClause, otherClauses)
        c0 = self.getClause(idlist[0])
        tcount = 2**(len(c0)-1)
        for id in idlist:
            clause = self.getClause(id)
            nlist = [1 if lit < 0 else 0 for lit in clause]
            nval = sum([nlist[i] * 2**i for i in range(len(nlist))])
            # Xor will have even number of negative literals
            if sum(nlist) % 2 == 0:
                xorClauses.append(id)
                xorNvals.append(nval)
            else:
                xnorClauses.append(id)
                xnorNvals.append(nval)
        # See if have true xors or true xnors
        nset = set(xorNvals)
        if len(nset) != tcount:
            otherClauses = otherClauses + xorClauses
            xorClauses = []
        nset = set(xnorNvals)
        if len(nset) != tcount:
            otherClauses = otherClauses + xnorClauses
            xnorClauses = []
        return (xorClauses, xnorClauses, otherClauses)
        
    def emitX(self, idlist, phase, outfile):
        slist = [str(id) for id in idlist]
        outfile.write("c %s\n" % " ".join(slist))
        if (len(idlist) > 1):
            outfile.write("a %d\n" % (len(idlist)-1))
        vars = [abs(lit) for lit in self.getClause(idlist[0])]
        stlist = ['1.%d' % v for v in vars]
        outfile.write("=2 %d %s\n" % (phase, " ".join(stlist)))

    def mapClauses(self, idlist, map):
        for id in idlist:
            clause = self.getClause(id)
            for lit in clause:
                map[abs(lit)] = True

    def generate(self, oname, multiFile):
        if oname is None:
            outfile = sys.stdout
        else:
            try:
                outfile = open(oname, 'w')
            except:
                exutil.ewrite("%sCouldn't open output file '%s'\n" % (self.msgPrefix, oname), 1)
                return False
        idlists = list(self.varMap.values())
        clauseCount = 0
        xcount = 0
        otherIdList = []
        xmap = {}
        omap = {}
        for idlist in idlists:
            clauseCount += len(idlist)
            (xorClauses, xnorClauses, otherClauses) = self.classifyClauses(idlist)
            if len(xorClauses) > 0:
                self.mapClauses(xorClauses, xmap)
                self.emitX(xorClauses, 1, outfile)
                xcount += 1
            if len(xnorClauses) > 0:
                self.mapClauses(xnorClauses, xmap)
                self.emitX(xnorClauses, 0, outfile)
                xcount += 1
            otherIdList += otherClauses
            self.mapClauses(otherClauses, omap)
        ivars = []
        if (xcount > 0):
            for v in xmap.keys():
                if v not in omap:
                    ivars.append(v)
            slist = [str(v) for v in sorted(ivars)]
            outfile.write("g %d %s\n" % (xcount, " ".join(slist)))
        if len(otherIdList) > 0:
            slist = [str(id) for id in sorted(otherIdList)]
            outfile.write("c %s\n" % " ".join(slist))
        if oname is not None:
            outfile.close()
        seconds = 0.0
        if startTime is not None:
            delta = datetime.datetime.now() - startTime
            seconds = delta.seconds + 1e-6 * delta.microseconds
        if multiFile:
            if self.csvFile is not None:
                self.dataList += [xcount, clauseCount, len(otherIdList), self.variableCount, len(ivars), "%.2f" % seconds]
                csvWrite(self.csvFile, self.dataList)
            exutil.ewrite("%s%d equations" % (self.msgPrefix, xcount), 1)
            exutil.ewrite(", %d clauses (%d non-xor)" % (clauseCount, len(otherIdList)), 1)
            exutil.ewrite(", %d variables (%d internal)" % (self.variableCount, len(ivars)), 1)
            if seconds is None:
                exutil.ewrite("\n", 1)
            else:
                exutil.ewrite(", %.2f seconds\n" % seconds, 1)
        else:
            exutil.ewrite("%s\n" % self.msgPrefix, 1)
            exutil.ewrite("    Equations extracted: %d\n" % xcount, 1)
            exutil.ewrite("    Input clauses: %d\n" % clauseCount, 1)
            exutil.ewrite("    Non-xor clauses: %d\n" % len(otherIdList), 1)
            exutil.ewrite("    Total variables: %d\n" % self.variableCount, 1)
            exutil.ewrite("    Internal variables: %d\n" % len(ivars), 1)
            if seconds is not None:
                exutil.ewrite("    Extraction seconds: %.2f\n" % seconds, 1)

        return True
        
def extract(iname, oname, maxclause, multiFile, csvFile):
    global startTime
    startTime = datetime.datetime.now()
    try:
        reader = exutil.CnfReader(iname, maxclause = maxclause, rejectClause = None)
        if len(reader.clauses) == 0:
            exutil.ewrite("File %s contains more than %d clauses\n" % (iname, maxclause), 2)
            return False
    except Exception as ex:
        exutil.ewrite("Couldn't read CNF file: %s" % str(ex), 1)
        return
    xor = Xor(reader.clauses, iname, reader.nvar, csvFile)
    result = xor.generate(oname, multiFile)
    startTime = None
    return result


def replaceExtension(path, ext):
    fields = path.split('.')
    if len(fields) == 1:
        return path + '.' + ext
    else:
        fields[-1] = ext
    return ".".join(fields)

def run(name, args):
    iname = None
    oname = None
    path = None
    maxclause = None
    ok = True
    csvFile = None

    optlist, args = getopt.getopt(args, "hcl:v:i:o:p:m:")
    for (opt, val) in optlist:
        if opt == '-h':
            ok = False
        elif opt == '-v':
            exutil.verbLevel = int(val)
        elif opt == '-c':
            exutil.careful = True
        elif opt == '-l':
            try:
                csvFile = open(val, 'w')
            except:
                print("Couldn't open log file '%s'" % val)
                return;
        elif opt == '-i':
            iname = val
        elif opt == '-o':
            oname = val
            exutil.errfile = sys.stdout
        elif opt == '-p':
            path = val
            exutil.errfile = sys.stdout
        elif opt == '-m':
            maxclause = int(val)
    if not ok:
        usage(name)
        return

    if csvFile:
        fields = ["File", "Equations", "Clauses", "NX-Clauses", "Variables", "I-Vars", "Seconds"]
        csvWrite(csvFile, fields)

    if path is None:
        ecode = 0 if  extract(iname, oname, maxclause, False, csvFile) else 1
        sys.exit(ecode)
    else:
        if iname is not None or oname is not None:
            exutil.ewrite("Cannot specify path + input or output name", 0)
            usage(name)
            sys.exit(0)
        scount = 0
        flist = sorted(glob.glob(path + '*.cnf'))
        for iname in flist:
            oname = replaceExtension(iname, 'schedule')
            if extract(iname, oname, maxclause, True, csvFile):
                scount += 1
        exutil.ewrite("Extracted equations for %d/%d files\n" % (scount, len(flist)), 1)

if __name__ == "__main__":
    run(sys.argv[0], sys.argv[1:])
        
            
            

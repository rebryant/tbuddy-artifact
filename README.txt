This is an archive version of the TBUDDY trusted BDD package, along
with tbsat, a proof-generating SAT solver that is built using TBUDDY.
It also includes code for the lrat-check proof checker.

Makefile options:

install:
  Compile and install the executable programs and libraries in the bin and lib directories

run:
  (Must install first)

  Run a representative set of benchmarks.  Lots of stuff gets printed,
  but everything should be tabulated in a file 'results-measured.txt'
  This can be compared to the file 'results-reference.txt' showing the
  results for the reference machine, a 3.2-GHz Apple M1~Max processor
  with 64~GB of memory and running the OS~X operating system.

  The displayed fields are:
        Size: The scaling parameter for the benchmark
      In Var: The number of variables in the input CNF file
      In Cls: The number of clauses in the input CNF file
     SAT Sec: The runtime for tbsat
      Pf Cls: The number of clasues in the generated proof
     Chk Sec: The time required to check the proof using lrat-check

  The smallest instance of each benchmark is at or beyond the outer
  reaches of all proof-generating CDCL SAT solvers.  It can be seen
  that these quite trivial for tbsat, and that tbsat can scale to much
  larger instances for each benchmark.  The performance with Gaussian
  elimination is especially noteworthy.

clean:
  Remove all but the original files


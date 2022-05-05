This is an archive version of the TBUDDY trusted BDD package, along
with tbsat, a proof-generating SAT solver that is built using TBUDDY.
It also includes code for the lrat-check proof checker.

MAKEFILE OPTIONS:

install:
  Compile and install the executable programs and libraries in the bin and lib directories

run:
  (Must install first)

  Run a representative set of benchmarks.  Lots of stuff gets printed,
  but everything should be tabulated in a file 'results-measured.txt'

clean:
  Remove all but the original files

EXPERIMENTAL RESULTS

  The results you obtain can be compared to the results below.  These
  were obtained on the reference machine, a 3.2-GHz Apple M1~Max
  processor with 64~GB of memory running the OS~X operating system.

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

    Benchmark      Size    In Var     In Cls    SAT Sec     Pf Cls    Chk Sec  
-------------------------------------------------------------------------------
chess-scan             20       756       2,552       0.1     147,052       0.1
chess-scan             70     9,656      33,452       3.5   4,561,093       2.7
chess-scan            100    19,796      68,792       9.9  12,604,562       7.7
-------------------------------------------------------------------------------
pigeon-scan            15       465         676       0.1     113,464       0.1
pigeon-scan            50     5,050       7,501       3.6   4,307,998       2.7
pigeon-scan            75    11,325      16,876      13.2  15,461,862      10.2
-------------------------------------------------------------------------------
chew-bucket            50       144         384       0.0      32,005       0.0
chew-bucket           500     1,494       3,984       1.5   1,831,813       1.1
chew-bucket         1,000     2,994       7,984       5.8   7,098,462       4.4
-------------------------------------------------------------------------------
chew-gauss             50       144         384       0.0      14,273       0.0
chew-gauss            500     1,494       3,984       0.2     211,789       0.1
chew-gauss          1,000     2,994       7,984       0.4     465,719       0.3
chew-gauss          5,000    14,994      39,984       2.5   2,811,857       1.7
-------------------------------------------------------------------------------
urquhart-bucket         3       153         408       0.0      38,598       0.0
urquhart-bucket        10     1,980       5,280       2.1   2,524,726       1.6
urquhart-bucket        15     4,545      12,120      10.5  12,146,151       7.7
-------------------------------------------------------------------------------
urquhart-gauss          3       153         408       0.0      14,961       0.0
urquhart-gauss         10     1,980       5,280       0.2     259,463       0.1
urquhart-gauss         15     4,545      12,120       0.6     634,705       0.4
urquhart-gauss         20     8,160      21,760       1.1   1,208,351       0.7
-------------------------------------------------------------------------------

This directory contains some useful tools for working with tbsat.

Programs:

  xor_extractor.py:

    Detect the parity constraints within a CNF file.  Generate a
    schedule file for use by tbsat that enables it to use Gaussian
    elimination.

  randomizer.py:

    Given a CNF file, generate a random permutation of the input
    variables.  The resulting file can be provided to tbsat to make it
    use a random ordering of the BDD variables.

  grab_data.py:

    Extract data from generated output files and put into .csv format.
    See the examples in the files ../benchmarks/results/*/Makefile

Other files.

  xutil.py:
    Contains some useful routines for xor_extractor.py

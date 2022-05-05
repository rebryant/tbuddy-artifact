This directory contains the code for the TBUDDY library.

The initial code was imported from the BuDDy BDD package.

Some of these files were left the same; some were modified, and some
new files were added.

The Makefile compiles two archive files:

buddy.a:

   This should be fully compatible with the original BuDDy code.  Some
   aspects of the cache were modified, but not in ways that would
   affect the BuDDy API.

tbuddy.a:

   This incorporates new proof generation features.

The library files are installed in ../../lib

Installing these files also causes copies of the .h files exported by
the API to be moved into ../../include

CC=gcc
CXX=g++
TFLAGS =  -DENABLE_TBDD
DFLAGS =  -DCACHESTATS 
OPT = -O2
CFLAGS=-g $(OPT) -fPIC -Wno-nullability-completeness $(DFLAGS)
CXXFLAGS=-std=c++11
INC = -I..
LDIR = ../../lib
IDIR = ../../include

FILES = bddio.o bddop.o bvec.o cache.o fdd.o ilist.o imatrix.o kernel.o pairs.o \
	prime.o reorder.o tree.o cppext.o

TFILES = tbdd.to prover.to bddio.to bvec.to bddop.to cache.to fdd.to ilist.to \
	imatrix.to kernel.to pairs.to prime.to reorder.to tree.to cppext.to pseudoboolean.to

all: buddy.a tbuddy.a
	cp -p buddy.a $(LDIR)
	cp -p tbuddy.a $(LDIR)
	cp -p bdd.h $(IDIR)
	cp -p tbdd.h $(IDIR)
	cp -p ilist.h $(IDIR)
	cp -p prover.h $(IDIR)
	cp -p pseudoboolean.h $(IDIR)

buddy.a: $(FILES)
	ar cr buddy.a $(FILES)

tbuddy.a: $(TFILES)
	ar cr tbuddy.a $(TFILES)

.SUFFIXES: .c .cxx .o .to

.c.o:
	$(CC) $(CFLAGS) $(INC) -c $<

.cxx.o:
	$(CXX) $(CFLAGS) $(INC) -c $<

.c.to:
	$(CC) $(CFLAGS) $(TFLAGS) $(INC) -c $< -o $@

.cxx.to:
	$(CXX) $(CFLAGS) $(CXXFLAGS) $(TFLAGS) $(INC) -c $< -o $@

clean:
	rm -f *.a *.o *.to *~
	rm -rf *.dSYM




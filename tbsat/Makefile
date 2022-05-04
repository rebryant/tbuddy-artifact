CC=gcc
CXX=g++
OPT=-O2
#OPT=-O0
CFLAGS=-g $(OPT) -Wno-nullability-completeness -std=c++11
INC=-I../buddy/include
LDIR = ../buddy/lib
TLIB = $(LDIR)/tbuddy.a

all: tbsat sat_check

tbsat: clause.cpp clause.h teval.cpp bsat.cpp 
	$(CXX) $(CFLAGS) $(INC) -o tbsat clause.cpp teval.cpp bsat.cpp $(TLIB)

sat_check: clause.cpp clause.h sat_check.cpp
	$(CXX) $(CFLAGS) $(INC) -o sat_check clause.cpp sat_check.cpp $(TLIB)

.SUFFIXES: .c .cpp .o

.c.o:
	$(CC) $(CFLAGS) $(INC) -c $<

.cpp.o:
	$(CXX) $(CFLAGS) $(INC) -c $<

clean:
	rm -f *.o *~
	rm -f tbsat sat_check


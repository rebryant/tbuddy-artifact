INTERP=python3
SIZE = 03
VLEVEL=1
FDIR=../../files
SDIR=../../../bin
SOLVER=$(SDIR)/tbsat
CHECKER=$(SDIR)/lrat-check
TDIR=../../../tools
EXTRACT=$(TDIR)/xor_extractor.py
GRAB=$(TDIR)/grab_data.py
ROOT=urquhart-gauss

full: gen run check clear

gen:
	cp $(FDIR)/urquhart-li-$(SIZE).cnf $(ROOT)-$(SIZE).cnf 
	$(INTERP) $(EXTRACT) -i $(ROOT)-$(SIZE).cnf -o $(ROOT)-$(SIZE).schedule | tee $(ROOT)-$(SIZE).data
run:
	$(SOLVER) -v $(VLEVEL) -i $(ROOT)-$(SIZE).cnf -s $(ROOT)-$(SIZE).schedule -o $(ROOT)-$(SIZE).lrat | tee -a $(ROOT)-$(SIZE).data

check:
	$(CHECKER) $(ROOT)-$(SIZE).cnf $(ROOT)-$(SIZE).lrat | tee -a $(ROOT)-$(SIZE).data

clear:
	rm -f $(ROOT)-$(SIZE).{lrat,order,schedule}

data:
	$(INTERP) $(GRAB) "Read" *.data > $(ROOT)-input-clauses.csv
	$(INTERP) $(GRAB) 2 "Read" *.data > $(ROOT)-input-variables.csv
	$(INTERP) $(GRAB) "Elapsed" *.data > $(ROOT)-sat-seconds.csv
	$(INTERP) $(GRAB) "verification time" *.data > $(ROOT)-check-seconds.csv
	$(INTERP) $(GRAB) "Total clauses" *.data > $(ROOT)-proof-clauses.csv


clean:
	rm -f *.{data,lrat,order,schedule,cnf,csv}
	rm -f *~






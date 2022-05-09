install:
	rm -rf bin include lib
	mkdir bin include lib
	cd src ; make all

run:
	cd benchmarks ; make run

clean:
	cd src ; make clean
	rm -rf bin include lib
	cd benchmarks ; make clean
	cd tools ; make clean
	rm -f *~
	rm -f results-measured.txt

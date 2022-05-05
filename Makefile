all:
	rm -rf bin include lib
	mkdir bin include lib
	cd src ; make all

clean:
	cd src ; make clean
	rm -rf bin include lib
	rm -f *~

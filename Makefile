#_MIT License
#_
#_Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
#_
#_Permission is hereby granted, free of charge, to any person obtaining a copy
#_of this software and associated documentation files (the "Software"), to deal
#_in the Software without restriction, including without limitation the rights
#_to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#_copies of the Software, and to permit persons to whom the Software is
#_furnished to do so, subject to the following conditions:
#_
#_The above copyright notice and this permission notice shall be included in all
#_copies or substantial portions of the Software.
#_
#_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#_IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#_FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#_AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#_LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#_OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#_SOFTWARE.

# Makefile for logdissect
# https://github.com/dogoncouch/logdissect

ISPYTWO := $(sh -c "python2 --version" dot 2>/dev/null)
ISPYTHREE := $(sh -c "python3 --version" dot 2>/dev/null)

all: install clean

default: all

install:
ifndef ISPYTHREE:
	@echo Installing for Python 3
	python3 setup.py install
endif

ifndef ISPYTWO:
	@echo Installing for Python 2
	python2 setup.py install
endif

clean:
	rm -rf build dist logdissect.egg-info

test:
	@echo Running diff tests for time
	@echo
	sh -c 'time tests/tests.sh'
	@echo
	@echo - There should be no errors.
	@echo - Times should be below 0m0.400s on an i3 for Python 2.
	@echo - Times should be below 0m0.800s on an i3 for Python 3.
	@echo - Diff results should be empty.
	@echo

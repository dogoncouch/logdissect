#!/bin/bash

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

# NOTE: Run this file from the repository root (one dir up)

echo Running testall.log
./logdissect.py -s --outlog=tests/files/testall.log tests/files/exsyslog tests/files/exmeslog

echo Running with \* input option
./logdissect.py -s --outlog=tests/files/teststar.log tests/files/ex*

echo Diff for teststar::
diff tests/files/teststarexlog tests/files/teststar.log 

echo Running testrange.log
./logdissect.py -s --outlog=tests/files/testrange.log --range 20160202020202-20170227213200 tests/files/exsyslog tests/files/exmeslog

echo Diff for testrange:
diff tests/files/testrangeexlog tests/files/testrange.log

echo Running testnone.log
./logdissect.py -s --outlog=tests/files/testnone.log --range=20160202020202-20160227213200 tests/files/exsyslog tests/files/exmeslog

echo Diff for testnone:
diff tests/files/testnoneexlog tests/files/testnone.log

echo Running testgrep.log
./logdissect.py -s --outlog=tests/files/testgrep.log --grep=software tests/files/exsyslog tests/files/exmeslog

echo Diff for testgrep:
diff tests/files/testgrepexlog tests/files/testgrep.log

echo Running testjson.log:
./logdissect.py -s --outjson=tests/files/testjson.log tests/files/exmeslog tests/files/exsyslog

echo Running testinjson.log
./logdissect.py -s -p ldjson --outjson=tests/files/testinjson.log tests/files/testjson.log

echo Diff test for testinjson:
diff tests/files/testinjson.log tests/files/testjson.log

echo Running testsource.log:
./logdissect.py -s --outlog=tests/files/testsource.log --source=shade tests/files/exsyslog

echo Running diff test for testsource:
diff tests/files/testsource.log tests/files/exsyslog

echo Running testprocess.log:
./logdissect.py -s --outlog=tests/files/testprocess.log --process=systemd tests/files/exsyslog

echo Running diff test for testprocess:
diff tests/files/testprocess.log tests/files/testprocessexlog

echo Running testfname.log
./logdissect.py -s --outlog=tests/files/testfname.log --label=fname tests/files/exsyslog tests/files/exmeslog

echo Diff for testfname:
diff tests/files/testfnameexlog tests/files/testfname.log

echo Running testfpath.log
./logdissect.py -s --outlog=tests/files/testfpath.log --label=fpath tests/files/exsyslog tests/files/exmeslog

echo Diffs should be the same, and there should be no errors.

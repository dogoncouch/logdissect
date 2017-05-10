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
./logdissect.py -s --outlog=devtests/files/testall.log devtests/files/exsyslog devtests/files/exmeslog

echo Running with \* input option
./logdissect.py -s --outlog=devtests/files/teststar.log devtests/files/ex*

echo Diff for teststar::
diff devtests/files/teststarexlog devtests/files/teststar.log 

echo Running testrange.log
./logdissect.py -s --outlog=devtests/files/testrange.log --range 20160202020202-20170227213200 devtests/files/exsyslog devtests/files/exmeslog

echo Diff for testrange:
diff devtests/files/testrangeexlog devtests/files/testrange.log

echo Running testnone.log
./logdissect.py -s --outlog=devtests/files/testnone.log --range=20160202020202-20160227213200 devtests/files/exsyslog devtests/files/exmeslog

echo Diff for testnone:
diff devtests/files/testnoneexlog devtests/files/testnone.log

echo Running testgrep.log
./logdissect.py -s --outlog=devtests/files/testgrep.log --grep=software devtests/files/exsyslog devtests/files/exmeslog

echo Diff for testgrep:
diff devtests/files/testgrepexlog devtests/files/testgrep.log

echo Running testjson.log:
./logdissect.py -s --outjson=devtests/files/testjson.log devtests/files/exmeslog devtests/files/exsyslog

echo Running testinjson.log
./logdissect.py -s -p ldjson --outjson=devtests/files/testinjson.log devtests/files/testjson.log

echo Diff test for testinjson:
diff devtests/files/testinjson.log devtests/files/testjson.log

echo Running testsource.log:
./logdissect.py -s --outlog=devtests/files/testsource.log --source=shade devtests/files/exsyslog

echo Running diff test for testsource:
diff devtests/files/testsource.log devtests/files/exsyslog

echo Running testprocess.log:
./logdissect.py -s --outlog=devtests/files/testprocess.log --process=systemd devtests/files/exsyslog

echo Running diff test for testprocess:
diff devtests/files/testprocess.log devtests/files/testprocessexlog

echo Running testfname.log
./logdissect.py -s --outlog=devtests/files/testfname.log --label=fname devtests/files/exsyslog devtests/files/exmeslog

echo Diff for testfname:
diff devtests/files/testfnameexlog devtests/files/testfname.log

echo Running testfpath.log
./logdissect.py -s --outlog=devtests/files/testfpath.log --label=fpath devtests/files/exsyslog devtests/files/exmeslog

echo Diffs should be the same, and there should be no errors.

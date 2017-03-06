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

echo Running testall.log
./logdissect.py --outlog=devtest/testall.log --range=20160202020202-20170227213200 devtests/exsyslog,devtests/exmeslog

echo Diff for testall:
diff devtest/testall.log devtest/testallexlog

echo Running with \* input option
./logdissect.py --outlog=devtest/teststar.log --range=20160202020202-20170227213200 devtests/ex*

echo Diff for testall.log and teststar.log:
diff devtest/testall.log devtest/teststar.log

echo Running testnone.log
./logdissect.py --outlog=devtest/testnone.log --range=20160202020202-20160227213200 devtests/exsyslog,devtests/exmeslog

echo Diff for testnone:
diff devtest/testnone.log devtest/testnoneexlog

echo Running testfname.log
./logdissect.py --outlog=devtest/testfname.log --label=fname --range=20160202020202-20170227213200 devtests/exsyslog,devtests/exmeslog

echo Diff for testfname:
diff devtest/testfname.log devtest/testfnameexlog

echo Running testfpath.log
./logdissect.py --outlog=devtest/testfpath.log --label=fpath --range=20160202020202-20170227213200 devtests/exsyslog,devtests/exmeslog

echo Diffs should be the same, and there should be no errors.

# logdissect
logdissect is a tool for gaining insight into log files. It can merge more than one together and sort by timestamp, and filter the results by time range and other criteria. Files that end in .gz or .bz2 are ignored.

# INSTALLING
    git clone https://github.com/dogoncouch/logdissect.git
    cd logdissect
    sudo python setup.py install

# TRY WITHOUT INSTALLING
    git clone https://github.com/dogoncouch/logdissect.git
    cd logdissect
    ./logdissect.py [OPTIONS]

# OPTIONS

    --version          show program's version number and exit
    -h, --help         show this help message and exit
    --list-parsers     returns a list of available parsers
    --list-morphers    returns a list of available morphers
    --list-outputs     returns a list of available output formats
    -i INPUTS_LIST     specifies input files
    -p PARSER          specifies parser to use

  Morph options:
    --range=RANGE    Specifies the range <YYYYMMDDhhmm-YYYYMMDDhhmm>

  Output options:
    --outlog=OUTLOG  Sets the output file for standard log output
    --label=LABEL    Sets label type for entries in OUTLOG <fname|fpath>


# EXAMPLES
    
    logdissect -i messages --outlog=mywindow --range=20170301070000-20170301100000
    
    logdissect -i messages,debug,apache2/error.log --outlog=mylog.log --range=20160202020202-20170227213200 --label=fpath
    
    logdissect -i /var/log/apache2/acces.log,/var/log/apache2/other_vhosts_access.log --outlog=myaccess.log --range=20170207040000-20170207050000 --label=fname

# AUTHOR
    Dan Persons (dpersonsdev@gmail.com)

# COPYRIGHT
MIT License

Copyright (c) 2017 Dan Persons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# logdissect
logdissect is a tool for gaining insight into syslog files. It can merge multiple log files together and sort by timestamp, and filter the results by time range and other criteria. Files that end in .gz or .bz2 are ignored.

# INSTALLING
Requirements: git, python-setuptools  

    git clone https://github.com/dogoncouch/logdissect.git
    cd logdissect
    sudo python setup.py install

# TRY WITHOUT INSTALLING
    git clone https://github.com/dogoncouch/logdissect.git
    cd logdissect
    ./logdissect.py [OPTIONS] <files>

# OPTIONS

    Usage: logdissect [options] <files>

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    --list-parsers      returns a list of available parsers
    --list-morphers     returns a list of available morphers
    --list-outputs      returns a list of available output formats
    -p PARSER           specifies parser to use (default: syslog)

    Morph options:
    --grep=PATTERN      specifies a pattern to match
    --range=RANGE       specifies the range <YYYYMMDDhhmm-YYYYMMDDhhmm>

    Output options:
    --outlog=OUTLOG     sets the output file for standard log output
    --label=LABEL       sets label type for entries in OUTLOG <fname|fpath>


# EXAMPLES
    
    logdissect --outlog=mywindow --range=20170301070000-20170301070500 *
    
    logdissect --outlog=mylog.log --range=20160202020202-20170227213200 --label=fpath messages debug apache2/error.log
    
    logdissect --outlog=myaccess.log --grep=192.168 --label=fname /var/log/apache2/access.log /var/log/apache2/other_vhosts_access.log

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

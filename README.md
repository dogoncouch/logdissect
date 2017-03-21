# logdissect
logdissect is a tool for gaining insight into syslog files. It can merge multiple log files together and sort by timestamp, and filter the results by time range and other criteria. Files that end in .gz or .bz2 are ignored.

# INSTALLING
See the latest instructions on the [releases page](https://github.com/dogoncouch/logdissect/releases).

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

# Tips
1. metadata: logdissect uses file modification times to assign years to syslog date stamps. This allows it to parse logs that span more than one year without a problem. If you are copying log files, always use `` cp -r `` and `` scp -r `` to preserve original mtimes and other file metadata.

2. --range shortcuts: The range module will fill in your ranges with zeroes if they are shorter than 14 characters. If you want to get a range of 20170204120000 to 20170204120000, you can save time and use 2017020412 and 2017020413.

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

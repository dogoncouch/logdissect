# logdissect
logdissect is a tool for analyzing syslog files. It can merge entries from multiple log files and sort by timestamp, and filter the results by time range and other criteria. Results are output to the terminal by default, and can also be output to a standard syslog file, or to a JSON array along with some metadata..

# Installing
See the latest instructions on the [releases page](https://github.com/dogoncouch/logdissect/releases).

# Options

  usage: logdissect [-h] [--grep PATTERN] [--host HOST] [--last LAST] [--process PROCESS] [--range RANGE] [--rgrep RPATTERN] [--outlog OUTLOG] [--label LABEL] [--outjson OUTJSON] [--version] [--list-parsers] [--list-morphers] [--list-outputs] [-p PARSER] [-s] [--verbose] [file [file ...]]
  
  positional arguments:
    file               Specifies input files
  
  optional arguments:
    -h, --help         show this help message and exit
    --version          show program's version number and exit
    --list-parsers     returns a list of available parsers
    --list-morphers    returns a list of available morphers
    --list-outputs     returns a list of available output formats
    -p PARSER          specifies parser to use (default: syslog)
    -s                 silences terminal output
    --verbose          sets verbose terminal output
  
  Morph options:
    --grep PATTERN     specifies a pattern to match
    --host HOST        specifies a source host to match
    --last LAST        specifies preceeding time period (5m/3h/2d/etc)
    --process PROCESS  specifies a source process to match
    --range RANGE      specifies a range <YYYYMMDDhhmm-YYYYMMDDhhmm>
    --rgrep RPATTERN   specifies a pattern to filter out
  
  Output options:
    --outlog OUTLOG    sets the output file for standard log output
    --label LABEL      sets label type for entries in OUTLOG <fname|fpath>
    --outjson OUTJSON  sets the output file for JSON output

# Examples
    
    logdissect --last=10m auth.log
    
    logdissect --last=2m *
    
    logdissect -v --range=20160202020202-20170227213200 --label=fpath messages debug apache2/error.log
    
    logdissect -s --outlog=myaccess.log --grep=192.168.1.56 --last=30d --label=fname /var/log/apache2/access.log /var/log/apache2/other_vhosts_access.log

# Notes
1. metadata: logdissect uses file modification times to assign years to syslog date stamps. This allows it to parse logs that span more than one year without a problem. If you are copying log files, always use `` cp -p `` (or `` cp --preserve=timestamps `` ) and `` scp -p `` to preserve original mtimes and other file metadata.

2. Re-parsing: If you are planning on parsing an output file back into logdissect at some point, using JSON is highly recommended. The JSON output module uses date stamps that include a year. Re-parsing a standard log output file will cause problems if the file has a different mtime than the original logs.

3. --range shortcuts: The range module will fill in your ranges with zeroes if they are shorter than 14 characters. If you want to get a range of 20170204120000 to 20170204130000, you can save time and use 2017020412 and 2017020413.

4. --last options: The last option should be a number followed by either 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. --last=20m).

5. Zipped files: Files that end in .gz, .bz2, or .zip are ignored.

# Author
    Dan Persons (dpersonsdev@gmail.com)

# Copyright
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

# logdissect
For API documentation, see [README-API.md](README-API.md)

## Index

- [Introduction](#introduction)
  - [Description](#description)
  - [Installing](#installing)
- [Usage](#usage)
  - [Options](#options)
  - [Examples](#examples)
  - [Notes](#notes)
- [Community](#community)
  - [API](#api)
  - [Support](#support)
  - [Contributing](#contributing)
- [Copyright](#copyright)


# Introduction


## Description
logdissect is a command line utility and library module for analyzing syslog files. It can merge entries from multiple log files and sort by timestamp, and filter the results by time range and other criteria. Results are output to the terminal by default, and can also be output to a standard syslog file, or to a JSON array along with some metadata..

## Installing
To install the latest release, see the latest instructions on the [releases page](https://github.com/dogoncouch/logdissect/releases). To install the development source, see the instructions in [README-DEV.md](README-DEV.md).

# Usage

## Options

    usage: logdissect [-h] [--dest DEST] [--grep PATTERN] [--last LAST]
                      [--process PROCESS] [--protocol PROTOCOL] [--range RANGE]
                      [--rdest RDEST] [--rgrep RPATTERN] [--rprocess RPROCESS]
                      [--rsource RSOURCE] [--source SOURCE] [--outlog OUTLOG]
                      [--label LABEL] [--outjson OUTJSON] [--version] [--verbose]
                      [-s] [--list-parsers] [-p PARSER] [-z] [-t TZONE]
                      [file [file ...]]
    
    positional arguments:
      file                 specify input files
    
    optional arguments:
      -h, --help           show this help message and exit
      --version            show program's version number and exit
      --verbose            set verbose terminal output
      -s                   silence terminal output
      --list-parsers       return a list of available parsers
      -p PARSER            select a parser (default: syslogbsd)
      -z, --unzip          include files compressed with gzip
      -t TZONE             specify timezone offset to GMT (e.g. '+0500')
    
    morph options:
      --dest DEST          match a destination host
      --grep PATTERN       match a pattern
      --last LAST          match a preceeding time period (e.g. 5m/3h/2d/etc)
      --process PROCESS    match a source process
      --protocol PROTOCOL  match a protocol
      --range RANGE        match a time range (YYYYMMDDhhmm-YYYYMMDDhhmm)
      --rdest RDEST        filter out a destination host
      --rgrep RPATTERN     filter out a pattern
      --rprocess RPROCESS  filter out a source process
      --rsource RSOURCE    filter out a source host
      --source SOURCE      match a source host
    
    output options:
      --outlog OUTLOG      set the output file for standard log output
      --label LABEL        set label type for OUTLOG (fname|fpath)
      --outjson OUTJSON    set the output file for JSON output

## Examples
    
    logdissect --last=10m auth.log
    logdissect --last=2m *
    logdissect -v --range=20160202020202-20170227213200 --label=fpath messages debug apache2/error.log
    logdissect -s --outlog=myaccess.log --grep=192.168.1.56 --last=30d --label=fname /var/log/apache2/access.log /var/log/apache2/other_vhosts_access.log

## Notes
1. metadata: logdissect uses file modification times to assign years to syslog date stamps. This allows it to parse logs that span more than one year without a problem. If you are copying log files, always use `` cp -p `` (or `` cp --preserve=timestamps `` ) and `` scp -p `` to preserve original mtimes and other file metadata.

2. Re-parsing: If you are planning on parsing an output file back into logdissect at some point, using JSON is highly recommended. The JSON output module uses date stamps that include a year. Re-parsing a standard log output file will cause problems if the file has a different mtime than the original logs.

3. --range shortcuts: The range module will fill in your ranges with zeroes if they are shorter than 14 characters. If you want to get a range of 20170204120000 to 20170204130000, you can save time and use 2017020412 and 2017020413.

4. --last options: The last option should be a number followed by either 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. --last=20m).

# Community

## API
logdissect 2.0 provides a stable API for parsing log files, and storing data. For more information on API usage, see  [README-API.md](README-API.md).

## Support
Bugs, questions, and other issues can be directed to the project's [issues page](https://github.com/dogoncouch/logdissect/issues) on GitHub, or emailed to [dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com).

## Contributing
Contributions are welcome in the form of code, bug fixes, or testing feedback. For more on how to contribute to logdissect, see [README-DEV.md](README-DEV.md).


# Copyright
MIT License

Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)

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

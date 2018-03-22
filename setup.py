# MIT License
# 
# Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Logdissect
----------

Logdissect is a CLI utility and Python library for analyzing log files and other data. It can parse, merge, filter, and export data (to log files, or JSON).

Options
```````

::

    usage: logdissect.py [-h] [--dhost DHOST] [--grep PATTERN] [--last LAST]
                         [--process PROCESS] [--protocol PROTOCOL] [--range RANGE]
                         [--utc] [--rdhost DHOST] [--rgrep PATTERN]
                         [--rprocess PROCESS] [--rprotocol PROTOCOL]
                         [--rshost SHOST] [--rsource SOURCE] [--shost SHOST]
                         [--source SOURCE] [--linejson LINEJSON] [--outlog OUTLOG]
                         [--label LABEL] [--sojson SOJSON] [--pretty] [--version]
                         [--verbose] [-s] [--list-parsers] [-p PARSER] [-z]
                         [-t TZONE]
                         [file [file ...]]
    
    positional arguments:
      file                  specify input files
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --verbose             set verbose terminal output
      -s                    silence terminal output
      --list-parsers        return a list of available parsers
      -p PARSER             select a parser (default: syslog)
      -z, --unzip           include files compressed with gzip
      -t TZONE              specify timezone offset to UTC (e.g. '+0500')
    
    filter options:
      --dhost DHOST         match a destination host
      --grep PATTERN        match a pattern
      --last LAST           match a preceeding time period (e.g. 5m/3h/2d/etc)
      --process PROCESS     match a source process
      --protocol PROTOCOL   match a protocol
      --range RANGE         match a time range (YYYYMMDDhhmm-YYYYMMDDhhmm)
      --utc                 use UTC for range matching
      --rdhost DHOST        filter out a destination host
      --rgrep PATTERN       filter out a pattern
      --rprocess PROCESS    filter out a source process
      --rprotocol PROTOCOL  filter out a protocol
      --rshost SHOST        filter out a source host
      --rsource SOURCE      filter out a log source
      --shost SHOST         match a source host
      --source SOURCE       match a log source
    
    output options:
      --linejson LINEJSON   set the output file for line by line JSON output
      --outlog OUTLOG       set the output file for standard log output
      --label LABEL         set label type for OUTLOG (fname|fpath)
      --sojson SOJSON       set the output file for single object JSON output
      --pretty              use pretty formatting for sojson output


    ==== Available parsing modules: ====
    
    ciscoios        : cisco ios parsing module
    linejson        : logdissect object-per-line JSON parsing module
    sojson          : logdissect single object JSON parsing module
    syslog          : syslog (standard timestamp) parsing module
    syslogiso       : syslog (ISO timestamp) parsing module
    syslognohost    : syslog (standard timestamp, no host) parsing module
    tcpdump         : tcpdump terminal output parsing module
    webaccess       : web access log parsing module
    windowsrsyslog  : windows rsyslog agent log parsing module

Links
`````

* `Releases <https://github.com/dogoncouch/logdissect/releases/>`_
* `Usage <https://github.com/dogoncouch/logdissect/blob/master/README.md>`_
* `API Usage <https://github.com/dogoncouch/logdissect/blob/master/docs/README-API.md>`_
* `How To Contribute <https://github.com/dogoncouch/logdissect/blob/master/docs/CONTRIBUTING.md>`_
* `Changelog <https://github.com/dogoncouch/logdissect/blob/master/CHANGELOG.md>`_
* `GitHub <https://github.com/dogoncouch/logdissect/>`_
* `Development source <https://github.com/dogoncouch/logdissect/tree/dev>`_

"""

from setuptools import setup
from os.path import join
from sys import prefix
from logdissect import __version__

ourdata = [(join(prefix, 'share/man/man1'), ['docs/logdissect.1']),
        (join(prefix, 'share/man/man3'), ['docs/logdissect.3']),
        (join(prefix, 'share/doc/logdissect'), ['README.md', 'docs/README-API.md',
            'docs/CONTRIBUTING.md', 'LICENSE', 'CHANGELOG.md'])]

setup(name = 'logdissect', version = str(__version__),
        description = 'Robust CLI syslog forensics tool',
        long_description = __doc__,
        author = 'Dan Persons', author_email = 'dpersonsdev@gmail.com',
        url = 'https://github.com/dogoncouch/logdissect',
        download_url = 'https://github.com/dogoncouch/logdissect/archive/v' + str(__version__) + '.tar.gz',
        keywords = ['log', 'syslog', 'analysis', 'forensics', 'security',
            'cli', 'secops', 'data-science', 'forensic-analysis',
            'log-analysis', 'log-analyzer', 'log-viewer', 'log-parser',
            'log-viewer', 'log-parsing', 'python-library',
            'python-module', 'parser', 'data-analysis', 'library', 'module'],
        packages = ['logdissect', 'logdissect.parsers',
            'logdissect.filters', 'logdissect.output'],
        entry_points = \
                { 'console_scripts': [ 'logdissect = logdissect.core:main' ]},
        data_files = ourdata,
        classifiers = ["Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python",
            "Topic :: System :: Systems Administration",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Security"])

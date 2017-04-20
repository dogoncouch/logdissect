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
"""
Logdissect
----------

Logdissect is a tool for analyzing syslog files. It can merge entries from multiple log files and sort by timestamp, and filter the results by time range and other criteria. Results are output to the terminal by default, and can also be output to a standard syslog file, or to a JSON array along with some metadata.

Options
```````

::

    Usage: logdissect [options] <files>
    
    --version          show program's version number and exit
    -h, --help         show this help message and exit
    --list-parsers     returns a list of available parsers
    --list-morphers    returns a list of available morphers
    --list-outputs     returns a list of available output formats
    -p PARSER          specifies parser to use (default: syslog)
    -s                 silences terminal output
    -v                 sets verbose terminal output
    
    Morph options:
    --grep=PATTERN     specifies a pattern to match
    --host=HOST        specifies a source host to match
    --last=LAST        specifies preceeding time period (5m/3h/2d/etc)
    --process=PROCESS  specifies a source process to match
    --range=RANGE      specifies the range <YYYYMMDDhhmm-YYYYMMDDhhmm>
    --rgrep=RPATTERN   specifies a pattern to filter out
    
    Output options:
    --outlog=OUTLOG    sets the output file for standard log output
    --label=LABEL      sets label type for entries in OUTLOG <fname|fpath>
    --outjson=OUTJSON  sets the output file for JSON output

Links
`````

* `Releases <https://github.com/dogoncouch/logdissect/releases/>`_
* `README <https://github.com/dogoncouch/logdissect/blob/master/README.md>`_
* `Development source <https://github.com/dogoncouch/logdissect/>`_

"""

from setuptools import setup
from os.path import join
from sys import prefix
from logdissect import __version__

ourdata = [(join(prefix, 'share/man/man1'), ['doc/logdissect.1']),
        (join(prefix, 'share/doc/logdissect'), ['README.md', 'LICENSE', 
            'CHANGELOG.md'])]

setup(name = 'logdissect', version = str(__version__),
        description = 'Robust CLI syslog forensics tool',
        long_description = __doc__,
        author = 'Dan Persons', author_email = 'dpersonsdev@gmail.com',
        url = 'https://github.com/dogoncouch/logdissect',
        download_url = 'https://github.com/dogoncouch/logdissect/archive/v' + str(__version__) + '.tar.gz',
        keywords = ['log', 'syslog', 'analysis', 'forensics', 'security',
            'cli', 'secops', 'sysadmin', 'forensic-analysis',
            'log-analysis', 'log-analyzer', 'log-viewer'],
        packages = ['logdissect', 'logdissect.data', 'logdissect.parsers',
            'logdissect.morphers', 'logdissect.output'],
        entry_points = \
                { 'console_scripts': [ 'logdissect = logdissect.core:main' ]},
        data_files = ourdata,
        classifiers = ["Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 2",
            "Topic :: System :: Systems Administration"])

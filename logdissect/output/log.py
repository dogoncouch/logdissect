# MIT License
# 
# Copyright (c) 2017 Dan Persons <dpersonsdev@gmail.com>
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

from logdissect.output.type import OutputModule as OurModule
from logdissect.data import LogData

class OutputModule(OurModule):
    def __init__(self, args=[]):
        """Initialize the log file output module"""
        self.name = 'log'
        self.desc = 'output to standard log file format'
        self.output_path = ''

        args.add_argument('--outlog', action='store', dest='outlog',
                help='set the output file for standard log output')
        args.add_argument('--label', action='store', dest='label',
                help='set label type for OUTLOG (fname|fpath)')

    def write_output(self, data, args=[]):
        """Write log data to a log file"""
        if not args.outlog:
            return 0
        lastpath = ''
        with open(str(args.outlog), 'w') as output_file:
            for entry in data.entries:
                if args.label:
                    if entry.source_path == lastpath:
                        output_file.write(entry.raw_text + '\n')
                    elif args.label == 'fname':
                        output_file.write('======== ' + \
                                entry.source_path.split('/')[-1] + \
                                ' >>>>\n' + entry.raw_text + '\n')
                    elif args.label == 'fpath':
                        output_file.write('======== ' + \
                                entry.source_path  + \
                                ' >>>>\n' + entry.raw_text + '\n')
                else: output_file.write(entry.raw_text + '\n')
                lastpath = entry.source_path

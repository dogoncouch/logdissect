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

import json
from logdissect.output.type import OutputModule as OurModule

class OutputModule(OurModule):
    def __init__(self, args=[]):
        """Initialize the line by line JSON output module"""
        self.name = 'linejson'
        self.desc = 'output JSON objects (one per line)'

        args.add_argument('--linejson', action='store', dest='linejson',
                help='set the output file for line by line JSON output')

    def write_output(self, data, args=[]):
        """Write log data to a file with one JSON object per line"""
        if not args.linejson:
            return 0
        else:
            entrylist = []
            for entry in data['entries']:
                entrystring = json.dumps(entry, sort_keys=True)
                entrylist.append(entrystring)
        
            with open(str(args.linejson), 'w') as output_file:
                output_file.write('\n'.join(entrylist))

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
        """Initialize the JSON output module"""
        self.name = 'outjson'
        self.desc = 'output to JSON arrays'

        args.add_argument('--outjson', action='store', dest='outjson',
                help='set the output file for JSON output')

    def write_output(self, data, args=[]):
        """Write log data to a JSON array"""
        if not args.outjson:
            return 0
        else:
            logstring = json.dumps(data['entries'], indent=2, sort_keys=True,
                    separators=(',', ': '))
        
            with open(str(args.outjson), 'w') as output_file:
                output_file.write(logstring)

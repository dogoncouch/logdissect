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
from logdissect.data.data import LogData

class OutputModule(OurModule):
    def __init__(self, options=[]):
        """Initialize the JSON output module"""
        self.name = 'outjson'
        self.desc = 'output to JSON arrays'

        options.add_argument('--outjson', action='append', dest='outjson',
                help='set the output file for JSON output')

    def write_output(self, data, options=[]):
        """Write log data to a JSON array"""
        if not options.outjson:
            return 0
        
        entrylist = []
        for entry in data.entries:
            thisentry = {'raw_text': entry.raw_text,
                    'date_stamp': entry.date_stamp,
                    'tzone': entry.tzone,
                    'raw_stamp': entry.raw_stamp,
                    'message': entry.message,
                    'source_path': entry.source_path,
                    'source_host': entry.source_host,
                    'dest_host': entry.dest_host,
                    'protocol': entry.protocol,
                    'source_process': entry.source_process,
                    'source_pid': entry.source_pid}
            
            entrylist.append(thisentry)

        logstring = json.dumps(entrylist, indent=2, sort_keys=True,
                separators=(',', ': '))

        with open(str(options.outjson[0]), 'w') as output_file:
            output_file.write(logstring)

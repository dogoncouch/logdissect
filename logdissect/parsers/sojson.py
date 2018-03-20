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
from logdissect.parsers.type import ParseModule as OurModule


class ParseModule(OurModule):
    def __init__(self):
        """Initialize the single object JSON parsing module"""
        self.name = 'sojson'
        self.desc = 'logdissect single object JSON parsing module'
        self.tzone = None



    def parse_file(self, sourcepath):
        """Parse single JSON object into a LogData object"""

        # Open input file and read JSON array:
        with open(sourcepath, 'r') as logfile:
            jsonstr = logfile.read()

        # Set our attributes for this entry and add it to data.entries:
        data = {}
        data['entries'] = json.loads(jsonstr)
        if self.tzone:
            for e in data['entries']:
                e['tzone'] = self.tzone

        # Return the parsed data
        return data

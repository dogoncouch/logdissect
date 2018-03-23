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
        """Initialize the object-per-line JSON parsing module"""
        self.name = 'linejson'
        self.desc = 'logdissect object-per-line JSON parsing module'
        self.data_format = ''
        self.fields = []
        self.backup_date_format =  None
        self.backup_fields = []
        self.tzone = None
        self.datestamp_type = None



    def parse_file(self, sourcepath):
        """Parse an object-per-line JSON file into a log data dict"""

        # Open input file and read JSON array:
        with open(sourcepath, 'r') as logfile:
            jsonlist = logfile.readlines()

        # Set our attributes for this entry and add it to data.entries:
        data = {}
        data['entries'] = jsonlist
        for line in jsonlist:
            entry = self.parse_line(line)
            data['entries'].append(entry)
        if self.tzone:
            for e in data['entries']:
                e['tzone'] = self.tzone

        # Return the parsed data
        return data

    def parse_line(self, line):
        """Convert a line of json into a Python object"""
        return json.loads(line)

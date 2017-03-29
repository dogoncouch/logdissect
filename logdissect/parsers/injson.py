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
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData



class ParseModule(OurModule):
    def __init__(self, options):
        """Initialize the JSON parsing module"""
        self.name = 'injson'
        self.desc = 'JSON parsing module'



    def parse_log(self, data):
        """Parse a JSON array into a LogData object"""

        newdata = data
        newdata.entries = []

        # Open input file and read JSON array:
        with open(data.source_full_path, 'r') as logfile:
            jsonstr = logfile.read()
        
        # Set our attributes for this entry and add it to newdata.entries:
        entrylist = json.loads(jsonstr)
        for entry in entrylist:
            thisentry = LogEntry()
            thisentry.date_stamp_year = entry[0]
            thisentry.source_full_path = entry[1]
            thisentry.source_host = entry[2]
            thisentry.source_process = entry[3]
            thisentry.raw_text = entry[4]
            newdata.entries.append(thisentry)

        # Return the parsed data
        return newdata

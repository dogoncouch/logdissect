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
from logdissect.data import LogEntry
from logdissect.data import LogData



class ParseModule(OurModule):
    def __init__(self):
        """Initialize the JSON parsing module"""
        self.name = 'ldjson'
        self.desc = 'logdissect JSON parsing module'
        self.tzone = None



    def parse_file(self, sourcepath):
        """Parse a JSON array into a LogData object"""

        data = LogData()
        data.source_path = sourcepath

        # Open input file and read JSON array:
        with open(data.source_path, 'r') as logfile:
            jsonstr = logfile.read()
        
        # Set our attributes for this entry and add it to data.entries:
        entrylist = json.loads(jsonstr)
        for entry in entrylist:
            thisentry = LogEntry()
            thisentry.parser = entry['parser']
            thisentry.source_path = entry['source_path']
            thisentry.raw_text = entry['raw_text']
            thisentry.date_stamp = entry['date_stamp']
            thisentry.date_stamp_utc = entry['date_stamp_utc']
            if self.tzone:
                thisentry.tzone = self.tzone
            else:
                thisentry.tzone = entry['tzone']
            thisentry.raw_stamp = entry['raw_stamp']
            thisentry.facility = entry['facility']
            thisentry.severity = entry['severity']
            thisentry.message = entry['message']
            thisentry.source_host = entry['source_host']
            thisentry.dest_host = entry['dest_host']
            thisentry.protocol = entry['protocol']
            thisentry.source_process = entry['source_process']
            thisentry.source_pid = entry['source_pid']
            data.entries.append(thisentry)

        # Return the parsed data
        return data

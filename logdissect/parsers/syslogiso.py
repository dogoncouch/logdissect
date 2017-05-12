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

import os
import re
from datetime import datetime
import time
import gzip
from logdissect.parsers.type import ParseModule as OurModule
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData

class ParseModule(OurModule):
    def __init__(self):
        """Initialize the syslog ISODATE parsing module"""
        self.name = 'syslogiso'
        self.desc = 'syslog ISODATE parsing module'
        self.date_format = \
                re.compile(r"^(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.?\d+?[+-]\d\d:?\d\d\s+\S+\s+\S+\[?\d*?\]?):")
        self.tzone = None



    def parse_file(self, sourcepath):
        """Parse a syslog file into a LogData object"""
        data = LogData()
        data.parser = 'syslogiso'
	current_entry = LogEntry()
        data.source_path = sourcepath
        data.source_file = data.source_path.split('/')[-1]

        # Set our start year:
        data.source_file_mtime = \
                os.path.getmtime(data.source_path)
        timestamp = \
                datetime.fromtimestamp(data.source_file_mtime)
        data.source_file_year = timestamp.year
        
                        
        # Get our lines:
        # To Do: Add check for zipped files right here:
        fparts = sourcepath.split('.')
        if fparts[-1] == 'gz':
            with gzip.open(str(sourcepath), 'r') as logfile:
                loglines = reversed(logfile.readlines())
        else:
            with open(str(data.source_path), 'r') as logfile:
                loglines = reversed(logfile.readlines())
        with open(str(data.source_path), 'r') as logfile:
            loglines = reversed(logfile.readlines())

        # Parse our lines:
        for line in loglines:
            ourline = line.rstrip()
            
            # Send the line to self.parse_line
            datestampnoyear, tzone, rawstamp, sourcehost, sourceprocess, \
                    sourcepid, message = self.parse_line(ourline)
           

            # Set our attributes:
            current_entry.parser = 'syslogiso'
            current_entry.raw_text = ourline
            current_entry.date_stamp_noyear = datestamp[4:]
            current_entry.date_stamp = datestamp
            if self.tzone:
                current_entry.tzone = self.tzone
            else:
                current_entry.tzone = tzone
            current_entry.date_stamp_utc = current_entry._utc_date()
            current_entry.raw_stamp = rawstamp
            current_entry.message = message
            current_entry.source_host = sourcehost
            current_entry.source_process = sourceprocess
            current_entry.source_pid = sourcepid
            current_entry.source_path = \
                    data.source_path

            # Append and reset current_entry
            data.entries.append(current_entry)
            current_entry = LogEntry()
        
        # Write the entries to the log object
        data.entries.reverse()
        return data


    def parse_line(self, line):
        """Returns date stamp (YYYYmmddHHMMSS[.f]), timezone, rawstamp, sourcehost, sourceprocess, sourcepid, message"""
        match = re.findall(self.date_format, line)
        if match:
            attr_list = str(match[0]).split(' ')
            try:
                attr_list.remove('')
            except ValueError:
                pass


            # Set our attributes:
            datestamp = attr_list[0][:-6].strip('-').strip('T').strip(':')
            if attr_list[0][-1] == 'Z':
                tzone = '+0000'
                datestamp = \
                        attr_list[0][:-1].strip('-').strip('T').strip(':')
            else:
                tzone = attr_list[0][-5:].strip(':')
                datestamp = \
                        attr_list[0][:-6].strip('-').strip('T').strip(':')
            sourcehost = attr_list[1]
            sourceproclist = attr_list[2].split('[')
            sourceprocess = sourceproclist[0]
            if len(sourceproclist) > 1:
                sourcepid = sourceproclist[1].strip(']')
            else: sourcepid = None
            rawstamp = line[:len(match[0])]
            message = line[len(match[0]) + 2:]

            
            return datestamp, tzone, rawstamp, sourcehost, \
                    sourceprocess, sourcepid, message


        else: return None

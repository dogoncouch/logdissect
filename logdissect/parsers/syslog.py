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
import datetime
from logdissect.parsers.type import ParseModule as OurModule
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData

class ParseModule(OurModule):
    def __init__(self, options):
        """Initialize the standard syslog parsing module"""
        self.name = 'syslog'
        self.desc = 'Syslog parsing module'
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+\[?\d*?\]?):")



    def parse_log(self, data):
        """Parse a syslog file into a LogData object"""
        newdata = data
        newdata.entries = []
	current_entry = LogEntry()
        data.source_file = data.source_path.split('/')[-1]

        # Set our start year:
        data.source_file_mtime = \
                os.path.getmtime(data.source_path)
        timestamp = \
                datetime.datetime.fromtimestamp(data.source_file_mtime)
        data.source_file_year = timestamp.year
        entry_year = timestamp.year
        recent_date_stamp = '99999999999999'

        # Get our lines and reverse them (parser works in reverse -
        #       helps find year and parse multi-line entries):
        # if data.source_path == '-':
            # If no file specified, use lines read from stdin
            # loglines = reversed(self.lines)
        # else:
            # Otherwise read lines from the file
        with open(str(data.source_path), 'r') as logfile:
            loglines = reversed(logfile.readlines())
        # Parse works in reverse. This helps with multi-line entries,
        # and logs that span multiple years (December to January shift).

        # Parse our lines:
        for line in loglines:
            ourline = line.rstrip()
            if len(current_entry.raw_text) >0:
                current_entry.raw_text = ourline + '\n' + \
                        current_entry.raw_text
            else: current_entry.raw_text = ourline
            match = re.findall(self.date_format, ourline)
            if match:
                attr_list = str(match[0]).split(' ')
                try:
                    attr_list.remove('')
                except ValueError:
                    pass

                # Get the date stamp (without year)
                months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
                        'Apr':'04', 'May':'05', 'Jun':'06', \
                        'Jul':'07', 'Aug':'08', 'Sep':'09', \
                        'Oct':'10', 'Nov':'11', 'Dec':'12'}
                int_month = months[attr_list[0].strip()]
                daydate = str(attr_list[1].strip()).zfill(2)
                timelist = str(str(attr_list[2]).replace(':',''))
                date_stamp_noyear = str(int_month) + str(daydate) + str(timelist)
                
                # Check for Dec-Jan jump and set the year:
                if int(date_stamp_noyear) > int(recent_date_stamp):
                    entry_year = entry_year - 1
                recent_date_stamp = date_stamp_noyear
                
                # Split source process/PID
                sourceproclist = attr_list[4].split('[')
                
                # Set our attributes:
                current_entry.source_host = attr_list[3]
                current_entry.source_process = sourceproclist[0]
                if len(sourceproclist) > 1:
                    current_entry.source_pid = sourceproclist[1].strip(']')
                current_entry.date_stamp_noyear = date_stamp_noyear
                current_entry.date_stamp = str(entry_year) \
                        + str(current_entry.date_stamp_noyear)
                current_entry.source_path = \
                        data.source_path

                # Append and reset current_entry
                newdata.entries.append(current_entry)
                current_entry = LogEntry()
        
        # Write the entries to the log object
        newdata.entries.reverse()
        return newdata

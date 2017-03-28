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
        # self.data = LogData()
        # self.newdata = LogData()
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} \S+ \S+\[?\d*?\]?):")

    def parse_log(self, data):
        newdata = data
        newdata.entries = []
	current_entry = LogEntry()
        data.source_file_mtime = \
                os.path.getmtime(data.source_full_path)
        timestamp = \
                datetime.datetime.fromtimestamp(data.source_file_mtime)
        data.source_file_year = timestamp.year
        entry_year = timestamp.year
        recent_date_stamp = '99999999999999'
        # To Do: add some detection to fill in LogData class vars
        data.source_file = data.source_full_path.split('/')[-1]
        # Get our lines:
        with open(str(data.source_full_path), 'r') as logfile:
            loglines = reversed(logfile.readlines())
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
                months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
                        'Apr':'04', 'May':'05', 'Jun':'06', \
                        'Jul':'07', 'Aug':'08', 'Sep':'09', \
                        'Oce':'10', 'Nov':'11', 'Dec':'12'}
                int_month = months[attr_list[0]]
                daydate = str(attr_list[1]).strip().zfill(2)
                timelist = str(str(attr_list[2]).replace(':',''))
                date_stamp = str(int_month) + str(daydate) + str(timelist)
                # Check for Dec-Jan
                if int(date_stamp) > int(recent_date_stamp):
                    entry_year = entry_year - 1
                recent_date_stamp = date_stamp
                current_entry.source_host = attr_list[3]
                current_entry.source_process = attr_list[4]
                current_entry.date_stamp = date_stamp
                current_entry.date_stamp_year = str(entry_year) \
                        + str(current_entry.date_stamp)
                current_entry.source_full_path = \
                        data.source_full_path
                newdata.entries.append(current_entry)
                current_entry = LogEntry()
        
        # Write the entries to the log object
        newdata.entries.reverse()
        return newdata

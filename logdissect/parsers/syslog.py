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
from logdissect.parsers.type import ParseModule as OurModule
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData

class ParseModule(OurModule):
    def __init__(self, options):
        """Initialize the standard syslog parsing module"""
        self.name = 'syslog'
        self.desc = 'syslog parsing module'
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+\[?\d*?\]?):")
        # Account for syslog configurations that don't include source host
        # options.add_argument('--no-host', action='store_true', 
        #         dest='nohost',
        #         help='parse syslog entries with no source host')
        # self.nohost_format = \
        #         re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\[?\d*\]?):")
                # re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\[?\d*?\]?):")



    def parse_log(self, data, options):
        """Parse a syslog file into a LogData object"""
        newdata = data
        newdata.parser = 'syslog'
        newdata.entries = []
	current_entry = LogEntry()
        data.source_file = data.source_path.split('/')[-1]

        # Set our start year:
        data.source_file_mtime = \
                os.path.getmtime(data.source_path)
        timestamp = \
                datetime.fromtimestamp(data.source_file_mtime)
        data.source_file_year = timestamp.year
        entryyear = timestamp.year
        recentdatestamp = '99999999999999'
        
        # Set our timezone
        if time.daylight:
            tzone = str(int(float(time.altzone) / 60 // 60)).rjust(2, '0') + \
                    str(int(float(time.altzone) / 60 % 60)).ljust(2, '0')
        else:
            tzone = str(int(float(time.altzone) / 60 // 60)).rjust(2, '0') + \
                    str(int(float(time.altzone) / 60 % 60)).ljust(2, '0')

                        
        # Parsing works in reverse. This helps with multi-line entries,
        # and logs that span multiple years (December to January shift).
        
        # Get our lines:
        with open(str(data.source_path), 'r') as logfile:
            loglines = reversed(logfile.readlines())

        # Parse our lines:
        for line in loglines:
            ourline = line.rstrip()
            # if len(current_entry.raw_text) >0:
            if current_entry.raw_text:
                ourline = ourline + '\n' + \
                        current_entry.raw_text
            
            # Send the line to self.parse_line
            datestampnoyear, rawstamp, sourcehost, sourceprocess, \
                    sourcepid, message = self.parse_line(ourline)
           

            # Check for Dec-Jan jump and set the year:
            if int(datestampnoyear[0:4]) > int(recentdatestamp[0:4]):
                entryyear = entryyear - 1
            recentdatestamp = datestampnoyear

            
            
            # Split source process/PID
            # sourceproclist = attr_list[4].split('[')
            
            # Set our attributes:
            current_entry.raw_text = ourline
            current_entry.date_stamp_noyear = datestampnoyear
            current_entry.date_stamp = str(entryyear) \
                    + str(datestampnoyear)
            current_entry.tzone = tzone
            current_entry.raw_stamp = rawstamp
            current_entry.message = message
            current_entry.source_host = sourcehost
            current_entry.source_process = sourceprocess
            current_entry.source_pid = sourcepid
            current_entry.source_path = \
                    data.source_path

            # Append and reset current_entry
            newdata.entries.append(current_entry)
            current_entry = LogEntry()
        
        # Write the entries to the log object
        newdata.entries.reverse()
        return newdata


    def parse_line(self, line):
            match = re.findall(self.date_format, line)
            if match:
                attr_list = str(match[0]).split(' ')
                try:
                    attr_list.remove('')
                except ValueError:
                    pass

                # Account for lack of source host:
                # if options.nohost: attr_list.insert(3, None)

                # Get the date stamp (without year)
                months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
                        'Apr':'04', 'May':'05', 'Jun':'06', \
                        'Jul':'07', 'Aug':'08', 'Sep':'09', \
                        'Oct':'10', 'Nov':'11', 'Dec':'12'}
                intmonth = months[attr_list[0].strip()]
                daydate = str(attr_list[1].strip()).zfill(2)
                timelist = str(str(attr_list[2]).replace(':',''))
                datestampnoyear = str(intmonth) + str(daydate) + str(timelist)
                
                # Split source process/PID
                
                # Set our attributes:
                sourcehost = attr_list[3]
                sourceproclist = attr_list[4].split('[')
                sourceprocess = sourceproclist[0]
                if len(sourceproclist) > 1:
                    sourcepid = sourceproclist[1].strip(']')
                else: sourcepid = None
                rawstamp = line[:len(match[0])]
                message = line[len(match[0]) + 2:]

                
                return datestampnoyear, rawstamp, sourcehost, sourceprocess, \
                        sourcepid, message


            else: return None

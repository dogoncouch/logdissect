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
import gzip
from logdissect.parsers.type import ParseModule as OurModule
from logdissect.data import LogEntry
from logdissect.data import LogData

class ParseModule(OurModule):
    def __init__(self):
        """Initialize the no-host syslog parsing module"""
        self.name = 'nohost'
        self.desc = 'syslog (without host) parsing module'
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\[?\d*\]?):")
        self.tzone = None



    def parse_file(self, sourcepath):
        """Parse a syslog file with no host fields into a LogData object"""
        data = LogData()
        data.source_path = sourcepath
        data.parser = 'nohost'
        current_entry = LogEntry()
        data.source_file = data.source_path.split('/')[-1]

        # Set our start year:
        data.source_file_mtime = \
                os.path.getmtime(data.source_path)
        timestamp = \
                datetime.datetime.fromtimestamp(data.source_file_mtime)
        data.source_file_year = timestamp.year
        entryyear = timestamp.year
        currentmonth = '99'
        
        # Set our timezone
        if not self.tzone:
            if time.daylight:
                self.tzone = \
                        str(int(float(time.altzone) / 60 // 60)).rjust(2,
                                '0') + \
                        str(int(float(time.altzone) / 60 % 60)).ljust(2, '0')
            else:
                self.tzone = \
                        str(int(float(time.timezone) / 60 // 60)).rjust(2,
                                '0') + \
                        str(int(float(time.timezone) / 60 % 60)).ljust(2, '0')
            if not '-' in self.tzone:
                self.tzone = '+' + self.tzone


        # Parsing works in reverse. This helps with multi-line entries,
        # and logs that span multiple years (December to January shift).
        
        # Get our lines:
        fparts = sourcepath.split('.')
        if fparts[-1] == 'gz':
            with gzip.open(str(sourcepath), 'r') as logfile:
                loglines = reversed(logfile.readlines())
        else:
            with open(str(data.source_path), 'r') as logfile:
                loglines = reversed(logfile.readlines())

        # Parse our lines:
        for line in loglines:
            ourline = line.rstrip()
            
            # Send the line to self.parse_line

            entry = self.parse_line(ourline)

            datestampnoyear = entry['year'] + entry['month'] + \
                    entry['day'] + entry['tstamp']
           
            # Check for Dec-Jan jump and set the year:
            if int(entry['month']) > int(currentmonth):
                entryyear = entryyear - 1
            currentmonth = entry['month']

            # Set our attributes:
            current_entry.parser = 'nohost'
            current_entry.raw_text = ourline
            current_entry.date_stamp_noyear = date_stamp_noyear
            current_entry.date_stamp = str(entryyear) + \
                    entry['month'] + entry['day'] + entry['tstamp']
            current_entry.year = str(entryyear)
            current_entry.month = entry['month']
            current_entry.day = entry['day']
            current_entry.tstamp = entry['tstamp']
            current_entry.tzone = self.tzone
            current_entry.date_stamp_utc = current_entry._utc_date()
            current_entry.raw_stamp = entry['raw_stamp']
            current_entry.message = entry['message']
            current_entry.source_host = None
            current_entry.source_process = entry['source_process']
            current_entry.source_pid = entry['source_pid']
            current_entry.source_path = \
                    data.source_path


            # Append and reset current_entry
            data.entries.append(current_entry)
            current_entry = LogEntry()
        
        # Write the entries to the log object
        data.entries.reverse()
        return data


    def parse_line(self, line):
        """Parse a syslog line (with no host) into a dictionary"""
        match = re.findall(self.date_format, line)
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
            intmonth = months[attr_list[0].strip()]
            daydate = str(attr_list[1].strip()).zfill(2)
            timelist = str(str(attr_list[2]).replace(':',''))
            
            # Set our attributes:
            sourceproclist = attr_list[3].split('[')
            if len(sourceproclist) > 1:
                sourcepid = sourceproclist[1].strip(']')
            else: sourcepid = None
            
            entry = {}
            entry['year'] = None
            entry['month'] = intmonth
            entry['day'] = daydate
            entry['tstamp'] = str(timelist)
            entry['tzone'] = None
            entry['raw_stamp'] = line[:len(match[0])]
            entry['facility'] = None
            entry['severity'] = None
            entry['source_host'] = None
            entry['source_port'] = None
            entry['source_process'] = sourceproclist[0]
            entry['source_pid'] = sourcepid
            entry['dest_host'] = None
            entry['dest_port'] = None
            entry['protocol'] = None
            entry['message'] = line[len(match[0]) + 2:]

            return entry
            
        else: return None

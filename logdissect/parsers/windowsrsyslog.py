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
from logdissect.data import LogEntry
from logdissect.data import LogData

class ParseModule(OurModule):
    def __init__(self):
        """Initialize the windows rsyslog agent parsing module"""
        self.name = 'windowsrsyslog'
        self.desc = 'windows rsyslog agent log parsing module'
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(.*)")
        self.fields = ['date_stamp', 'source_host', 'source_process',
            'message']
        self.tzone = None



    def parse_file(self, sourcepath):
        """Parse a windows rsyslog agent file into a LogData object"""
        data = LogData()
        data.parser = 'syslog'
        current_entry = LogEntry()
        data.source_path = sourcepath
        data.source_file = data.source_path.split('/')[-1]

        # Set our start year:
        data.source_file_mtime = \
                os.path.getmtime(data.source_path)
        timestamp = \
                datetime.fromtimestamp(data.source_file_mtime)
        data.source_file_year = timestamp.year
        entryyear = timestamp.year
        currentmonth = '99'

        # Set our timezone
        if not self.tzone:
            if time.localtime().tm_isdst:
                self.tzone = \
                        str(int(float(time.altzone) / 60 // 60)).rjust(2,
                                '0') + \
                        str(int(float(time.altzone) / 60 % 60)).ljust(2, '0')
            else:
                self.tzone = \
                        str(int(float(time.timezone) / 60 // 60)).rjust(2,
                                '0') + \
                        str(int(float(time.timezone) / 60 % 60)).ljust(2, '0')
            if not '-' in self.tzone and not '+' in self.tzone:
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

            if not entry: continue

            # Check for Dec-Jan jump and set the year:
            if int(entry['month']) > int(currentmonth):
                entryyear = entryyear - 1
            currentmonth = entry['month']


            # Set our attributes:
            current_entry.parser = 'syslogbsd'
            current_entry.raw_text = ourline
            current_entry.date_stamp = str(entryyear) \
                    + entry['month'] + entry['day'] + entry['tstamp']
            current_entry.year = str(entryyear)
            current_entry.month = entry['month']
            current_entry.day = entry['day']
            current_entry.tstamp = entry['tstamp']
            current_entry.tzone = self.tzone
            current_entry.date_stamp_utc = current_entry._utc_date()
            current_entry.raw_stamp = entry['raw_stamp']
            current_entry.message = entry['message']
            current_entry.source_host = entry['source_host']
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
        """Parse a windows rsyslog agent line into a dictionary"""
        match = re.findall(self.date_format, line)
        if match:
            entry = {}
            entry['facility'] = None
            entry['severity'] = None
            entry['source_host'] = None
            entry['source_port'] = None
            entry['source_process'] = None
            entry['source_pid'] = None
            entry['dest_host'] = None
            entry['dest_port'] = None
            entry['protocol'] = None
            entry['message'] = None

            matchlist = list(zip(self.fields, match[0]))
            for f, v in matchlist:
                entry[f] = v


            # Get the date stamp (without year)
            months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
                    'Apr':'04', 'May':'05', 'Jun':'06', \
                    'Jul':'07', 'Aug':'08', 'Sep':'09', \
                    'Oct':'10', 'Nov':'11', 'Dec':'12'}
            datelist = entry['date_stamp'].split(' ')
            try:
                datelist.remove('')
            except ValueError:
                pass
            intmonth = months[datelist[0].strip()]
            daydate = str(datelist[1].strip()).zfill(2)
            timestring = str(datelist[2]).replace(':','')
            datestampnoyear = intmonth + daydate + timestring


            # Set our attributes:
            entry['year'] = None
            entry['month'] = intmonth
            entry['day'] = daydate
            entry['tstamp'] = str(timestring)
            entry['tzone'] = None
            entry['raw_stamp'] = None # doesn't work with new method

            return entry


        else: return None

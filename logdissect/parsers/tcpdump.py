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
import time
from logdissect.parsers.type import ParseModule as OurModule
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData

class ParseModule(OurModule):
    def __init__(self, options):
        """Initialize the tcpdump terminal output parsing module"""
        self.name = 'tcpdump'
        self.desc = 'tcpdump terminal output parsing module'
        self.date_format = \
                re.compile(r"^(\d{2}:\d{2}:\d{2}\.\d+\s+\w+,?\s?\w?\s+[\w\-\.]+\s+>\s+[\w\-\.]+):")



    def parse_log(self, data, options):
        """Parse tcpdump terminal output from file into a LogData object"""
        newdata = data
        newdata.parser = 'tcpdump'
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
        entry_month = timestamp.month
        entry_day = timestamp.day
        oldtnum = 999999.999999
        currentday = timestamp
        
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
            if current_entry.raw_text:
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
                
                tstamp = attr_list[0].replace(':', '')
                if attr_list[1][-1] == ',':
                    protocol = attr_list[1] + attr_list.pop(2)
                else:
                    protocol = attr_list[1]
                rawstamp = ourline[:len(match[0])]
                message = ourline[len(match[0]) + 2:]
                sourcehost = attr_list[2]
                desthost = attr_list[4]
                tnum = float(tstamp)

                # Set the current day:
                if float(tstamp) > oldtnum:
                    currentday = currentday - datetime.timedelta(days=1)

                ymdstamp = currentday.strftime('%Y%m%d')
                
                # Set the attributes for current_entry:
                current_entry.date_stamp = ymdstamp + tstamp
                current_entry.tzone = tzone
                current_entry.raw_stamp = rawstamp
                current_entry.message = message
                current_entry.source_host = sourcehost
                current_entry.dest_host = desthost
                current_entry.protocol = protocol
                current_entry.source_path = data.source_path


                # Append and reset current_entry
                newdata.entries.append(current_entry)
                current_entry = LogEntry()
                oldtnum = float(tstamp)
        
        # Write the entries to the log object
        newdata.entries.reverse()
        return newdata

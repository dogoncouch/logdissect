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

import re
from LogDissect.parsers.type import ParseModule as OurModule
from LogDissect.data.data import LogEntry
from LogDissect.data.data import LogData

class ParseModule(OurModule):
    def __init__(self):
        self.data = LogData()
        self.date_stamp_format = "" # To Do: add this
        pass

    def parse_date(self, options):
        # To Do: lots
        line.replace('Feb', '02')
        pass

    def parse_entry(self, options):
        pass

    def run_parse(self, options):
	current_entry = LogEntry()
        source_file_mtime = os.path.getmtime(self.data.source_fullpath)
        #To Do: strip year out of mtime
        entry_year = None
        last_date_stamp = None

	with open(self.data.source_full_path) as logfile:
            loglines = reversed(logfile.readlines())
        for line in loglines:
            line = line.rstrip()
            current_entry.raw_text = line + '\n' + current_entry.raw_text
            # To Do: get date stamp
            if line.startswith(self.date_stamp_format):
                current_entry.date_stamp = # To Do
                current_entry.year = # To Do
                current_entry.date_stamp_year = # To Do

                # Check if we just jumped to last year:
                if current_entry.date_stamp > last_date_stamp:
                    if entry_year:
                        entry year = entry_year - 1
                self.data.entries.append(current_entry)
                last_date_stamp = current_entry.date_stamp
                current_entry = LogEntry()
        
        self.data.entries = reversed(self.data.entries)

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

from os import path


class LogEntry:
    def __init__(self, options):
        """Initialize a log entry"""
        self.date_stamp = None
        # For datestamps that include a year:
        self.date_stamp_year = None
        self.raw_text = ""
        self.source_full_path = ""


class LogData:
    def __init__(self):
        """Initialize parsing for a log file"""
        self.lines = []
        self.entries = []
        self.parser = ""
        # self.date_stamp_format = ""
        self.source_full_path = ""
        self.source_file = ""
        self.source_file_mtime = ""
        self.source_file_time = ""
        self.source_file_year = "" # To Do
        self.abcdetc_name = "" # To Do
        self.first_date_stamp = None
        self.first_date_stamp_year = None
        self.last_date_stamp = None
        self.last_date_stamp_year = None
        
# =============================
# Move parsing function to parser
# 
#     def parse_log(self):
#         """Parse a log file into a dictionary"""
# 
#         # Should return a list of individual entries.
#         # Should be called with source_full_path as option.
#         current_entry = LogEntry()
#         source_file_mtime = os.path.getmtime(source_fullpath)
#         # To Do: strip year out of mtime
#         entry_year = None
#         last_date_stamp = None
#         
#         # Read the file in reverse and clean up the lines:
#         with open(self.source_full_path) as logfile:
#             loglines = reversed(logfile.readlines())
#         for line in loglines:
#             line = line.rstrip()
#             current_entry.raw_text = line + '\n' + current_entry.raw_text
#             # To Do: get date stamp
#             if line.startswith(self.date_stamp_format):
#                 current_entry.date_stamp = # To Do
#                 current_entry.year = # To Do
#                 current_entry.date_stamp_year = # To Do
# 
#                 # Check if we just jumped to last year:
#                 if current_entry.date_stamp > last_date_stamp:
#                     if entry_year:
#                         entry year = entry_year - 1
#                 self.entries.append(current_entry)
#                 last_date_stamp = current_entry.date_stamp
#                 current_entry = LogEntry()
#         
#         self.entries = reversed(self.entries)
#
# ==========================

    # To Do: Move range into morph module.
    # def range(self, options):
    #     """Isolate a specific date range"""
    #     pass

class LogDataSet:
    def __init__(self):
        """Initialize data set for multiple parsed logs"""
        self.source_full_paths = []
        self.data_set = []
        self.finalized_data = LogData()
        # To Do: Add more parsers later
        self.parser = 'syslog'
        # To Do: set creation date to runtime
        self.creation_date = None
        # To Do: update options for finalized data

    def read_logs(self):
        """Read in a log file"""
        for logfile in self.source_full_paths:
            newlog = LogData(source_full_path=logfile, parser=self.parser)
            newlog.parse_log()
            self.data_set.append(newlog)

    def merge(self):
        """Merge set of log data into one sorted instance"""
        pass

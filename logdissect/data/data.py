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


class LogEntry:
    def __init__(self):
        """Initialize a log entry"""
        self.parser = None
        self.date_stamp_noyear = None
        self.date_stamp = None
        self.tzone = None # new
        self.raw_text = None
        self.raw_stamp = None # new
        self.facility = None # new
        self.severity = None # new
        self.message = None # new
        self.source_path = None
        self.source_host = None
        self.source_port = None # To Do
        self.source_process = None
        self.source_pid = None
        self.dest_host = None # new
        self.dest_port = None # To Do
        self.protocol = None # new
        # self.date_stamp_noyear = None
        # self.date_stamp = None
        # self.tzone = "" # new
        # self.raw_text = ""
        # self.source_path = ""
        # self.source_host = ""
        # self.source_port = "" # To Do
        # self.source_process = ""
        # self.source_pid = None
        # self.dest_host = "" # new
        # self.dest_port = "" # To Do
        # self.protocol = "" # new
        # self.raw_stamp = ""
        # self.message = "" # new


class LogData:
    def __init__(self):
        """Initialize data object for a log file"""
        self.entries = []
        self.source_path = None
        self.source_file = None
        self.source_file_mtime = None
        self.parser = None
        
class LogDataSet:
    def __init__(self):
        """Initialize data object for multiple parsed logs"""
        self.data_set = []
        self.finalized_data = LogData()

    def merge_logs(self):
        """Merge data sets together into finalized_data"""
        ourlog = LogData()
        for l in self.data_set:
            ourlog.entries = ourlog.entries + l.entries
        ourlog.entries.sort(key=lambda x: float(x.date_stamp))
        self.finalized_data = ourlog

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

    def _date_to_utc(self):
        if int(self.tzone) < 0 and self.tzone[-2] == '30':
            tminus = self.tzone[:-2] + '70'
            return float(self.date_stamp) + int(self.tzone)
        else:
            return float(self.date_stamp) + int(self.tzone)


class LogData:
    def __init__(self):
        """Initialize data object for a log file"""
        self.entries = []
        self.source_path = None
        self.source_file = None
        self.source_file_mtime = None
        self.parser = None

    def sort_time(self):
        """Sort entries by datestamp"""
        self.entries.sort(key=lambda x: x._date_to_utc())
        # self.entries.sort(key=lambda x: float(x.date_stamp) + int(x.tzone))

    def sort_path(self):
        """Sort entries by source path"""
        self.entries.sort(key=lambda x: x.source_path)

    def sort_facility(self):
        """sort entries by facility, then severity"""
        self.entries.sort(key=lambda x: x.severity)
        self.entries.sort(key=lambda x: x.facility)


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
        ourlog.sort_time()
        self.finalized_data = ourlog

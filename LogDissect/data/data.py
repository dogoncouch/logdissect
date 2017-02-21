# MIT License
# 
# Copyright (c) 2017 Dan Persons
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
    def __init__(self, options):
        """Initialize a log entry"""
        self.date_stamp=None
        # For datestamps that include a year:
        self.date_stamp_year=None
        self.raw_text=""
        self.source_file=""
        self.source_file_path=""
        self.source_file_atime=""
        self.parser=""

class LogData:
    def __init__(self, options):
        """Initialize parsing for a log file"""
        self.lines=[]
        self.entries={}
        self.source_file=""
        self.source_file_path=""
        self.source_file_atime=""
        self.abcdetc_name=""
        self.output_file=""
        pass

    def parse_log(self, options):
        """Parse a log file into a dictionary"""
        pass

    # TO DO: Move range into morph module.
    def range(self, options):
        """Isolate a specific date range"""
        pass

class LogDataSet:
    def __init__(self, options):
        """Initialize data set for multiple parsed logs"""
        self.data_set = []
        pass

    def read_log(self, options):
        """Read in a log file"""
        pass

    def merge(self, options):
        """Merge two logs in chronological order"""
        pass

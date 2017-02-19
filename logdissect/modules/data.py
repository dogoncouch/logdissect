#!/usr/bin/python

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

class LogData:
    def __init__(self, options):
        """Initialize parsing for a log file"""
        self.lines=[]
        self.entries={}
        self.outputfile=""
        pass

    def parse_dict(self, options):
        """Parse a log file into a dictionary"""
        pass

    def range(self, options):
        """Isolate a specific date range"""
        pass

class DataSet:
    def __init__(self, options):
        """Initialize data set for multiple parsed logs"""
        dataset = []
        pass

    def read_log(self, options):
        """Read in a log file"""
        pass

    def merge(self, options):
        """Merge two logs in chronological order"""
        pass


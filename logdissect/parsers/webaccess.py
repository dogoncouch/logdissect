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

from logdissect.parsers.type import ParseModule as OurModule

class ParseModule(OurModule):
    def __init__(self, options=[]):
        """Initialize a log parsing module"""
        self.name = 'webaccess'
        self.desc = 'web access log parsing module'
        self.date_format = \
                '^(\S+)\s+-\s+-\s+\[(\S+)\s+([0-9+-]+)\]\s+"(\S+)\s+(\S+)\s+(\S+)"\s+(\d+)\s+(\d+)\s+"(\S+)"\s+"(.*)"'
        self.fields = ['source_host', 'date_stamp', 'tzone', 'method',
                'path', 'protocol', 'status', 'byte_count',
                'referrer', 'user_agent_string']
        self.backup_date_format = \
                '^(\S+)\s+-\s+-\s+\[(\S+)\]\s+"(\S+)\s+(\S+)\s+(\S+)"\s+(\d+)\s+(\d+)\s+"(\S+)"\s+"(.*)"'
        self.backup_fields = ['source_host', 'date_stamp', 'method',
                'path', 'protocol', 'status', 'byte_count',
                'referrer', 'user_agent_string']
        self.tzone = None
        self.datestamp_type = 'webaccess'

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
from logdissect.filters.type import FilterModule as OurModule

class FilterModule(OurModule):
    def __init__(self, args=None):
        """Initialize the rprotocol filter module"""
        self.name = "rprotocol"
        self.desc = "filter out a protocol"

        if args:
            args.add_argument('--rprotocol', action='append', dest='rprotocol',
                    metavar='PROTOCOL', help='filter out a protocol')

    def filter_data(self, data, values=None, args=None):
        """Return entries without specified protocol (single log)"""
        if args:
            if not args.rprotocol:
                return data
        if not values: values = args.rprotocol
        newdata = {}
        if 'parser' in data.keys():
            newdata['parser'] = data['parser']
            newdata['source_path'] = data['source_path']
            newdata['source_file'] = data['source_file']
            newdata['source_file_mtime'] = data['source_file_mtime']
            newdata['source_file_year'] = data['source_file_year']
        newdata['entries'] = []

        for entry in data['entries']:
            if 'protocol' in entry.keys():
                if entry['protocol'] not in values:
                    newdata['entries'].append(entry)
            else:
                newdata['entries'].append(entry)

        return newdata

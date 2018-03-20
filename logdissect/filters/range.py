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

from logdissect.filters.type import FilterModule as OurModule

class FilterModule(OurModule):
    def __init__(self, args):
        """Initialize the range filter module"""
        self.name = "range"
        self.desc = "match a time range (YYYYMMDDhhmm-YYYYMMDDhhmm)"

        args.add_argument('--range', action='store', dest='range',
                help='match a time range (YYYYMMDDhhmm-YYYYMMDDhhmm)')
        args.add_argument('--utc', action='store_true', dest='utc',
                help='use UTC for range matching')

    def filter_data(self, data, args):
        """Morph log data by timestamp range (single log)"""
        if not args.range:
            return data
        else:
            ourlimits = args.range.split('-')

            newdata = data
            newdata['entries'] = []

            firstdate = int(ourlimits[0].ljust(14, '0'))
            lastdate = int(ourlimits[1].ljust(14, '0'))
            if args.utc:
                for entry in data['entries']:
                    if int(entry['numeric_date_stamp_utc']) >= firstdate: 
                        if int(entry['numeric_date_stamp_utc']) <= lastdate:
                            newdata['entries'].append(entry)
            else:
                for entry in data['entries']:
                    if int(entry['numeric_date_stamp']) >= firstdate: 
                        if int(entry['numeric_date_stamp']) <= lastdate:
                            newdata['entries'].append(entry)

            return newdata

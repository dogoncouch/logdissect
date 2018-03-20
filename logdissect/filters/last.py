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
from time import strftime
from datetime import datetime, timedelta

class FilterModule(OurModule):
    def __init__(self, args):
        """Initialize the 'last' filter module"""
        self.name = "last"
        self.desc = "match a preceeding time period (e.g. 5m/3h/2d/etc)"

        args.add_argument('--last', action='store', dest='last',
                help='match a preceeding time period (e.g. 5m/3h/2d/etc)')

    def filer_data(self, data, args):
        """Morph log data by preceeding time period (single log)"""
        if not args.last:
            return data
        else:
            # Set the units and number from the option:
            lastunit = args.last[-1]
            lastnum = args.last[:-1]
            
            # Set the start time:
            if lastunit == 's':
                starttime = datetime.utcnow() - \
                        timedelta(seconds=int(lastnum))
            if lastunit == 'm':
                starttime = datetime.utcnow() - \
                        timedelta(minutes=int(lastnum))
            if lastunit == 'h':
                starttime = datetime.utcnow() - \
                        timedelta(hours=int(lastnum))
            if lastunit == 'd':
                starttime = datetime.utcnow() - \
                        timedelta(days=int(lastnum))
            ourstart = starttime.strftime('%Y%m%d%H%M%S')
            
            # Pull out the specified time period:
            newdata = data
            newdata['entries'] = []

            for entry in data['entries']:
                if int(entry['numeric_date_stamp_utc']) >= int(ourstart): 
                    newdata['entries'].append(entry)

            return newdata

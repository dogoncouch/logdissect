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

from logdissect.morphers.type import MorphModule as OurModule
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData
from time import strftime
import datetime

class MorphModule(OurModule):
    def __init__(self, options):
        """Initialize the 'last' morphing module"""
        self.name = "last"
        self.desc = "Specifies preceeding time period"

        options.add_option('--last', action='append', dest='last',
                help='specifies preceeding time period (5m/3h/2d/etc)')

    def morph_data(self, data, options):
        """Morph log data by preceeding time period (single log)"""
        if not options.last:
            return data
        else:
            # Set the units and number from the option:
            lastunit = options.last[0][-1]
            lastnum = options.last[0][:-1]
            
            # Set the start time:
            if lastunit == 's':
                starttime = datetime.datetime.now() - \
                        datetime.timedelta(seconds=int(lastnum))
            if lastunit == 'm':
                starttime = datetime.datetime.now() - \
                        datetime.timedelta(minutes=int(lastnum))
            if lastunit == 'h':
                starttime = datetime.datetime.now() - \
                        datetime.timedelta(hours=int(lastnum))
            if lastunit == 'd':
                starttime = datetime.datetime.now() - \
                        datetime.timedelta(days=int(lastnum))
            ourstart = starttime.strftime('%Y%m%d%H%M%S')
            
            # Pull out the specified time period:
            newdata = LogData()
            for entry in data.entries:
                if int(entry.date_stamp_year) >= int(ourstart): 
                    newdata.entries.append(entry)
            return newdata

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

import time
from datetime import datetime

def get_blank_entry():
    """Return a blank entry dictionary"""
    entry = {}
    entry['parser'] = None
    entry['date_stamp'] = None
    entry['tzone'] = None
    entry['facility'] = None
    entry['severity'] = None
    entry['log_source']
    entry['source_host'] = None
    entry['source_port'] = None
    entry['source_process'] = None
    entry['source_pid'] = None
    entry['dest_host'] = None
    entry['dest_port'] = None
    entry['protocol'] = None
    entry['message'] = None

    return entry

def convert_standard_datestamp(entry):
    """Set date and time attributes based on a standard date stamp"""
    # Get the date stamp (without year)
    months = {'Jan':'01', 'Feb':'02', 'Mar':'03', \
            'Apr':'04', 'May':'05', 'Jun':'06', \
            'Jul':'07', 'Aug':'08', 'Sep':'09', \
            'Oct':'10', 'Nov':'11', 'Dec':'12'}
    datelist = entry['date_stamp'].split(' ')
    try:
        datelist.remove('')
    except ValueError:
        pass
    intmonth = months[datelist[0].strip()]
    daydate = datelist[1].strip().zfill(2)
    timestring = datelist[2].replace(':','')
    datestampnoyear = intmonth + daydate + timestring

    # Set attributes:
    entry['year'] = None
    entry['month'] = intmonth
    entry['day'] = daydate
    entry['tstamp'] = timestring
    entry['tzone'] = None

    return entry


def convert_iso_datestamp(entry):
    """Set date and time attributes based on an iso date stamp"""
    # Set our attributes:
    if entry['date_stamp'][-1] == 'Z':
        tzone = '+0000'
        datestamp = entry['date_stamp'][:-1].strip('-').strip('T').strip(':')
    else:
        tzone = entry['date_stamp'][-5:].strip(':')
        datestamp = entry['date_stamp'][:-6].strip('-').strip('T').strip(':')

    entry['year'] = datestamp[0:4]
    entry['month'] = datestamp[4:6]
    entry['day'] = datestamp[6:8]
    entry['tstamp'] = datestamp[8:]
    entry['tzone'] = tzone

    return entry


def get_utc_date(entry):
    """Return datestamp converted to UTC"""
    if entry['numeric_date_stamp'] == '0':
        entry['numeric_date_stamp_utc'] = '0'
        return entry

    else:
        if '.' in entry['numeric_date_stamp']:
            t = datetime.datetime.strptime(entry['numeric_date_stamp'],
                    '%Y%m%d%H%M%S.%f')
        else:
            t = datetime.datetime.strptime(entry['numeric_date_stamp'],
                    '%Y%m%d%H%M%S')
        tdelta = datetime.timedelta(hours = int(entry['tzone'][1:3]),
                minutes = int(entry['tzone'][3:5]))
        
        if self.tzone[0] == '-':
            ut = t - tdelta
        else:
            ut = t + tdelta

        entry['numeric_date_stamp_utc'] = ut.strftime('%Y%m%d%H%M%S.%f')
        
        return entry


def get_local_tzone():
    """Get the current time zone on the local host"""
    if time.localtime().tm_isdst:
        tzone = \
                str(int(float(time.altzone) / 60 // 60)).rjust(2,
                        '0') + \
                str(int(float(time.altzone) / 60 % 60)).ljust(2, '0')
    else:
        tzone = \
                str(int(float(time.timezone) / 60 // 60)).rjust(2,
                        '0') + \
                str(int(float(time.timezone) / 60 % 60)).ljust(2, '0')
    if not '-' in tzone and not '+' in tzone:
        tzone = '+' + tzone

    return tzone


def merge_logs(dataset):
    """Merge log dictionaries together into one log dictionary"""
    ourlog = {}
    ourlog['entries'] = []
    for d in dataset:
        ourlog['entries'] = ourlog['entries'] + d['entries']
    ourlog['entries'] = ourlog['entries'].sort(
            key= lambda x: x['numeric_date_stamp_utc'])

    return ourlog

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

from time import localtime
from time import timezone
from time import altzone
from datetime import datetime, timedelta

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


def convert_nodate_datestamp(entry, datedata):
    """Set date and time attributes based on timestamp with no date"""
    entry['tstamp'] = entry['date_stamp'].replace(':', '')
    # Remember, we're parsing in reverse.
    if float(entry['tstamp']) > datedata['entry_time']:
        datedata['timestamp'] = datedata['timestamp'] - timedelta(days=1)
    if '.' in entry['tstamp']:
        datedata['entry_time'] = int(entry['tstamp']).split('.')[0]
    else:
        datedata['entry_time'] = int(entry['tstamp'])
    entry['year'] = str(datedata['timestamp'].year)
    entry['month'] = str(datedata['timestamp'].month)
    entry['day'] = str(datedata['timestamp'].day)
    entry['numeric_date_stamp'] = entry['year'] + entry['month'] + \
            entry['day'] + entry['tstamp']

    return entry, datedata


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
    entry['numeric_date_stamp'] = entry['year'] + entry['month'] + \
            entry['day'] + entry['tstamp']

    return entry


def convert_unix_datestamp(entry):
    """Set date and time attributes based on a unix date stamp"""
    timestamp = datetime.fromtimestamp(float(entry['date_stamp']))
    entry['year'] = str(timestamp.year)
    entry['month'] = str(timestamp.month)
    entry['day'] = str(timestamp.day)
    entry['tstamp'] = str(timestamp.strftime('%H%M%S.%f'))
    entry['numeric_date_stamp'] = entry['year'] + entry['month'] + \
            entry['day'] + entry['tstamp']

    return entry


def convert_now_datestamp(entry):
    """Set date and time attributes based on a unix date stamp"""
    timestamp = datetime.now()
    entry['date_stamp'] = timestamp.strftime('%Y %b %d %H:%M:%S.%f')
    entry['year'] = str(timestamp.year)
    entry['month'] = str(timestamp.month)
    entry['day'] = str(timestamp.day)
    entry['tstamp'] = timestamp.strftime('%H%M%S.%f')
    entry['numeric_date_stamp'] = entry['year'] + entry['month'] + \
            entry['day'] + entry['tstamp']

    return entry


def get_utc_date(entry):
    """Return datestamp converted to UTC"""
    if entry['numeric_date_stamp'] == '0':
        entry['numeric_date_stamp_utc'] = '0'
        return entry

    else:
        if '.' in entry['numeric_date_stamp']:
            t = datetime.strptime(entry['numeric_date_stamp'],
                    '%Y%m%d%H%M%S.%f')
        else:
            t = datetime.strptime(entry['numeric_date_stamp'],
                    '%Y%m%d%H%M%S')
        tdelta = timedelta(hours = int(entry['tzone'][1:3]),
                minutes = int(entry['tzone'][3:5]))
        
        if entry['tzone'][0] == '-':
            ut = t - tdelta
        else:
            ut = t + tdelta

        entry['numeric_date_stamp_utc'] = ut.strftime('%Y%m%d%H%M%S.%f')
        
        return entry


def get_local_tzone():
    """Get the current time zone on the local host"""
    if localtime().tm_isdst:
        tzone = \
                str(int(float(altzone) / 60 // 60)).rjust(2,
                        '0') + \
                str(int(float(altzone) / 60 % 60)).ljust(2, '0')
    else:
        tzone = \
                str(int(float(timezone) / 60 // 60)).rjust(2,
                        '0') + \
                str(int(float(timezone) / 60 % 60)).ljust(2, '0')
    if not '-' in tzone and not '+' in tzone:
        tzone = '+' + tzone

    return tzone


def merge_logs(dataset):
    """Merge log dictionaries together into one log dictionary"""
    ourlog = {}
    ourlog['entries'] = []
    for d in dataset:
        ourlog['entries'] = ourlog['entries'] + d['entries']
    ourlog['entries'].sort(key= lambda x: x['numeric_date_stamp_utc'])

    return ourlog

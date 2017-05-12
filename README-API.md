# NOTICE:
### logdissect is now beta testing version 2.0!
To install the development version, follow the instructions in [README-TESTING.md](README-TESTING.md).

Read the changelog:
[https://github.com/dogoncouch/logdissect/CHANGELOG.md](https://github.com/dogoncouch/logdissect/CHANGELOG.md)

# logdissect API
For program documentation, see [README.md](README.md)

The logdissect module contains utilities for parsing, storing, filtering, and exporting log data.

## Synopsis
    import logdissect
    myparser = logdissect.parsers.syslogbsd.ParseModule()
    attribute_tuple = myparser.parse_line(<RAW_LINE>)
    logdataobject = myparser.parse_log(<LOG_FILE_PATH>)

## Description
The logdissect module comes with the logdissect log analysis program. It contains objects which can be used to parse log lines and files, and store log information. It also contains objects for filtering and outputting log information that have no user-friendly API at this point, but will in the future.

## Parsers
### logdissect.parsers.\<parser>.ParseModule()
Replace \<parser\> with one of the available parsers:

`` syslogbsd `` - standard syslog<br>
`` syslogiso `` - syslog with ISO 8601 datestamp<br>
`` nohost `` - syslog with no host attribute<br>
`` tcpdump `` - tcpdump terminal output<br>
`` ldjson `` - logdissect JSON output<br>
    
Parsers contain two methods (except the ldjson parser, which has no parse\_line() method):

### parse\_file(\<file>)
Accepts a filename as input, and outputs a LogData object (described below).

Parsers have a tzone attribute that uses standard ISO 8601 time zone formatting (e.g. `+0500`, `-0200`); if not set, logdissect will attempt to get current time zone data from the local system (unless a time zone is already present, such as in the syslogiso parser, or the ldjson parser).

### parse\_line(\<line>)
Accepts a log line as input, and outputs a tuple containing attributes. Tuples vary from parser to parser; their values are described in the docstrings for each parse\_line() method.

## Data Objects
### logdissect.data.LogEntry()
LogEntry is the data type for a single log entry. It contains the following attributes: `parser`, `date_stamp_noyear`, `date_stamp`, `date_stamp_utc`, `tzone`, `raw_text`, `raw_stamp`, `facility`, `severity`, `message`, `source_path` (the file it was parsed from), `source_host`, `source_port`, `source_process`, `source_pid`, `dest_host`, `dest_port`, `protocol`.

LogEntry also contains the `_utc_date` method, which uses the datestamp and timezone to convert its timestamp to UTC.

### logdissect.data.LogData()
LogData is the data type for a single log. It contains the following attributes: `entries` (a list containing LogEntry objects), `source_path` (the file it was parsed from), `source_file`, `source_file_mtime`, `parser`.

LogData also contains a few sorting methods. `` sort_time() `` sorts entries by their `date_stamp_utc` attribute. `` sort_path()  `` sorts by path. `` sort_facility `` sorts by facility, with each facility sorted by severity.

### logdissect.data.LogDataSet()
LogDataSet is the data type for a logdissect project. It contains the following attributes: `data_set` (a list containing LogData objects), `finalized_data` (a LogData object to hold all of the hold logs).

LogDataSet also contains the `` merge_logs() `` method, which merges the logs in `data_set` and sorts them using LogData's `sort_time()` method.

# Author
Dan Persons (dpersonsdev@gmail.com)

# Copyright
MIT License

Copyright (c) 2017 Dan Persons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# logdissect API
For program documentation, see [README.md](README.md)

The logdissect module contains utilities for parsing, storing, filtering, and exporting log data.

## Index
- [Introduction](#introduction)
- [Objects and Methods](#objects-and-methods)
  - [Parsers](#parsers)
- [Copyright](#copyright)

# Introduction
## Synopsis
    import logdissect
    myparser = logdissect.parsers.syslog.ParseModule()
    attribute_dict = myparser.parse_line(<RAW_LINE>)
    file_dict = myparser.parse_file(<PATH/TO/FILE>)

## Description
The logdissect module comes with the logdissect log analysis program. It contains objects which can be used to parse log lines and files.

# Objects and Methods

## Parsers
### logdissect.parsers.\<parser>.ParseModule()
Replace \<parser\> with one of the available parsers:

- `` ciscoios `` - Cisco IOS logs
- `` syslog `` - standard syslog
- `` syslogiso `` - syslog with ISO 8601 datestamp
- `` syslognohost `` - syslog with no host attribute
- `` tcpdump `` - tcpdump terminal output
- `` sojson `` - logdissect single-object JSON output
- `` linejson `` - logdissect object-per-line JSON output
- `` windowsrsyslog `` - windows rsyslog agent forwarded logs
    
Parsers have two methods (except the sojson parser, which has no parse\_line() method):

#### parse\_file(\<file>)
Accepts a filename as input, and returns a dictionary with some metadata, and a list of entry dictionaries (`entries`).

Parsers have a `tzone` attribute that uses standard ISO 8601 offset to UTC (e.g. `+0500`, `-0200`); if not set, logdissect will attempt to get current time zone data from the local system (unless a time zone is already present, such as in the syslogiso parser, or the sojson parser).

#### parse\_line(\<line>)
Accepts a log line as input, and returns a dictionary of strings. There are two built-in keys, `raw_text` and `parser`, and parsers can add their own keys.

Parsers have a `datestamp_type` attribute that defines how timestamps will be converted. The options are as follows:

- `standard` - Standard syslog date stamps
- `nodate` - Time stamps with no date (i.e. tcpdump)
- `iso` - ISO8601 timestamps
- `unix` - Unix timestamps
- `now` - Always set date stamp to time parsed
- `None` - Skip conversion

Conversion happens with any parser that has a `date_stamp` field in `fields` (the `now` datestamp type doesn't require a `date_stamp` field), and adds the following attributes to the entry dictionary:

- `year` - a 4-digit string (or None)
- `month` - a 2-digit string
- `day` - a 2-digit string
- `tstamp` - a 6-digit string with optional decimal and extra places
- `tzone` - `+` or `-` followed by a 4-digit offset to utc (HHMM)
- `numeric_date_stamp` - a datestamp in the form of YYYYmmddHHMMSS[.ffffff]
- `date_stamp` - a standard date stamp (added for `now` datestamp type only)

The sojson parser has no parse\_line() method.

# Copyright
MIT License

Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)

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

# Change log
Change log for [logdissect](https://github.com/dogoncouch/logdissect)

## [Unreleased]
### Added
- `post_parse_action` parser method for more customization

### Fixed
- Bug parsing gzipped files

## [3.0.2] 2018-03-25
### Fixed
- Reversed UTC time calculation bug

### Updated
- Renamed `date_format` parser attribute to `format_regex` for clarity

## [3.0.1] 2018-03-23
### Fixed
- `linejson` parser bug

## [3.0] 2018-03-22
### Added
- Cisco IOS parser
- Windows rsyslog agent parser
- Web access log parser
- `utils` functions
- API documentation for filters, outputs, utils

### Fixed
- Python3 --list-parsers error

### Updated
- Data is now stored in dicts instead of custom objects
- `log_source` attribute replaces old `source_host` for logs
- Parser logic is more modular
- Parsers can now use any fields
- Moved `morphers` to `filters`

## [2.2.1] - 2018-01-10
### Fixed
- Syslog parsers now ignore lines without stamp
- Daylight savings check logic

## [2.2] - 2017-07-03
### Added
- Support for multiple instances of all non-time-based morphers
- Python 3 library installation in Makefile

## [2.1] - 2017-06-14
### Added
- Python 3 compatibility

### Fixed
- Module loading issue (logdissect.data)

## [2.0.2] - 2017-06-13
### Fixed
- Python version issue

## [2.0.1] - 2017-06-07
### Fixed
- Compatibility issues

## [2.0] - 2017-05-30
### Added
- `tcpdump` parser for parsing tcpdump terminal output
- `parse_line()` parser functions
- More LogEntry attributes
- Morphers: `dest`, `rdest`, `rsource`, `rprocess`, `protocol`
- `syslogiso` parser for ISO 8601 datestamp format (ISODATE)
- More sorting methods (path, facility/severity)
- `_date_to_utc()` method for LogEntry objects
- Option to include archives compressed with gzip
- `-z` option to manually set time zone
- API documentation (README-API.md, man 3 logdissect)
- Instructions for contributing (README-DEV.md)

### Changed
- More data in JSON arrays
- Module redesign: geared toward public use
- Morph/output options now optional
- Removed parse options
- Changed `--no-host` option to `nohost` parser
- Moved `host` morpher to `source`
- Moved `injson` parser to `ldjson`
- Moved `parse_log()` functions to `parse_file()`
- Moved merge to LogDataSet method
- Moved sort to LogData method
- Updated time sort method to use time zones
- Renamed `syslog` parser to `syslogbsd`
- `logdissect` now loads everything when imported as a module
- `parse_line()` returns a predictable dictionary instead of random values

## [1.3.1] - 2017-04-24
### Added
- Add `--no-host` option for syslog configurations with no host attribute

## [1.3] - 2017-04-21
### Updated
- Migrate from optparse to argparse
- Move CHANGELOG to CHANGELOG.md
### Fixed
- Formatting in setup.py docstring

## [1.2.2] - 2017-04-01
### Fixed
- `syslog` parser: fix bug with extra whitespace in timestamp

## [1.2.1] - 2017-04-01
### Fixed
- `syslog` parser: typo (s/Oce/Oct/)
- `setup.py`: Changed long description to rst formatted docstring

## [1.2] - 2017-03-31
### Added
- `rgrep` morpher: reverse grep
- `outjson` output module for JSON
- `injson` parser module for JSON
- `host` morpher: match source host
- `process` morpher: match source process
- Dev tests for new modules

## [1.1.1] - 2017-03-28
### Fixed
- `syslog` parser no longer breaks without PID

## [1.1] - 2017-03-26
### Added
- `last` morpher
- Terminal output by default
- Silent and verbose options
- `source_host` and `source_process` attributes in `LogEntry` object

## [1.0] - 2017-03-21
- First stable release

# Change log
Change log for [logdissect](https://github.com/dogoncouch/logdissect)

## [Unreleased]
### Added
- `tcpdump` parser for parsing tcpdump terminal output
- `parse_line()` parser functions
- More LogEntry attributes
- Morphers: `dest`, `rdest`, `rsource`, `rprocess`, `protocol`
- `syslogiso` parser for ISO 8601 datestamp format (ISODATE)
- More sorting methods (path, facility/severity)
- Option to include archives compressed with gzip

### Changed
- More data in JSON arrays
- Module redesign: geared toward public use
- Morph/output options now optional
- Removed parse options
- Changed `--no-host` option to `nohost` parser
- Moved `host` parser to `source`
- Moved `injson` parser to `ldjson`
- Moved `parse_log()` functions to `parse_file()`
- Moved merge to LogDataSet method
- Moved sort to LogData method
- Updated time sort method to use time zones


## [1.3.1] - 2017-04-24
### Fixed
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

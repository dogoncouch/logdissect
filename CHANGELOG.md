# Change log
Change log for [logdissect](https://github.com/dogoncouch/logdissect)

## [Unreleased]
### Fixed
- Add '--no-host' option for syslog configurations with no host attribute

## [1.3] - 2017-04-21
### Updated
- Migrate from optparse to argparse
- Move CHANGELOG to CHANGELOG.md
### Fixed
- Formatting in setup.py docstring

## [1.2.2] - 2017-04-01
### Fixed
- 'syslog' parser: fix bug with extra whitespace in timestamp

## [1.2.1] - 2017-04-01
### Fixed
- 'syslog' parser: typo (s/Oce/Oct/)
- 'setup.py': Changed long description to rst formatted docstring

## [1.2] - 2017-03-31
### Added
- 'rgrep' morpher: reverse grep
- 'outjson' output module for JSON
- 'injson' parser module for JSON
- 'host' morpher: match source host
- 'process' morpher: match source process
- Dev tests for new modules

## [1.1.1] - 2017-03-28
### Fixed
- 'syslog' parser no longer breaks without PID

## [1.1] - 2017-03-26
### Added
- 'last' morpher
- Terminal output by default
- Silent and verbose options
- source host and source process attributes in LogEntry object

## [1.0] - 2017-03-21
- First stable release

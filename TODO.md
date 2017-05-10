# To Do
To do list for [logdissect](https://github.com/dogoncouch/logdissect)

## v2.0

### Update
- Parsers: make options a keyword arg (default to empty list)
- Update JSON arrays: add `LogData` attributes (parser, file, mtime)
- Update dev tests for new JSON attributes, etc.

### Add
- `ISODATE` parser
- `rhost` morph option
- `rprocess` morph option
- Option to include zipped files ('# To Do:' pointers in core.py, syslog.py)

### Document
- Library use - `parse_line()`, `parse_log()`, data types, morphers

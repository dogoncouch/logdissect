# To Do
To do list for [logdissect](https://github.com/dogoncouch/logdissect)

## v2.0

### Update
- Parsers: make options a keyword arg (default to empty list)
- Update JSON arrays: add `LogData` attributes (parser, file, mtime)
- Update `tcpdump` parser: `parse_line()` function: handle ARP
- Update dev tests for new JSON attributes, etc.
- `parse_line()`: backup in case `parse_line()` returns `None`

### Add
- `ISODATE` parser
- `rhost` morph option
- `rprocess` morph option
- Option to include zipped files

### Document
- Library use - `parse_line()`, `parse_log()`, data types, morphers

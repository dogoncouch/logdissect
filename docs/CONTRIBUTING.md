# Contributing to logdissect
Contributions are welcome in the form of code or testing feedback. All contributors are expected to follow our [code of conduct](CODE_OF_CONDUCT.md).

## Index

- [Testing](#testing)
- [Coding](#coding)
  - [Parser Modules](#parser-modules)
  - [Filter Modules](#filter-modules)
  - [Output Modules](#output-modules)
- [Installing Development Source](#installing-development-source)
- [Usage](#usage)

## Testing
User feedback helps logdissect get better. All issues and comments can be directed to the [issues page on GitHub](https://github.com/dogoncouch/logdissect/issues), or emailed to [dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com). Please ensure you are using the latest release.

Issues based on bugs should be well documented, with any error message and an explanation of how the issue can be reproduced. Additional information such as Python version and operating system are also useful.

## Coding
If you have a bug fix, or an idea for a module, we would love to hear about it! You can start an [issue on GitHub](https://github.com/dogoncouch/logdissect/issues), or email the author at [dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com).

All new modules should be based on the `dev` branch. New modules usually don't require any editing of existing files (except `__init__.py` files), so conflicts shouldn't be much of an issue. Get in touch beforehand if you need to change other existing files for your module, or if you want to add to `logdissect.utils`.

Code should run with both Python 2 and 3. Coding style should be as simple and readable as possible. Variable names should tell you exactly what a variable does. Use four spaces for indentation (no tabs), and avoid one-liners; equivalent blocks of code are usually easier to read.

### Parser Modules
Creating a parser module is as simple as coming up with a regular expression, and some fields for it to parse. Parse modules are not limited to built-in fields; any field names can be defined. There is an example blank parser in `logdissect/parsers/blank.py`. Set the `datestamp_type` attribute for automatic date stamp conversion, which is required for merging and sorting logs. The options for `datestamp_type` are as follows:

- `standard` - Standard syslog date stamps
- `nodate` - Time stamps with no date (i.e. tcpdump)
- `iso` - ISO8601 timestamps
- `unix` - Unix timestamps
- `now` - Always set date stamp to time parsed
- `None` - Skip conversion

The name of your parse module should be added to the `all` variable and imported in `logdissect/parsers/__init__.py`. More information on parser modules can be found in the [API documentation](README-API.md#parser-modules).

### Filter Modules
Creating a filter module is a bit more difficult. Check out the [filter API documentation](README-API.md#filters-modules), and look at existing filter modules to get an idea of how filters work. There is an example blank filter in `logdissect/filters/blank.py`. Once you have created a filter module, add it to the `all` variable and import it in `logdissect/filters/__init__.py`.

### Output Modules
Check out the [output API documentation](README-API.md#output-modules), and look at existing output modules to get an idea of how outputs work. There is an example blank output in `logdissect/output/blank.py`. Once you have created an output module, add it to the `all` variable and import it in `logdissect/output/__init__.py`.

## Installing Development Source
To install the latest development version of `` logdissect `` from source, follow these instructioons:

Requirements: git, python-setuptools

    git clone https://github.com/dogoncouch/logdissect.git
    cd logdissect
    sudo make all

## Usage
For usage instructions, see [README.md](../README.md).

For API documentation, see [README-API.md](README-API.md)

#!/usr/bin/env python

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

import sys
import string
import LogDissect.data
import LogDissect.parsers
import LogDissect.morphers
import LogDissect.output
from LogDissect import __version__
from optparse import OptionParser
from optparse import OptionGroup

class LogDissectCore:

    def __init__(self):
        """Initialize logdissect job"""
        self.input_files = []
        self.parse_modules = {}
        self.morph_modules = {}
        self.output_modules = {}
        # LogDataSet from data objects:
        self.data_set = LogDataSet()
        self.options = None
        self.option_parser = OptionParser(
                usage = ("Usage: %prog [options]"),
                version = "%prog" + str(__version__))
        self.input_options = OptionGroup(self.option_parser, _("Input options"))
        self.parse_options = OptionGroup(self.option_parser, _("Parse options"))
        self.morph_options = OptionGroup(self.option_parser, _("Morph options"))
        self.output_options = OptionGroup(self.option_parser, \
                _("Output options"))
    
    # run_parse does the actual job using the other functions.
    def run_parse():
        """Parse one or more log files"""
        pass

    def config_options(self):
        """Set config options"""
        # Input option:
        self.option_parser.add_option("-i", "--input",
                action="store",
                dest="inputs_list"
                help=_("specifies input files"))
        # Module list options:
        self.option_parser.add_option("--list-parsers",
                action="callback",
                callback=self.list_parsers,
                help=_("returns a list of available parsers"))
        self.option_parser.add_option("--list-morphers",
                action="callback",
                callback=self.list_morphers,
                help=_("returns a list of available morphers"))
        self.option_parser.add_option("--list-outputs",
                action="callback",
                callback=self.list_outputs,
                help=_("returns a list of available output formats"))
        # Module load options:
        self.option_parser.add_option("-p", "--parsers",
                action="store",
                dest="parsers_list", default="syslog"
                help=_("specifies parsers to use"))
        self.option_parser.add_option("-m", "--morphers",
                action="store",
                dest="morphers_list",
                help=_("specifies morphers to use"))
        self.option_parser.add_option("-o", "--outputs",
                action="store",
                dest="output_list"
                help=_("specifies output formats to use"))
        
        self.option_parser.add_option_group(self.input_options)
        self.option_parser.add_option_group(self.parse_options)
        self.option_parser.add_option_group(self.morph_options)
        self.option_parser.add_option_group(self.output_options)
        self.options, args = self.option_parser.parse_args(sys.argv[1:])

    # Parsing modules:
    def list_parsers(self):
        """Return a list of available parsing modules"""
        print '==== Available parsing modules: ===='
        print
        for parser in sorted(self.parse_modules):
            print string.ljust(self.parse_modules[parser].name, 16) + \
                ': ' + self.parse_modules[parser].desc
        sys.exit 0
    
    def load_parsers(self, parse_modules):
        """Load parsing module(s)"""
        for parser in sorted(LogDissect.parsers.__parsers__):
            self.parse_modules[parser] = \
                __import__('LogDissect.parsers.' + parser, globals(), \
                locals(), [LogDissect]).ParseModule(self.parse_options)

    # Morphing modules (range, grep, etc)
    def list_morphers(self):
        """Return a list of available morphing modules"""
        print '==== Available morphing modules: ===='
        print
        for morpher in sorted(self.morph_modules):
            print string.ljust(self.morph_modules[morpher].name, 16) + \
                ': ' + self.morph_module[morpher].desc
        sys.exit 0

    def load_morphers(sels, morph_modules):
        """Load morphing module(s)"""
        for morpher in sorted(LogDissect.morphers.__morphers__):
            self.morph_modules[morpher] = \
                __import__('LogDissect.morphers.' + morpher, globals(), \
                locals(), [LogDissect]).MorphModule(self.morph_options)

    # Output modules (log file, csv, html, etc)
    def list_outputs(self):
        """Return a list of available output modules"""
        print '==== Available output modules ===='
        print
        for output in sorted(self.output_modules):
            print string.ljust(self.output_modules[output].name, 16) + \
                ': ' + self.format_module[format].desc
        sys.exit 0
    
    def load_outputs(self, output_modules):
        """Load output module(s)"""
        for output in sorted(LogDissect.output.__formats__):
            self.output_modules[output] = \
                __import__('LogDissect.output.' + output, globals(), \
                locals(), [LogDissect]).OutputModule(self.output_options)

if __name == "__main__":
    dissect = LogDissectCore()
    dissect.run_parse()

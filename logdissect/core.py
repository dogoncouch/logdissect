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

import os
import sys
import string
import logdissect.data
import logdissect.parsers
import logdissect.morphers
import logdissect.output
from logdissect.data.data import LogEntry
from logdissect.data.data import LogData
from logdissect.data.data import LogDataSet
from logdissect import __version__
from optparse import OptionParser
from optparse import OptionGroup
import gettext
gettext.install('licins')

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
        # self.input_options = OptionGroup(self.option_parser, \
        #         _("Input options"))
        self.parse_options = OptionGroup(self.option_parser, \
                _("Parse options"))
        self.morph_options = OptionGroup(self.option_parser, \
                _("Morph options"))
        self.output_options = OptionGroup(self.option_parser, \
                _("Output options"))
    
    # run_job does the actual job using the other functions.
    def run_job(self):
        """Execute a logdissect job"""
        self.load_parsers()
        self.load_morphers()
        self.load_outputs()
        self.config_options()
        self.load_inputs()
        self.run_parse()
        self.run_merge()
        self.run_morph()
        self.run_output()

    def run_parse(self):
        """Parse one or more log files"""
        # Data set already has source file names from load_inputs
        parsedset = LogDataSet()
        for l in self.data_set.data_set:
            parsemodule = self.parse_modules[self.options.parser]
            parsemodule.data = l
            parsemodule.parse_log()
            parsedset.data_set.append(parsemodule.newdata)
        self.data_set = parsedset

    def run_merge(self):
        """Merge all of our data sets together"""
        #Note: just add the logs together then sort the final list.
        ourlog = LogData()
        for l in self.data_set.data_set:
            ourlog.entries = ourlog.entries + l.entries
        ourlog.entries.sort(key=lambda x: x.date_stamp_year)
        self.data_set.finalized_data = ourlog

    def run_morph(self):
        ourlog = self.data_set.finalized_data
        for m in self.morph_modules:
            if not self.options.morphers_list == None:
                if m in self.options.morphers_list:
                    ourmorph = self.morph_modules[m]
                    ourmorph.data = ourlog
                    ourmorph.morph_data(self.options)
                    ourlog = ourmorph.newdata
        self.data_set.finalized_data = ourlog

    def run_output(self):
        """Output finalized data"""
        for f in logdissect.output.__formats__:
            if self.options.output_type == f:
                ouroutput = self.output_modules[f]
                ouroutput.data = self.data_set.finalized_data
                ouroutput.write_output(str(self.options.output_file))

    def config_options(self):
        """Set config options"""
        # Input option:
        self.option_parser.add_option("-i", "--input",
                action="store",
                dest="inputs_list",
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
        self.option_parser.add_option("-p", "--parser",
                action="store",
                dest="parser", default="syslog",
                help=_("specifies parser to use"))
        self.option_parser.add_option("-m", "--morphers",
                action="store",
                dest="morphers_list",
                help=_("specifies morphers to use"))
        self.option_parser.add_option("-o", "--output",
                action="store",
                dest="output_type",
                help=_("specifies output formats to use"))
        self.option_parser.add_option("-f", "--file",
                action="store",
                dest="output_file", default="logdissectjob",
                help=_("specifies output formats to use"))
        
        # self.option_parser.add_option_group(self.input_options)
        # self.option_parser.add_option_group(self.parse_options)
        self.option_parser.add_option_group(self.morph_options)
        # self.option_parser.add_option_group(self.output_options)
        self.options, args = self.option_parser.parse_args(sys.argv[1:])

    # Load input files:
    def load_inputs(self):
        """Load the specified inputs"""
        for f in self.options.inputs_list.split(','):
            fullpath = os.path.abspath(f)
            log = LogData()
            log.source_full_path = fullpath
            self.data_set.data_set.append(log)

    # Parsing modules:
    def list_parsers(self, *args):
        """Return a list of available parsing modules"""
        print '==== Available parsing modules: ===='
        print
        for parser in sorted(self.parse_modules):
            print string.ljust(self.parse_modules[parser].name, 16) + \
                ': ' + self.parse_modules[parser].desc
        sys.exit(0)
    
    def load_parsers(self):
        """Load parsing module(s)"""
        for parser in sorted(logdissect.parsers.__all__):
            self.parse_modules[parser] = \
                __import__('logdissect.parsers.' + parser, globals(), \
                locals(), [logdissect]).ParseModule(self.parse_options)

    # Morphing modules (range, grep, etc)
    def list_morphers(self, *args):
        """Return a list of available morphing modules"""
        print '==== Available morphing modules: ===='
        print
        for morpher in sorted(self.morph_modules):
            print string.ljust(self.morph_modules[morpher].name, 16) + \
                ': ' + self.morph_modules[morpher].desc
        sys.exit(0)

    def load_morphers(self):
        """Load morphing module(s)"""
        for morpher in sorted(logdissect.morphers.__morphers__):
            self.morph_modules[morpher] = \
                __import__('logdissect.morphers.' + morpher, globals(), \
                locals(), [logdissect]).MorphModule(self.morph_options)

    # Output modules (log file, csv, html, etc)
    def list_outputs(self, *args):
        """Return a list of available output modules"""
        print '==== Available output modules ===='
        print
        for output in sorted(self.output_modules):
            print string.ljust(self.output_modules[output].name, 16) + \
                ': ' + self.output_modules[output].desc
        sys.exit(0)
    
    def load_outputs(self):
        """Load output module(s)"""
        for output in sorted(logdissect.output.__formats__):
            self.output_modules[output] = \
                __import__('logdissect.output.' + output, globals(), \
                locals(), [logdissect]).OutputModule(self.output_options)

if __name__ == "__main__":
    dissect = LogDissectCore()
    dissect.run_job()

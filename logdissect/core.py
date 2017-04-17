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
from argparse import ArgumentParser
# from optparse import OptionParser
# from optparse import OptionGroup
import gettext
gettext.install('logdissect')

# To Do: enable delete statements

class LogDissectCore:

    def __init__(self):
        """Initialize logdissect job"""
        self.input_files = []
        self.parse_modules = {}
        self.morph_modules = {}
        self.output_modules = {}
        self.data_set = LogDataSet()
        self.options = None
        self.option_parser = ArgumentParser()
        # self.option_parser = ArgumentParser(
        #         usage = ("Usage: %prog [options] <files>"),
        #         version = "%prog" + '-' + str(__version__))
        # self.option_parser = OptionParser(
        #         usage = ("Usage: %prog [options] <files>"),
        #         version = "%prog" + '-' + str(__version__))
        # self.input_options = OptionGroup(self.option_parser, \
        #         _("Input options"))
        self.parse_options = \
                self.option_parser.add_argument_group('Parse options')
        self.morph_options = \
                self.option_parser.add_argument_group('Morph options')
        self.output_options = \
                self.option_parser.add_argument_group('Output options')
        # self.parse_options = OptionGroup(self.option_parser, \
        #         _("Parse options"))
        # self.morph_options = OptionGroup(self.option_parser, \
        #         _("Morph options"))
        # self.output_options = OptionGroup(self.option_parser, \
        #         _("Output options"))
    
    
        
    # run_job does the actual job using the other functions.
    def run_job(self):
        """Execute a logdissect job"""
        try:
            # self.config_options()
            # if self.options.verbosemode: print('Loading parsers')
            self.load_parsers()
            # if self.options.verbosemode: print('Loading morphers')
            self.load_morphers()
            # if self.options.verbosemode: print('Loading outputs')
            self.load_outputs()
            # if self.options.verbosemode: print('Setting options')
            self.config_options()
            # List options, if asked:
            if self.options.list_parsers:
                self.list_parsers()
            if self.options.list_morphers:
                self.list_morphers()
            if self.options.list_outputs:
                self.list_outputs()
            if self.options.verbosemode: print('Loading input files')
            self.load_inputs()
            if self.options.verbosemode: print('Running parsers')
            self.run_parse()
            if self.options.verbosemode: print('Merging data')
            self.run_merge()
            if self.options.verbosemode: print('Running morphers')
            self.run_morph()
            if self.options.verbosemode: print('Running output')
            self.run_output()
        except KeyboardInterrupt:
            sys.exit(1)

    def run_parse(self):
        """Parse one or more log files"""
        # Data set already has source file names from load_inputs
        parsedset = LogDataSet()
        for l in self.data_set.data_set:
            parsemodule = self.parse_modules[self.options.parser]
            parsedset.data_set.append(parsemodule.parse_log(l))
        self.data_set = parsedset
        del(parsedset)

    def run_merge(self):
        """Merge all of our data sets together"""
        ourlog = LogData()
        for l in self.data_set.data_set:
            ourlog.entries = ourlog.entries + l.entries
        ourlog.entries.sort(key=lambda x: x.date_stamp)
        self.data_set.finalized_data = ourlog
        del(ourlog)

    def run_morph(self):
        for m in self.morph_modules:
            ourmorph = self.morph_modules[m]
            ourlog = ourmorph.morph_data(self.data_set.finalized_data,
                    self.options)
            self.data_set.finalized_data = ourlog
            del(ourlog)
            del(ourmorph)

    def run_output(self):
        """Output finalized data"""
        for f in logdissect.output.__formats__:
            ouroutput = self.output_modules[f]
            ouroutput.write_output(self.data_set.finalized_data,
                    self.options)
            del(ouroutput)

        # Output to terminal if silent mode is not set:
        if not self.options.silentmode:
            if self.options.verbosemode:
                print('\n==== ++++ ==== Output: ==== ++++ ====\n')
            for line in self.data_set.finalized_data.entries:
                print(line.raw_text)



    def config_options(self):
        """Set config options"""
        # Module list options:
        self.option_parser.add_argument('--version', action='version',
                version='%(prog)s ' + str(__version__))
        self.option_parser.add_argument('--list-parsers',
                action='store_true', dest='list_parsers',
                help=_('returns a list of available parsers'))
        self.option_parser.add_argument('--list-morphers',
                action='store_true', dest='list_morphers',
                help=_('returns a list of available morphers'))
        self.option_parser.add_argument('--list-outputs',
                action='store_true', dest='list_outputs',
                help=_('returns a list of available output formats'))
        self.option_parser.add_argument('-p',
                action='store', dest='parser', default='syslog',
                help=_('specifies parser to use (default: syslog)'))
        self.option_parser.add_argument('-s',
                action='store_true', dest = 'silentmode',
                help=_('silences terminal output'))
        self.option_parser.add_argument('--verbose',
                action='store_true', dest = 'verbosemode',
                help=_('sets verbose terminal output'))
        self.option_parser.add_argument('files',
                metavar='file', nargs='+',
                #default=sys.stdin, # To Do
                help=_('Specifies input files'))
        # self.option_parser.add_argument_group(self.input_options)
        # self.option_parser.add_argument_group(self.parse_options)
        self.option_parser.add_argument_group(self.morph_options)
        self.option_parser.add_argument_group(self.output_options)
        self.options = self.option_parser.parse_args()
        # self.args = self.options.accumulate(self.options.ourfiles)
        # self.options, self.args = self.option_parser.parse_args()
        # self.options, self.args = self.option_parser.parse_args(sys.argv[1:])

    
    
    # Load input files:
    def load_inputs(self):
        """Load the specified inputs"""
        # for f in self.args:
        for f in self.options.files:
            if os.path.isfile(str(f)):
                fparts = str(f).split('.')
                if fparts[-1] == 'gz' or fparts[-1] == 'bz2' or \
                        fparts[-1] == 'zip':
                    return 0
                else:
                    fullpath = os.path.abspath(str(f))
                    log = LogData()
                    log.source_path = fullpath
                    self.data_set.data_set.append(log)
            else: return 1

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


                
def main():
    dissect = LogDissectCore()
    dissect.run_job()
                
if __name__ == "__main__":
    dissect = LogDissectCore()
    dissect.run_job()

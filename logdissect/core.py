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
import logdissect.parsers
import logdissect.morphers
import logdissect.output
from logdissect.data import LogEntry
from logdissect.data import LogData
from logdissect.data import LogDataSet
from logdissect import __version__
from argparse import ArgumentParser
import gettext
gettext.install('logdissect')


class LogDissectCore:

    def __init__(self):
        """Initialize logdissect job"""
        self.input_files = []
        self.parse_modules = {}
        self.morph_modules = {}
        self.output_modules = {}
        self.data_set = LogDataSet()
        self.args = None
        self.arg_parser = ArgumentParser()
        self.parse_args = \
                self.arg_parser.add_argument_group('parse options')
        self.morph_args = \
                self.arg_parser.add_argument_group('morph options')
        self.output_args = \
                self.arg_parser.add_argument_group('output options')
    
    
        
    # run_job does the actual job using the other functions.
    def run_job(self):
        """Execute a logdissect job"""
        try:
            self.load_parsers()
            self.load_morphers()
            self.load_outputs()
            self.config_options()
            if self.args.list_parsers:
                self.list_parsers()
            if self.args.verbosemode: print('Loading input files')
            self.load_inputs()
            if self.args.verbosemode: print('Running parsers')
            self.run_parse()
            if self.args.verbosemode: print('Merging data')
            self.data_set.merge_logs()
            if self.args.verbosemode: print('Running morphers')
            self.run_morph()
            if self.args.verbosemode: print('Running output')
            self.run_output()
        except KeyboardInterrupt:
            sys.exit(1)

    def run_parse(self):
        """Parse one or more log files"""
        # Data set already has source file names from load_inputs
        parsedset = LogDataSet()
        for log in self.input_files:
            parsemodule = self.parse_modules[self.args.parser]
            try:
                if self.args.tzone:
                    parsemodule.tzone = self.args.tzone
            except NameError: pass
            parsedset.data_set.append(parsemodule.parse_file(log))
        self.data_set = parsedset
        del(parsedset)

    def run_morph(self):
        for m in self.morph_modules:
            ourmorph = self.morph_modules[m]
            ourlog = ourmorph.morph_data(self.data_set.finalized_data,
                    args=self.args)
            self.data_set.finalized_data = ourlog
            del(ourlog)
            del(ourmorph)

    def run_output(self):
        """Output finalized data"""
        for f in logdissect.output.__formats__:
            ouroutput = self.output_modules[f]
            ouroutput.write_output(self.data_set.finalized_data,
                    args=self.args)
            del(ouroutput)

        # Output to terminal if silent mode is not set:
        if not self.args.silentmode:
            if self.args.verbosemode:
                print('\n==== ++++ ==== Output: ==== ++++ ====\n')
            for line in self.data_set.finalized_data.entries:
                print(line.raw_text)



    def config_options(self):
        """Set config options"""
        # Module list options:
        self.arg_parser.add_argument('--version', action='version',
                version='%(prog)s ' + str(__version__))
        self.arg_parser.add_argument('--verbose',
                action='store_true', dest = 'verbosemode',
                help=_('set verbose terminal output'))
        self.arg_parser.add_argument('-s',
                action='store_true', dest = 'silentmode',
                help=_('silence terminal output'))
        self.arg_parser.add_argument('--list-parsers',
                action='store_true', dest='list_parsers',
                help=_('return a list of available parsers'))
        self.arg_parser.add_argument('-p',
                action='store', dest='parser', default='syslogbsd',
                help=_('select a parser (default: syslogbsd)'))
        self.arg_parser.add_argument('-z', '--unzip',
                action='store_true', dest='unzip',
                help=_('include files compressed with gzip'))
        self.arg_parser.add_argument('-t',
                action='store', dest='tzone',
                help=_('specify timezone offset to UTC (e.g. \'+0500\')'))
        self.arg_parser.add_argument('files',
                # nargs needs to be * not + so --list-morphers/etc
                # will work without file arg
                metavar='file', nargs='*',
                help=_('specify input files'))

        # self.arg_parser.add_argument_group(self.parse_args)
        self.arg_parser.add_argument_group(self.morph_args)
        self.arg_parser.add_argument_group(self.output_args)
        self.args = self.arg_parser.parse_args()

    
    
    # Load input files:
    def load_inputs(self):
        """Load the specified inputs"""
        for f in self.args.files:
            if os.path.isfile(f):
                fparts = str(f).split('.')
                if fparts[-1] == 'gz':
                    if args.unzip:
                        fullpath = os.path.abspath(str(f))
                        self.input_files.append(fullpath)
                    else:
                        return 0
                elif fparts[-1] == 'bz2' or fparts[-1] == 'zip':
                    return 0
                else:
                    fullpath = os.path.abspath(str(f))
                    self.input_files.append(fullpath)
            else: return 1

    # Parsing modules:
    def list_parsers(self, *args):
        """Return a list of available parsing modules"""
        print('==== Available parsing modules: ====\n')
        for parser in sorted(self.parse_modules):
            print(string.ljust(self.parse_modules[parser].name, 16) + \
                ': ' + self.parse_modules[parser].desc)
        sys.exit(0)
    
    def load_parsers(self):
        """Load parsing module(s)"""
        for parser in sorted(logdissect.parsers.__all__):
            self.parse_modules[parser] = \
                __import__('logdissect.parsers.' + parser, globals(), \
                locals(), [logdissect]).ParseModule()

    def load_morphers(self):
        """Load morphing module(s)"""
        for morpher in sorted(logdissect.morphers.__morphers__):
            self.morph_modules[morpher] = \
                __import__('logdissect.morphers.' + morpher, globals(), \
                locals(), [logdissect]).MorphModule(args=self.morph_args)

    def load_outputs(self):
        """Load output module(s)"""
        for output in sorted(logdissect.output.__formats__):
            self.output_modules[output] = \
                __import__('logdissect.output.' + output, globals(), \
                locals(), [logdissect]).OutputModule(args=self.output_args)


                
def main():
    dissect = LogDissectCore()
    dissect.run_job()
                
if __name__ == "__main__":
    dissect = LogDissectCore()
    dissect.run_job()

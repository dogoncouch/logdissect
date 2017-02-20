# MIT License
# 
# Copyright (c) 2017 Dan Persons
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
        pass
    
    # run_parse does the actual job using the other functions.
    def run_parse():
        """Parse one or more log files"""

    def config_options(self, options):
        """Set config options"""
        pass

    # Parsing modules:
    def list_parsers(self):
        """Return a list of available parsing modules"""
        pass
    
    def load_parsers(self, parse_modules):
        """Load parsing module(s)"""
        pass

    # Morphing modules (range, grep, etc)
    def list_morphers(self):
        """Return a list of available morphing modules"""
        pass

    def load_morphers(sels, morph_modules):
        """Load morphing module(s)"""
        pass

    # Output modules (log file, csv, html, etc)
    def list_outputs(self):
        """Return a list of available output modules"""
    
    def load_outputs(self, output_modules):
        """Load output module(s)"""

if __name == "__main__":
    dissect = LogDissectCore()
    dissect.run_parse()

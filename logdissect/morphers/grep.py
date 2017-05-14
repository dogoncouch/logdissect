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

import re
from logdissect.morphers.type import MorphModule as OurModule
from logdissect.data import LogEntry
from logdissect.data import LogData

class MorphModule(OurModule):
    def __init__(self, args):
        """Initialize the grep morphing module"""
        self.name = "grep"
        self.desc = "match a pattern"

        args.add_argument('--grep', action='store', dest='pattern',
                help='match a pattern')

    def morph_data(self, data, args):
        """Return entries containing specified pattern (single log)"""
        if not args.pattern:
            return data
        else:
            repattern = re.compile(r".*({}).*".format(args.pattern))

            newdata = LogData()
            newdata.source_path = data.source_path
            newdata.source_file = data.source_file
            newdata.source_file_mtime = data.source_file_mtime
            newdata.parser = data.parser

            for entry in data.entries:
                if re.match(repattern, entry.raw_text):
                    newdata.entries.append(entry)
            return newdata

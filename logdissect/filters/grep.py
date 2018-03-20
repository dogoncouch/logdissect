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
from logdissect.filters.type import FilterModule as OurModule

class FilterModule(OurModule):
    def __init__(self, args):
        """Initialize the grep filter module"""
        self.name = "grep"
        self.desc = "match a pattern"

        args.add_argument('--grep', action='append', dest='pattern',
                help='match a pattern')

    def filer_data(self, data, args):
        """Return entries containing specified patterns (single log)"""
        if not args.pattern:
            return data
        else:
            newdata = data
            newdata['entries'] = []

            repatterns = {}
            for pat in args.pattern:
                repatterns[pat] = re.compile(r".*({}).*".format(pat))

            for entry in data['entries']:
                for repat in repatterns:
                    if re.match(repatterns[repat], entry['raw_text']):
                        newdata['entries'].append(entry)
                        break

            return newdata

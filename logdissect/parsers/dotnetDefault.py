from logdissect.parsers.type import ParseModule as OurModule

class ParseModule(OurModule):
    def __init__(self, options=[]):
        """Initialize the .Net Core parsing module"""
        self.name = 'dotnetDefault'
        self.desc = '.Net Core Build parsing module'
        self.format_regex = \
                '^(?:\s+)?(?:\d+>)?(.*?)(?:\((\d+),(\d+)\))?:\s+(\w+)\s+(\w+\d+):\s+(.*)$'
        self.fields = ["filepath","line_number","column_number","log_type","error_code","description"]

        self.backup_format_regex = None
        self.backup_fields = []
        self.tzone = None
        self.datestamp_type = None
        self.time_ordering = False
        self.numeric_time_ordering = False 

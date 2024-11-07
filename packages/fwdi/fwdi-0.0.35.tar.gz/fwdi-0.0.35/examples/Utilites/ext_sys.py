import sys


class ExtSys():

    def is_debug():
        has_trace = hasattr(sys, 'gettrace') and sys.gettrace() is not None
        has_breakpoint = sys.breakpointhook.__module__ != "sys"
        return has_trace or has_breakpoint

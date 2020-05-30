# BOTLIB - Framework to program bots.
#
#

""" user entry commands (log/todo). """

from lo import Object

def __dir__():
    return ("Log", "Todo")

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


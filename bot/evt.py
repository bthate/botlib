# BOTLIB - the bot library !
#
#

import importlib, inspect, os, pkg_resources, queue

from .prs import Parsed
from .obj import Default, Object

class Event(Parsed):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.result = []
        self.txt = ""

    def reply(self, txt):
        self.result.append(txt)
 
    def show(self):
        from .krn import k
        for txt in self.result:
            k.fleet.say(self.orig, self.channel, txt)


# BOTLIB - the bot library !
#
#

import importlib, inspect, os, pkg_resources, queue

from .krn import k
from .prs import Parsed
from .obj import Default, Object

class Event(Parsed):

    def __init__(self, txt=""):
        super().__init__()
        if type(txt) != str:
            raise ETYPE(str(type(txt)))
        self.type = "event"
        self.result = []
        self.parse(txt)

    def reply(self, txt):
        self.result.append(txt)
 
    def show(self):
        for txt in self.result:
            k.fleet.say(self.orig, self.channel, txt)


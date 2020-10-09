# BOTLIB - framework to program bots
#
#

import ol
import threading

class Event(ol.Object):

    def __init__(self):
        super().__init__()
        self.args = []
        self.cmd = ""
        self.prs = ol.Object()
        self.ready = threading.Event()
        self.rest = ""
        self.result = []
        self.thrs = []
        self.txt = ""

    def direct(self, txt):
        ol.bus.bus.say(self.orig, self.channel, txt)

    def parse(self):
        o = ol.Default()
        ol.prs.parse(o, self.txt)
        ol.update(self.prs, o)
        args = self.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = args
            self.rest = " ".join(args)

    def reply(self, txt):
        if not self.result:
            self.result = []
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            try:
                print(txt)
            except:
               pass

    def wait(self):
        self.ready.wait()
        res = []
        for thr in self.thrs:
            res.append(thr.join())
        return res

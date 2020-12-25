# BOTLIB - rss.py
#
# this file is placed in the public domain

"rich site syndicate"

# imports

import datetime
import os
import random
import re
import time
import urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

from bot.bus import bus
from bot.clk import Repeater
from bot.dbs import all, find, last, lastmatch
from bot.obj import Cfg, Default, O, Object, save, get, update
from bot.ofn import edit
from bot.hdl import debug
from bot.thr import launch
from bot.utl import unescape, useragent

# defines

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
    "%d, %b %Y %H:%M:%S +0000"
]

def init(hdl):
    "start a rss poller and return it"
    f = Fetcher()
    return launch(f.start)

# classes

class Cfg(Cfg):

    "rss configuration"

    def __init__(self):
        super().__init__()
        self.dosave = True

class Feed(Default):

    "a feed item"

class Rss(Object):

    "a rss feed url"

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    "all urls seen"

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    "rss feed poller"

    cfg = Cfg()
    seen = Seen()

    def display(self, o):
        "display a rss feed item"
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = get(o, key, None)
            if not data:
                continue
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            data = data.replace("\n", " ")
            data = strip_html(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        "update a rss feed"
        counter = 0
        objs = []
        if not rssobj.rss:
            return 0
        for o in reversed(list(get_feed(rssobj.rss))):
            if not o:
                continue
            f = Feed()
            update(f, rssobj)
            update(f, O(o))
            u = urllib.parse.urlparse(f.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = f.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
            if self.cfg.dosave:
                save(f)
        if objs:
            save(Fetcher.seen)
        for o in objs:
            txt = self.display(o)
            bus.announce(txt)
        return counter

    def run(self):
        "update all feeds"
        thrs = []
        for fn, o in all("bot.rss.Rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        "start the rss poller"
        last(Fetcher.cfg)
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        "stop the rss poller"
        save(self.seen)

# functions

def get_feed(url):
    "return a feed by it's url"
    if debug:
        return [Object(), Object()]
    try:
        result = get_url(url)
    except (HTTPError, URLError):
        return [Object(), Object()]
    if gotparser:
        result = feedparser.parse(result.data)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [Object(), Object()]

# runtime

fetcher = Fetcher()

# commands

def rem(event):
    "remove a rss feed"
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in find("bot.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        save(o)
    event.reply("ok")

def dpl(event):
    "set keys to display"
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for fn, o in lastmatch("bot.rss.Rss", {"rss": event.args[0]}):
        edit(o, setter)
        save(o)
        event.reply("ok")

def ftc(event):
    "manual run a fetch batch"
    res = []
    thrs = []
    fetchr = Fetcher()
    fetchr.start(False)
    thrs = fetchr.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def rss(event):
    "add a feed"
    if not event.args:
        return
    url = event.args[0]
    res = list(find("bot.rss.Rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    save(o)
    event.reply("ok")


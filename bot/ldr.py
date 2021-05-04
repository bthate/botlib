# This file is in the Public Domain

from obj import Object

import adm
import bus
import clk
import cms
import dbs
import edt
import evt
import fnd
import hdl
import irc
import log
import nms
import obj
import opt
import prs
import rss
import slg
import tdo
import udp
import ver

class Loader(Object):

    table = Object()
    table.adm = adm
    table.bus = bus
    table.clk = clk
    table.cms = cms
    table.dbs = dbs
    table.edt = edt
    table.evt = evt
    table.fnd = fnd
    table.hdl = hdl
    table.irc = irc
    table.log = log
    table.nms = nms
    table.obj = obj
    table.opt = opt
    table.prs = prs
    table.slg = slg
    table.rss = rss
    table.tdo = tdo
    table.udp = udp
    table.ver = ver

README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 bot library you can use to program bots, uses a JSON
in file database with a versioned readonly storage and reconstructs objects
based on type information in the path. BOTLIB can run from systemd to
provide restart after reboot, to provide a 24/7 channel service on IRC.
It can be used to display RSS feeds, act as a UDP to IRC relay and you can 
program your own commands for it. for source see :ref:`here <source>`.

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

BOTLIB can be found on pypi, see http://pypi.org/project/botlib

installation is through pypi::

 > sudo pip3 install botlib

24/7
====

to run BOTLIB 24/7 you need to enable the bot service under systemd (as root)::

 # cp /usr/local/share/bot/bot.service /etc/systemd/system
 # systemctl enable bot
 # systemctl daemon-reload
 # botcmd cfg server=irc.freenode.net channel=\#dunkbots
 # systemctl restart bot

if you don't want botlib to startup at boot, remove the service file::

 # rm /etc/systemd/system/bot.service

CONFIGURE
=========

BOTLIB has it's own CLI, the bot program, you can run it on the shell prompt 
and, as default, it won't do anything:: 

 $ bot
 $ 

use bot <cmd> to run a command directly, e.g. the cmd command shows
a list of commands::

 $ bot cmd
 cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,krn,log,met,mod,rem,rss,thr,ver,upt

configuration is done with the cfg command::

 $ bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 ok

users need to be added before they can give commands, use the met command::

 $ bot met ~botfather@jsonbot/daddy
 ok

RSS
===

BOTLIB provides, with the use of feedparser, the possibility to serve rss
feeds in your channel. Install python3-feedparser if you want to display 
rss feeds in the channel:

 $ sudo apt install python3-feedparser


To add an url use the rss command with an url::

 

 $ bot rss https://github.com/bthate/botd/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ bot fnd rss
 0 https://github.com/bthate/botd/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ bot ftc
 fetched 20

adding rss to mods= will load the rss module and start it's poller::

 $ bot krn mods=rss
 ok

UDP
===

BOTLIB also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
Output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTLIB, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

PROGRAMMING
===========

BOTLIB provides a library you can use to program
objects under python3. It provides a basic BigO Object, that mimics a dict
while using attribute access and provides a save/load to/from json files on
disk. Objects can be searched with a little database module, provides
read-only files to improve persistence and use a type in filename
reconstruction.

Basic usage is this:

 >>> from bot.obj import Object
 >>> o = Object()
 >>> o.set("key", "value")
 >>> o.key
 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. Hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

The bot.obj module provides the basic methods like load and save as a object
function using an obj as the first argument:

 >>> import bot.obj
 >>> bot.obj.wd = "data"
 >>> from bot.obj import Object, save, load
 >>> o = Object()
 >>> o["key"] = "value"
 >>> path = save(o)
 >>> path
 'bot.obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = Object()
 >>> load(oo, path)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

COMMANDS
========

programming your own commands is easy, open mod/hlo.py and add the following
code::

    def hlo(event):
        event.reply("hello %s" % event.origin)

now you can type the "hlo" command, showing hello <user> ::

    $ bot hlo
    hello root@console

CONTACT
=======

have fun coding

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

.. toctree::
    :hidden:
    :glob:

    source
    *

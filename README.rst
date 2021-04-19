README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 bot library you can use to program bots, uses a JSON
in file database with a versioned readonly storage and reconstructs objects
based on type information in the path. BOTLIB can run from systemd to
provide restart after reboot, to provide a 24/7 channel service on IRC.

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

BOTLIB can be found on pypi, see http://pypi.org/project/botlib

installation is through pypi::

 > sudo pip3 install botlib

MODULES
=======

BOTLIB provides the following modules: 

::

    bot.adm		- admin
    bot.bus		- listeners
    bot.clk		- repeater
    bot.clt		- clients
    bot.cmd		- commands
    bot.dbs		- databases
    bot.edt		- edit
    bot.evt		- events
    bot.fnd		- find
    bot.hdl		- handler
    bot.irc		- bot
    bot.itr		- introspection
    bot.ldr		- loader
    bot.log		- logging
    bot.opt		- output
    bot.prs		- parser
    bot.rss		- syndicate
    bot.sel		- select
    bot.tdo		- todo
    bot.thr		- threads
    bot.tms		- times
    bot.trc		- trace
    bot.trm		- terminal
    bot.udp		- relay
    bot.url		- locators
    bot.usr		- users
    bot.utl		- utilities
    bot.zzz		- closure

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

    $ botc hlo
    hello root@console

CONTACT
=======

"have fun"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

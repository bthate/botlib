README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 bot library you can use to program bots.
BOTLIB uses a JSON in file database with a versioned readonly storage and
reconstructs objects based on type information in the path.

BOTLIB can be found on pypi, see http://pypi.org/project/botlib

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

installation is through pypi::

 > sudo pip3 install botlib

PROGRAMMING
===========

BOTLIB provides a "move all methods to functions" like this:

::

 obj.method(*args) -> method(obj, *args) 

 e.g.

 not:

 >>> from bot import Object
 >>> o = Object()
 >>> o.set("key", "value")
 >>> o.key
 'value'

 but:

 >>> from bot import Object, set
 >>> o = Object()
 >>> set(o, "key", "value")
 >>> o.key
 'value'

The bot module has the most basic object functions like get, set, update, load,
save etc.

A dict without methods in it is the reason to factor out methods from the base
object, it is inheritable without adding methods in inherited classes. It also
makes reading json from disk into a object easier because you don’t have any
overloading taking place. Hidden methods are still available so it is not a 
complete method less object, it is a pure object what __dict__ is concerned 
(user defined data/methods):

::

 >>> from bot import Object
 >>> o = Object()
 >>> o.__dict__
 {}

COMMANDS
========

Programming your own commands is easy, open /mod/hlo.py and add the following
code::

    def hlo(event):
        event.reply("hello %s" % event.origin)

Now you can type the "hlo" command, showing hello <user> ::

    $ botc hlo
    hello root@console

MODULES
=======

BOTLIB provides the following modules:

.. autosummary::
    :toctree: 
    :template: module.rst

    bot 		- pure python3 bot library
    bot.bus		- list of bots
    bot.clk		- clock/repeater
    bot.cmd.adm		- admin
    bot.cmd.cfg		- configuration
    bot.cmd.cmd		- list of commands
    bot.cmd.fnd		- find
    bot.csl		- console
    bot.dbs		- databases
    bot.evt		- events
    bot.hdl		- handler
    bot.irc		- internet relay chat
    bot.itr		- introspection
    bot.prs		- parser
    bot.tbl		- tables
    bot.thr		- threads
    bot.usr		- users
    bot.utl		- utilities
    bot.ver		- version

CONTACT
=======

"hf"

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

.. toctree::
    :hidden:
    :glob:

    *

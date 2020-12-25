README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 bot library you can use to program bots.
BOTLIB uses a JSON in file database with a versioned readonly storage. It 
reconstructs objects based on type information in the path and is a "dump 
OOP and use OP" programming library where the methods are factored out into
functions that use the object as the first argument. This to obtain a clean
namespace object, which has no methods to clutter the namespace. A "clean",
still has hidden methods, loadable from JSON object, that provides load/save
methods to other classes derived from Object.

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

OBJECT PROGRAMMING
==================

BOTLIB provides a "move all methods to functions" like this:

::

 obj.method(*args) -> method(obj, *args) 

 e.g.

 not:

 >>> from bot.obj import Object
 >>> o = Object()
 >>> o.set("key", "value")
 >>> o.key
 'value'

 but:

 >>> from bot.obj import Object, set
 >>> o = Object()
 >>> set(o, "key", "value")
 >>> o.key
 'value'

it's a way of programming with objects, replacing OOP. Not object-oriented 
programming, but object programming. If you are used to functional programming
you'll like it (or not) ;]

MODULES
=======

BOTLIB provides the following modules:

.. autosummary::
    :toctree: 
    :template: module.rst

    bot.clk          - clock/repeater
    bot.cmd          - commands
    bot.dbs          - databases
    bot.hdl          - handler
    bot.irc          - internet relay chat
    bot.obj          - objects
    bot.prs          - parser
    bot.rss          - rich site syndicate
    bot.thr          - threads
    bot.trm          - terminal
    bot.udp          - udp to irc relay

INSTALL
=======

installation is through pypi::

 > sudo pip3 install botlib

CONTACT
=======

"contributed back to society."

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

.. toctree::
    :hidden:
    :glob:

    *

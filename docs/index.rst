.. title:: Framework to program bots


.. image:: jpg/mirror2.jpg
    :width: 100%
    :height: 3cm

README
######


BOTLIB is a python3 framework to use if you want to program IRC or XMPP bots.

provides
========

| CLI, IRC and XMPP bots.

| Object class	 	- save/load to/from a JSON file.
| ReST server 		- serve saved object’s over HTTP.
| RSS fetcher 		- echo rss feeds to IRC channels.
| UDP server 		- udp to bot to IRC channel.
| Watcher server 	- run tail -f and have output send to IRC channel.
| Email scanning 	- scan mbox format to searchable BOTLIB objects.
| JSON backend 		- objects are stored as json string in files on the fs.
| Db 			- iteration over stored objects.
| Timestamp		- time based filenames gives logging capabilities
| Future		- future sensors should provide entry to the logger.

setup
=====

| Set export PYTHONPATH=”.” if the bot cannot be found by the python interpreter.
| Set export PYTHONIOENCODING=”utf-8” if your shell has problems with handling utf-8 strings.
| For the XMPP server use a ~/.sleekpass file with the password in it

source
======

.. autosummary::
    :toctree: botlib
    :template: module.rst

    botlib.bot
    botlib.cli
    botlib.clock
    botlib.cmnds
    botlib.compose
    botlib.engine
    botlib.db
    botlib.error
    botlib.event
    botlib.fleet
    botlib.handler
    botlib.irc
    botlib.kernel
    botlib.launcher
    botlib.log
    botlib.object
    botlib.raw
    botlib.rss
    botlib.selector
    botlib.task
    botlib.trace
    botlib.users
    botlib.xmpp
    botlib.register
    botlib.rest
    botlib.runner
    botlib.space
    botlib.static
    botlib.template
    botlib.test
    botlib.udp
    botlib.utils
    botlib.url
    botlib.watcher

contact
=======

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com

.. raw:: html

    <br>

BOTLIB is released in the :ref:`Public Domain <license>` - https://bitbucket.org/bthate/botlib

.. toctree::
    :hidden:
    :glob:

    LICENSE

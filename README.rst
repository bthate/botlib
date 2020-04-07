R E A D M E
###########


BOTLIB is a library you can use to program bots. no copyright. no LICENSE.

as of version 76 the binaries in the tarball are no longer distributed with the egg.
this makes this package a pure library package e.g. no binaries. program your own clientcode with it, see http://pypi.org/project/genoclaim


I N S T A L L


download the tarball from pypi, https://pypi.org/project/botlib/#files

extract the tarball, cd into the directory and run the following:

::

 > sudo python3 setup.py install


you can also download with pip3 and install globally.

::

 > sudo pip3 install botlib --upgrade --force-reinstall


U S A G E


BOTLIB is a pure python3 library and does not install binaries. 


C O D I N G


if you want to develop on the library clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botd/botlib

if you want to add your own modules to the bot, you can put you .py files in a "mods" directory and use the -m option to point to that directory.

BOTLIB contains the following modules:

::

    bot.dft		- default
    bot.flt		- fleet
    bot.irc		- irc bot
    bot.krn		- core handler
    bot.rss		- rss to channel
    bot.shw		- show runtime
    bot.udp		- udp to channel
    bot.usr		- users

BOTLIB uses the LIBOBJ library which gets included in the tarball.

::

    lo.clk		- clock
    lo.csl		- console 
    lo.hdl		- handler
    lo.shl		- shell
    lo.thr		- threads
    lo.tms		- times
    lo.typ		- types

basic code is a function that gets an event as a argument:

::

 def command(event):
     << your code here >>

to give feedback to the user use the event.reply(txt) method:

::

 def command(event):
     event.reply("yooo %s" % event.origin)


have fun coding ;]


you can contact me on IRC/freenode/#dunkbots.

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

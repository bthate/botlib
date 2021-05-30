.. _programmer:

PROGRAMMER
##########

Welcome to BOTLIB,

BOTLIB is a pure python3 bot library you can use to program bots, uses a JSON
in file database with a versioned readonly storage and reconstructs objects
based on type information in the path. It can be used to display RSS feeds,
act as a UDP to IRC relay and you can program your own commands for it. 

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

BOTLIB can be found on pypi, see http://pypi.org/project/botlib

installation is through pip::

 > sudo pip3 install botlib --upgrade --force-reinstall

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE. 

MODULES
=======

BOTLIB provides the following modules::

    all            - all modules
    bus            - list of bots
    cfg            - configuration
    clk            - clock/repeater
    clt            - client
    cmd            - command
    cms            - commands
    dbs            - database
    dft            - default
    evt            - event
    hdl            - handler
    irc            - internet relay chat
    krn            - kernel
    lst            - dict of lists
    obj            - objects
    opt            - output
    prs            - parsing
    thr            - threads
    adm            - administrator
    fnd            - find
    log            - log items
    rss            - rich site syndicate
    slg            - slogan
    tdo            - todo items
    udp            - UDP to IRC relay

COMMANDS
========

BOTLIB, on purpose, doesn't read modules from a directory, instead you must
include your own written commands with a updated version fo the code.

Use the repository at github to get the latest repo and install setuptools::

 $ git clone http://github.com/bthate/botlib
 $ cd botlib
 $ sudo apt install python3-setuptools
 
to program your own commands, open bot/hlo.py and add the following code::

    def register(k):
        k.regcmd(hlo)

    def hlo(event):
        event.reply("hello %s" % event.origin)

add the command in the bot/all.py module::

    import bot.hlo

    Kernel.addmod(bot.hlo)

edit the list of modules to load in bin/bot:::

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,hlo"

now you can type the "hlo" command, showing hello <user>::

 $ ./bin/bot hlo
 hello root@console

PROGRAMMING
===========

BOTLIB provides a library you can use to program objects under python3. It 
provides a basic BigO Object, that mimics a dict while using attribute access
and provides a save/load to/from json files on disk. Objects can be searched
with a little database module, it uses read-only files to improve persistence
and a type in filename for reconstruction.

Basic usage is this:

 >>> from bot.obj import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. Hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

The bot.obj module has the basic methods like load and save as a object
function using an obj as the first argument:

 >>> import bot.obj
 >>> bot.obj.wd = "data"
 >>> o = bot.obj.Object()
 >>> o["key"] = "value"
 >>> p = o.save()
 >>> p
 'bot.obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = bot.obj.Object()
 >>> oo.load(p)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

UDP
===

BOTD also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTD, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

CONTACT
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

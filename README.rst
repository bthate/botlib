README
######

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

CONFIGURE
=========

BOTLIB is a library and doesn't include binaries in its install. It does
have examples in the tar ball such as the bot program, you can run it on the
shell prompt and, as default, it won't do anything:: 

 $ bot
 $ 

use bot <cmd> to run a command directly, e.g. the cmd command shows
a list of commands::

 $ botc cmd
 cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,krn,log,met,mre,rem,rse,rss,slg,tdo,thr,upt,ver

configuration is done with the cfg command::

 $ bot cfg server=botd.openbsd.amsterdam 
 ok

when user is enabled in the irc config users need to be added before they can
give commands, use the met command::

 $ bot met ~bart@botd.openbsd.amsterdam
 ok

use the -c option to start a shell::

 $ bot -c
 > cmd
 cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,krn,log,met,mre,rem,rse,rss,slg,tdo,thr,upt,ver

and use  the mods= setter to start modules::

 $ bot mods=irc
 > thr
 Console.handler(1s) Console.input(1s) IRC.handler(1s) IRC.input(1s) IRC.keep(1s) IRC.output(1s) IRC.start(1s)

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


RSS
===

BOTLIB provides, with the use of feedparser, the possibility to serve rss
feeds in your channel::

 $ sudo apt install python3-feedparser

to add an url use the rss command with an url::

 $ bot rss https://github.com/bthate/botd/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ bot fnd rss
 0 https://github.com/bthate/botlib/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ bot ftc
 fetched 20

UDP
===

BOTLIB also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTLIB, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

COMMANDS
========

to program your own commands, open bot/hlo.py and add the following code::

    def register(k):
        k.regcmd(hlo)

    def hlo(event):
        event.reply("hello %s" % event.origin)

add the command in the bot/all.py module::

    import bot.hlo

    Kernel.addmod(bot.hlo)

edit the list of modules to load in bin/bot or bin/bots:

    all = "adm,cms,fnd,hlo,irc,krn,log,rss,tdo,udp"

install the bot on the system with install::

 $ sudo python3 setup.py install

now you can type the "hlo" command, showing hello <user>::

 $ bot hlo
 hello root@console

RC.D
====

to run botlib under rc.d::

 # cp files/bots /etc/rc.d/bots
 # groupadd _bots
 # useradd -b /var/lib -d bots -g _bots
 # chown -R botd:_botd /var/lib/botd
 # rcctl enable bots
 # rcctl start bots

CONTACT
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net/botd.openbsd.amsterdam

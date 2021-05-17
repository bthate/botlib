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

CONFIGURE
=========

BOTLIB is a library and doesn't include binaries in tis install. It does
have examples in the tar ball such as the bot program, you can run it on the
shell prompt and, as default, it won't do anything:: 

 $ ./bin/bot
 $ 

use bot <cmd> to run a command directly, e.g. the cmd command shows
a list of commands::

 $ ./bin/bot cmd
 cfg,cmd,dlt,fnd,met,mre,ver

configuration is done with the cfg command::

 $ ./bin/bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 ok

users need to be added before they can give commands, use the met command::

 $ ./bin/bot met ~botfather@jsonbot/daddy
 ok

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

MODULES
=======

BOTLIB provides the following modules:

 all		- all modules
 cms		- commands
 fnd		- find
 hdl		- handler
 irc		- bot
 krn		- tables
 obj		- object

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

install the bot on the system with install::

 $ sudo python3 setup.py install

now you can type the "hlo" command, showing hello <user>::

 $ bot hlo
 hello root@console

24/7
====

to run BOTLIB 24/7 you need to enable the botd service under systemd, edit 
/etc/systemd/system/botd.service and add the following txt::

 [Unit]
 Description=BOTD - 24/7 channel daemon
 After=multi-user.target

 [Service]
 DynamicUser=True
 StateDirectory=botd
 LogsDirectory=botd
 CacheDirectory=botd
 ExecStart=/usr/local/bin/botd
 CapabilityBoundingSet=CAP_NET_RAW

 [Install]
 WantedBy=multi-user.target

copy the botd and botctl binaries to /usr/local/bin/::

 $ sudo cp bin/botd bin/botctl /usr/local/bin/

then enable the bot with::

 $ sudo systemctl enable botd
 $ sudo systemctl daemon-reload
 $ sudo systemctl restart botd

disable botd to start at boot with removing the service file::

 $ sudo rm /etc/systemd/system/botd.service

CONTACT
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

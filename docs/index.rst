BOTLIB
######

| Welcome to BOTLIB, framework to program bots ! see https://pypi.org/project/botlib/ 

BOTLIB is placed in the public domain and contains no copyright or LICENSE, this makes BOTLIB truely
free (pastable) code you can use how you see fit.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install botlib

if you have previous versions already installed and things fail try to force reinstall:

::

 > sudo pip3 install botlib --upgrade --force-reinstall

USAGE
=====

BOTLIB has it's own CLI, you can run it by giving the bcmd command on the
prompt, it will return with no response:

:: 

 $ bcmd
 $ 

you can use bcmd <cmd> to run a command directly, use the !cmd command to
see a list of commands:

::

 $ bcmd cmd
 cmd|dne|edt|fnd|flt|krn|log|add|tsk|tdo|udp|upt|ver


BOTLIB also has it's own shell, bsh:

::

  $ bsh
  > cmd
  cmd|dne|edt|fnd|flt|krn|log|add|tsk|tdo|udp|upt|ver

IRC
===

BOTLIB provides the bot as IRC client, configuration is done with the cfg command:

::

 $ bcmd cfg
 channel=#botlib nick=birc port=6667 realname=botlib server=localhost username=botlib

you can use setters to edit fields in a configuration:

::

 $ bcmd cfg server=irc.freenode.net channel=\#botlib nick=birc
 channel=#botib nick=birc port=6667 realname=botlib server=irc.freenode.net username=botlib

RSS
===

BOTLIB provides with the use of feedparser the possibility to server rss
feeds in your channel. adding rss to mods= will load the rss modules and
start it's poller.

::

 $ bot mods=rss

to add an url use the rss command with an url:

::

 $ bcmd rss https://github.com/bthate/objr/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ bcmd fnd rss
 0 https://github.com/bthate/objr/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ bcmd ftc
 fetched 0

UDP
===

BOTLIB also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

use the 'budp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | budp

to send the tail output to the IRC channel you can use python3 code to send a UDP packet 
to botlib, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to botlib in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

MODULES
=======

BOTLIB use the OLIB library for the new functional object library, it provides
a move all methods to functions and to 

::

 method(obj, *args) instead of obj.method(*args)

way of programming with objects. If you are use to functional programming you'll like it (or not) ;]

OLIB has the following modules:

::

    ol	 	- object library
    ol.bus	- announce
    ol.csl	- console
    ol.dbs	- databases
    ol.hdl	- handler
    ol.krn	- kernel
    ol.prs 	- parser
    ol.tms	- times
    ol.trm	- terminal
    ol.tsk	- tasks
    ol.utl	- utilities

BOTLIB uses bmod as the namespace to distribute modules for BOTLIB:

::

    bmod.cfg	= config
    bmod.cmd	- command
    bmod.edt	- edit
    bmod.ent	- enter log and todo items
    bmod.fnd	- find typed objects
    bmod.mbx	- mailbox
    bmod.rss	- rich site syndicate
    bmod.udp	- UDP to IRC gateway

BOTLIB has 1 module, the bot.irc module:

::

    bot.irc

this package adds bot.irc to the bot namespace.

you can add you own modules to the bot and bmod packages, they are namespace packages.

SERVICE
=======

if you want to run the BOTLIB 24/7 you can install botd as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/botd.service file:

::


 [Unit]
 Description=24/7 channel daemon
 After=network-online.target
 Wants=network-online.target

 [Service]
 User=botd
 Group=botd
 ExecStart=/usr/local/bin/botd -n

 [Install]
 WantedBy=multi-user.target

add the botd user to the system:

::

 $ groupadd botd
 $ useradd botd -d /var/lib/botd/
 $ passwd botd
 $ chown -R botd:botd /var/lib/botd/

copy modules over to botd's work directory:

::

 $ cp -Ra bmod/*.py /var/lib/botd/bmod

make sure permissions are set properly:

::

 $ chmod -R 700 /var/lib/botd/bmod/
 $ chmod -R 400 /var/lib/botd/bmod/*.py

add the botd service with:

::

 $ sudo systemctl enable botd
 $ sudo systemctl daemon-reload

configure botd to connect to irc:

::

 $ sudo -u botd bcmd cfg server=irc.freenode.net channel=#botlib nick=botd

then restart the botd service.

::

 $ sudo service botd stop
 $ sudo service botd start

the bot should join your configured channel, if it doesn't look at the
/var/log/syslog for any debug messages. 

if you don't want botd to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/botd.service

CONTACT
=======

contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

.. toctree::
   :hidden:
   :glob:

   *

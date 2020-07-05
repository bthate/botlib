BOTLIB
======

Welcome to BOTLIB, the bot library ! see https://pypi.org/project/botlib/ , it's public domain ;]

BOTLIB can fetch RSS feeds, lets you program your own commands, can work as a UDP to IRC
relay, has user management to limit access to prefered users and can run as a service to let
it restart after reboots. BOTLIB is the result of 20 years of programming bots, was there 
in 2000, is here in 2020, has no copyright, no LICENSE and is placed in the Public Domain. 
This makes BOTLIB truely free (pastable) code you can use how you see fit, i hope you enjoy 
using and programming BOTLIB till the point you start programming your own bots yourself.

have fun coding ;]

I N S T A L L
=============

you can download with pip3 and install globally:

::

 > sudo pip3 install botlib

You can also download the tarball and install from that, see https://pypi.org/project/botlib/#files

if you want to run the bot 24/7 you can install BOTLIB as a service for
the systemd daemon. You can do this by running the following:

::

 > sudo cp botd.service /etc/systemd/system/
 > systemctl enable botd
 > systemctl daemon-reload

if you don't want the bot to startup at boot, remove the service file:

::

 > sudo rm /etc/systemd/system/botd.service

C O N F I G
===========

to configure the bot use the cfg (config) command, use sudo for the system daemon
and without sudo if you want to run the bot locally:

::

 > sudo bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 > sudo service botd stop
 > sudo service botd start

U S A G E
=========

BOTLIB detects whether it is run as root or as a user. if it's root it
will use the /var/lib/botd directory and it it's user it will use ~/.bot

BOTLIB has it's own CLI, you can run it by giving the bot command on the
prompt, it will return with no response:

:: 

 > bot
 >

you can use bot cmd with arguments to run a command directly:

::

 > bot cmds
 cfg|cmds|ed|find|fleet|meet|ps|udp

if you run with sudo, you will get additional command like install,hup and remove:

::

 > sudo bot cmds
 cfg|cmds|ed|find|fleet|hup|install|meet|ps|remove|udp


running bot with the mods option "csl" will start a console:

::

 > bot mods=csl
 > cmds
 cfg|cmds|ed|find|fleet|meet|ps|udp
 >

giving the -d option runs bot in the background:

::

 > bot -d
 > ps xa | grep bot
 74452 ?        Sl     0:00 /usr/bin/python3 -u ./bin/bot -d
 >

R S S
=====

botlib doesn't depend on other libraries so for RSS you need to install
feedparser yourself:

::

 > sudo apt install feedparser

start the bot with the -r option to have the rss fetcher started:

::

 > bot mods=rss

to add an url use the rss command with an url:

::

 > bot rss https://news.ycombinator.com/rss
 ok 1

run the rss command to see what urls are registered:

::

 > bot rss
 0 https://news.ycombinator.com/rss

the fetch command can be used to poll the added feeds:

::

 > bot fetch
 fetched 0

U D P
=====

using udp to relay text into a channel, use the -u options to start the UDP
service and use the udp command to send text via the bot  to the channel on 
the irc server:

::

 > tail -f /var/log/syslog | bot udp

to send the tail output to the IRC channel, send a udp packet to the bot:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

S O U R C E
===========

if you want to develop on the bot clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/bthate/botlib

BOTLIB has the following modules:

::

    bot.clk             - clock/repeater
    bot.cmd             - commands
    bot.csl             - console
    bot.dbs             - database
    bot.err		- errors
    bot.flt             - list of bots
    bot.hdl             - handler
    bot.irc             - internet relay chat
    bot.isp             - introspect
    bot.krn             - core handler
    bot.obj             - base classes
    bot.opr             - opers
    bot.prs             - parse
    bot.rss             - rich site syndicate
    bot.run             - runtime
    bot.tbl             - tables
    bot.thr             - threads
    bot.tms             - time
    bot.trc             - trace
    bot.udp             - udp to channel
    bot.usr             - users
    bot.utl             - utilities

You can add you own modules to the bot package, its a namespace package.

C O N T A C T
=============

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

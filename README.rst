B  O  T  L  I  B 
################

Welcome to BOTLIB, the bot library ! see https://pypi.org/project/botlib/ , it's public domain ;]

BOTLIB can lets you program your own commands, can work as a UDP to IRC
relay, has user management to limit access to prefered users and can run as a service to let
it restart after reboots. BOTLIB is the result of 20 years of programming bots, was there 
in 2000, is here in 2020, has no copyright, no LICENSE and is placed in the Public Domain. 
This makes BOTLIB truely free (pastable) code you can use how you see fit, i hope you enjoy 
using and programming BOTLIB till the point you start programming your own bots yourself.

INSTALL
=======

you can download with pip3 and install globally:

::

 > sudo pip3 install botlib --upgrade --force-reinstall

BOTLIB itself does not install a binary as it is a library. The tarball
however includes a bot program that can run as a test bot for BOTLIB.

You can download the tarball from https://pypi.org/project/botlib/#files

USAGE
=====

BOTLIB has it's own CLI, you can run it by giving the bot command on the
prompt, it will return with no response:

:: 

 > bot
 >

you can use bot <cmd> to run a command directly:

::

 > bot cmds
 cfg|cmds|display|done|ed|feed|fetch|find|fleet|kernel|log|meet|ps|rm|rss|todo|udp|up|v

you can use the mods= setter to set the modules to load:

::

 > bot mods=csl,cmd,opr
 > cmds
 cfg|cmds|ed|find|fleet|kernel|ps|up|v

to configure the bot, use the cfg command with appropriate setters.

::

 > bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje

to start a irc server with the cmd and opr modules loaded and a console running:

::

 > bot mods=irc,csl,cmd,opr
 > ps
 0 0s       Console.input
 1 0s       IRC.handler
 2 0s       IRC.input
 3 0s       IRC.output
 4 0s       Kernel.handler
 > 

to run a pure UDP to IRC relay, run the bot with irc,udp modules loaded

::

 > bot mods=irc,udp
 >

use the udp command to send text via the bot to the channel on the irc server:

::

 > tail -f /var/log/syslog | bot udp


to send a udp packet to the bot:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

MODULES
=======

if you want to develop on the bot clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/bthate/botlib

BOTLIB has the following modules:

::

    bot.cfg		- configuration
    bot.clk             - clock/repeater
    bot.cls		- classes
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
    bot.thr             - threads
    bot.tms             - time
    bot.trc             - trace
    bot.udp             - udp to channel
    bot.usr             - users
    bot.utl             - utilities

you can add you own modules to the bot package, its a namespace package.

SERVICE
=======

if you want to run the bot 24/7 you can install BOTLIB as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/botd.service file:

::

 [Unit]
 Description=BOTD - the 24/7 channel daemon
 After=network-online.target
 Wants=network-online.target
 
 [Service]
 ExecStart=/usr/local/bin/bot mods=irc,udp,cmd
 
 [Install]
 WantedBy=multi-user.target

then copy the bin/bot to /usr/local/bin and add the botd service with:

::

 > sudo cp bin/bot /usr/local/bin
 > sudo systemctl enable botd
 > sudo systemctl daemon-reload

to configure the bot use the cfg (config) command, use sudo for the system daemon
and without sudo if you want to run the bot locally:

::

 > sudo bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 > sudo service botd stop
 > sudo service botd start

if you don't want the bot to startup at boot, remove the service file:

::

 > sudo rm /etc/systemd/system/botd.service

BOTLIB detects whether it is run as root or as a user. if it's root it
will use the /var/lib/botd/ directory and if it's a user it will use ~/.bot

CONTACT
=======

contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

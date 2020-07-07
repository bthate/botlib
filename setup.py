# setup.py
#
#

from setuptools import setup

setup(
    name='botlib',
    version='89',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description=""" BOTLIB is a library you can use to program bots. """,
    long_description="""
BOTLIB
======

Welcome to BOTLIB, the bot library ! see https://pypi.org/project/botlib/ , it's public domain ;]

BOTLIB can lets you program your own commands, can work as a UDP to IRC
relay, has user management to limit access to prefered users and can run as a service to let
it restart after reboots. BOTLIB is the result of 20 years of programming bots, was there 
in 2000, is here in 2020, has no copyright, no LICENSE and is placed in the Public Domain. 
This makes BOTLIB truely free (pastable) code you can use how you see fit, i hope you enjoy 
using and programming BOTLIB till the point you start programming your own bots yourself.

as of version 89 I ditched RSS as it depends on feedparser, this should make
this code all own intellectual property, that is completely my creation to put into the public
domain as a whole.

I N S T A L L
=============

you can download with pip3 and install globally:

::

 > sudo pip3 install botlib

You can also download the tarball and install from that, see https://pypi.org/project/botlib/#files

if you want to run the bot 24/7 you can install BOTLIB as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/botd.service file:

::

 [Unit]
 Description=BOTD - the 24/7 channel daemon
 After=network-online.target
 Wants=network-online.target
 
 [Service]
 ExecStart=/usr/local/bin/bot mods=irc,udp
 
 [Install]
 WantedBy=multi-user.target

then add the botd service with:

::

 > systemctl enable botd
 > systemctl daemon-reload

to configure the bot use the cfg (config) command, use sudo for the system daemon
and without sudo if you want to run the bot locally:

::

 > sudo bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 > sudo service botd stop
 > sudo service botd start

if you don't want the bot to startup at boot, remove the service file:

::

 > sudo rm /etc/systemd/system/botd.service

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

 > the bot does nothing if you don't provide commands.

 > bot
 
the cmds commands shows a list of available commands:

 > bot cmds
 cfg|cmds|done|ed|find|fl|krn|log|meet|ps|todo|udp|up|v

you can use the mods= setter to set the modules to load:

::

 > bot mods=csl,cmd
 > cmds
 cfg|cmds|find|fl|krn|up|v

to configure the bot, use the cfg command with appropriate setters.

 > bot cfg server=irc.freenode.net channel=\#dunkbots nick=botje

to start a irc server with the cmd and opr modules loaded and a console
running:

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
    
""",
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=False,
    packages=["bot"],
    namespace_packages=["bot"],
    scripts=["bin/bot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

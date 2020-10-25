README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel. It installs itself as a service so
you can get it restarted on reboot. You can use it to display RSS feeds, act as a
UDP to IRC gateway, program your own commands for it, have it log objects on
disk and search them and scan emails for correspondence analysis. BOTLIB uses
a JSON in file database with a versioned readonly storage. It reconstructs
objects based on type information in the path and uses a "dump OOP and use
OP" programming library where the methods are factored out into functions
that use the object as the first argument. BOTLIB is placed in the Public
Domain and has no COPYRIGHT or LICENSE.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install botlib

if you have previous versions already installed and things fail try to force reinstall:

::

 > sudo pip3 install botlib --upgrade --force-reinstall

if this also doesn't work you'll need to remove all installed previous  versions, so you can do a clean install.

you can run directly from the tarball, see https://pypi.org/project/botlib/#files

USAGE
=====

BOTLIB is a library and doesn't have it's own CLI, however a bot test
program is provided with the tarball. you can run the bot command on the prompt, it will return with no response:

:: 

 $ bot
 $ 

you can use bot <cmd> to run a command directly, use the cmd command to see a list of commands:

::

 $ bot cmd
 cfg,cmd,cor,dne,dpl,fed,fnd,ftc,log,mbx,rem,req,rss,sts,tdo,trt,tsk,upt,ver,wsd

BOTLIB also has it's own shell, use genocide -s to start a genocide shell:

::

  $ sudo genocide -s
  > cmd
  cfg,cmd,cor,dne,dpl,fed,fnd,ftc,log,mbx,rem,req,rss,sts,tdo,trt,tsk,upt,ver,wsd


IRC
===

configuration is done with the cfg command:

::

 $ sudo genocide cfg
 channel=#genocide nick=genocide port=6667 server=localhost

you can use setters to edit fields in a configuration:

::

 $ genocide cfg server=irc.freenode.net channel=\#genocude nick=genocide
 channel=#genocide nick=genocide port=6667 server=irc.freenode.net

to have the irc bot started use the mods=irc option at start:

 $ sudo genocide mods=irc

RSS
===

BOTLIB provides with the use of feedparser the possibility to server rss
feeds in your channel. BOTLIB itself doesn't depend, you need to install
python3-feedparser first:

::

 $ sudo apt install python3-feedparser
 $

adding rss to mods= will load the rss module and start it's poller.

::

 $ sudo genocide mods=irc,rss

to add an url use the rss command with an url:

::

 $ sudo genocide rss https://github.com/bthate/botlib/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ sudo genocide fnd rss
 0 https://github.com/bthate/botlib/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ sudo genocide ftc
 fetched 20

UDP
===

BOTLIB also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

use the 'genocide udp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | genocide udp

output to the IRC channel can be done with the use python3 code to send a UDP packet 
to genocide, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to genocide in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

OBJECT PROGRAMMING
==================

BOTLIB uses the OLIB library as object library, it provides a "move all methods to functions" like this:

::

 obj.method(*args) -> method(obj, *args) 

 e.g.

 not:

 >>> import ol
 >>> o = ol.Object()
 >>> o.set("key", "value")
 >>> o.key
 'value'

 but:

 >>> import ol
 >>> o = ol.Object()
 >>> ol.set(o, "key", "value")
 >>> o.key
 'value'

A way of programming with objects, replacing OOP., it works because the
object library is 2 characters long and using the, now generic, method is
not too much typing.

it's a way of programming with objects, replacing OOP. Not object-oriented programming, but object programming. If you are used to functional programming you'll like it (or not) ;]

OLIB has the following modules:

::

    ol	 	- object library
    ol.bus	- announce
    ol.csl	- console
    ol.dbs	- databases
    ol.evt	- event
    ol.hdl	- handler
    ol.int	- introspection
    ol.krn	- kernel
    ol.prs 	- parser
    ol.spc	- specification
    ol.tms	- times
    ol.trm	- terminal
    ol.tsk	- tasks
    ol.utl	- utilities

MODULES
=======

BOTLIB uses the bot and botmod as the namespace to distribute modules:


::

   bot.cfg	- config
   bot.cmd	- command
   bot.irc	- irc 

::

   botmod.ent	- entry
   botmod.fnd	- find
   botmod.mbx	- mail
   botmod.rss	- rich site syndicate
   botmod.udp	- UDP to IRC


CONTACT
=======

"hope you enjoy my contribution back to society."

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

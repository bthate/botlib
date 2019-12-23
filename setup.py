#!/usr/bin/env python3

""" bl setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run BOTLIB with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='bl',
    version='18',
    url='https://bitbucket.org/bthate/bl',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    license='Public Domain',
    include_package_data=False,
    zip_safe=False,
    install_requires=["sleekxmpp", "feedparser", "dnspython", "pyasn1", "pyasn1_modules"],
    scripts=["bin/bot", "bin/bot-udp"],
    packages=['bl'],
    extra_path="bl",
    long_description='''
README
######

BOTLIB is a python3 framework to use if you want to program IRC or XMPP bots.

provides:

| CLI, IRC and XMPP bots.

| Object class 		- save/load to/from a JSON file.
| ReST server 		- serve saved object’s over HTTP.
| RSS fetcher 		- echo rss feeds to IRC channels.
| UDP server 		- udp to bot to IRC channel.
| Watcher server 	- run tail -f and have output send to IRC channel.
| Email scanning 	- scan mbox format to searchable BOTLIB objects.
| JSON backend 		- objects are stored as json string in files on the fs.
| Db	 		- iteration over stored objects.
| Timestamp		- time based filenames gives logging capabilities
| Future		- future sensors should provide entry to the logger.

setup:

| Set export PYTHONPATH=”.” if the bot cannot be found by the python interpreter.
| Set export PYTHONIOENCODING=”utf-8” if your shell has problems with handling utf-8 strings.
| For the XMPP server use a ~/.sleekpass file with the password in it

source:

| bl		- bl package.
| bl.bot		- bot base class.
| bl.cli 		- command line interfacce bot, gives a shell prompt to issue bot commands.
| bl.clock 		- timer, repeater and other clock based classes.
| bl.cmnds 		- bl basic commands.
| bl.compose 	- construct a object into it’s type.
| bl.engine 	- select.epoll event loop, easily interrup_table esp. versus a blocking event loop.
| bl.db 		- JSON file db.
| bl.error 		- bl exceptions.
| bl.event 		- event handling classes.
| bl.fleet 		- fleet is a list of bots.
| bl.handler 	- schedule events.
| bl.irc 		- IRC bot class.
| bl.kernel 	- program boot and module loading.
| bl.launcher 	- a launcher launches threads (or tasks in this case).
| bl.log 		- log module to set standard format of logging.
| bl.object 	- JSON file backed object with dotted access.
| bl.raw 		- raw output using print.
| bl.rss 		- rss module.
| bl.selector 	- functions used in code to select what objects to use.
| bl.task 		- adapted thread to add extra functionality to threads.
| bl.trace 		- functions concering stack trace.
| bl.users 		- class to access user records.
| bl.xmpp 		- XMPP bot class.
| bl.register 	- object with list for multiple values.
| bl.rest 		- rest interface.
| bl.runner 	- threaded loop to run tasks on.
| bl.space 		- central module to store objects in.
| bl.static 	- static definitions.
| bl.template 	- cfg objects containing default values for various services and plugins.
| bl.test 		- plugin containing test commands and classes.
| bl.udp 		- relay txt through a udp port listener.
| bl.utils 		- lib local helper functions.
| bl.url 		- functions that fetch data from url.
| bl.watcher 	- watch files.

contact:

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com

BOTLIB is code released in the Public Domain - https://bitbucket.org/bthate/bl


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Public Domain',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)

% BOTCMD(8)  BOTCMD(8)
% Bart Thate
% April 2021

# NAME
BOTCMD - control the bot daemon

# SYNOPSIS
sudo botcmd \<cmd\>

# DESCRIPTION
BOTCMD executes a bot command under the systemd-exec wrapper, this to make 
commands run under systemd. it uses /var/lib/bot as the work directory and
/vae/lib/bot/mod as the modules directory.

# EXAMPLES
| sudo botcmd cmd
| sudo botcmd cfg server=irc.freenode.net channel=\#dunkbots nick=botje
| sudo botcmd met ~botfather@jsonbot/daddy
| sudo botcmd rss https://github.com/bthate/botd/commits/master.atom
| sudo botcmd krn mods=rss

# AUTHOR
Bart Thate \<bthate@dds.nl\>

# COPYRIGHT
BOTCMD is placed in the Public Domain. 

# SEE ALSO
| bot
| botsrv
| /var/lib/bot
| /var/lib/bot/mod
| /usr/local/share/botd/bot.service

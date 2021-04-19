% BOTSRV(8) BOTSRV(8)
% Bart Thate
% April 2021

# NAME
BOTSRV - 24/7 channel daemon

# SYNOPSIS
sudo botsrv \<cmd\>

# DESCRIPTION
BOTSRV is a pure python3 IRC chat bot that can run as a background
daemon for 24/7 a day presence in a IRC channel. You can install
it as a service so it restarts on reboot. It can be used to
display RSS feeds, act as a UDP to IRC relay and you can program
your own commands for it. 

# CONFIGURATION
| sudo cp /usr/local/share/bot/bot.service /etc/systemd/system
| sudo systemctl enable bot
| sudo systemctl daemon-reload
| sudo systemctl restart bot

# COPYRIGHT
BOTSRV is placed in the Public Domain.

# AUTHOR
Bart Thate \<bthate@dds.nl\>

# SEE ALSO
| bot
| botcmd
| /var/lib/bot
| /var/lib/bot/mod
| /usr/local/share/bot/bot.service

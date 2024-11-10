# This file is placed in the Public Domain.
# pylint: disable=C


"console"


import os
import sys


from .command import NAME, Commands, Config
from .command import command, parse, scanner, wrap
from .modules import face
from .runtime import Client, Event, errors


cfg  = Config()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        print(txt)


def srv(event):
    import getpass
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))
    

def wrapped():
    wrap(main)
    for line in errors():
        print(line)


scan = scanner


def main():
    Commands.add(srv)
    parse(cfg, " ".join(sys.argv[1:]))
    scan(face)
    evt = Event()
    evt.type = "command"
    evt.txt = cfg.txt
    csl = CLI()
    command(csl, evt)
    evt.wait()


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""


if __name__ == "__main__":
    wrapped()

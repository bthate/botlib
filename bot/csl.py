# This file is placed in the Public Domain.

from hdl import Client

def init():
    c = Console()
    c.start()
    return c

class CLI(Client):

    def handle(self, e):
        super().handle(e)
        e.wait()

    def raw(self, txt):
        print(txt)

class Console(CLI):

    def poll(self):
        return input("> ")

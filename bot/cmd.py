# This file is placed in the Public Domain.

from .evt import Event

class Command(Event):

    def __init__(self):
        super().__init__()
        self.type = "cmd"

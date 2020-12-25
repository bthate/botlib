# BOTLIB - irc.py
#
# this file is placed in the public domain

"Internet Relay Chat"

# imports

from bot.obj import Object, get, save

# exceptions

class ENOUSER(Exception):
    "no matching user found."
    

# classes

class User(Object):

    "IRC user"

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Object):

    "IRC users"

    userhosts = Object()

    def allowed(self, origin, perm):
        "see if origin has needed permission"
        perm = perm.upper()
        origin = get(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        "remove a permission of the user"
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        "get all users, optionaly provding an matching origin"
        s = {"user": origin}
        return find("irc.User", s)

    def get_user(self, origin):
        "get specific user with corresponding origin"
        u = list(self.get_users(origin))
        if u:
            return u[-1][-1]

    def meet(self, origin, perms=None):
        "add a irc user"
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        "grant origin oper permission"
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        "add permission to origin"
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user

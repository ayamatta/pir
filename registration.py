 # -*- coding: utf-8 -*-

import core

def __create_userdict(un, pw):
    return {'_id':un, 'pw':pw}

def _username_is_free(un):
    t=core.getview('users', 'registration/check_free', un)
    if t==[]:
        return True
    else:
        return False

def _new_user(un, pw):
    userdoc=__create_userdict(un, pw)
    core.setdoc('users', userdoc)

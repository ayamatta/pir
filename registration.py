 # -*- coding: utf-8 -*-
import core

def __create_userdict(id, un, pw):
    return {'_id':id, 'un':un, 'pw':pw}

def _username_is_free(un):
    t=core.getdb('users').view('registration/check_free', key=un).rows
    if t==[]:
        return True
    else:
        return False

def _new_user(un, pw):
    glob=core.getdoc('users', "glob")
    glob['counter']=glob['counter']+1
    userdoc=__create_userdict(str(glob['counter']), un, pw)
    core.setdoc('users', glob)
    core.getdb('tasks')[str(-glob['counter'])]={'tasklist':[], 'buf':[], 'taskcounter':0}
    return core.setdoc('users', userdoc)

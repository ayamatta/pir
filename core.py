 # -*- coding: utf-8 -*-
import couchdb
    
def getdb(db):
    return couchdb.Database("http://localhost:5984/"+db)

def getview(db, name, key):
    res=core.getdb(db).view(name, key=key).rows
    values=[]
    for i in res:
        values.append(i['value'])
    return values

def getdoc(db, id):
    return getdb(db)[id]

def setdoc(db, doc):
    getdb(db)[doc['_id']]=doc

def deldoc(db, id):
    del getdb(db)[id]

def _perm_check(groups, perm):
    return (list(set(groups) & set(perm))!=[])

def cani(groups, shit, ifican):
    if 2 in groups:
        return ifican[0](*ifican[1])
    if shit[0]=='_global':
        if (list(set(groups) & set(getdb(shit[1])['_perm'][shit[2]]))!=[]) or (list(set(groups) & set(getdb(shit[1])['_perm']['_full']))!=[]):
            return ifican[0](*ifican[1])
        else:
            return False
    else:
        if (list(set(groups) & set(getdb(shit[1])['_perm'][shit[2]]))!=[]) or (list(set(groups) & set(getdb(shit[1])['_perm']['_full']))!=[]):
            return ifican[0](*ifican[1])
        else:
            return False

#def check_rights(user,module,cmd_type,args=()):
    

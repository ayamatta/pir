import couchdb

#def update(user, db, doc):
    

#def delete(user, db, doc):
    

#def add(user, db, doc):
    
def getdb(db):
    return couchdb.Database("http://localhost:5984/"+db)

def getdoc(db, id):
    return getdb(db)[id]

def setdoc(db, doc):
    getdb(db)[doc['_id']]=doc
    return getdoc(db, doc['_id'])

def cani(groups, shit, ifican):
    if 2 in groups:
        return ifican[0](ifican[1])
    if shit[0]=='_global':
        if (list(set(groups) & set(getdb(shit[1])['_perm'][shit[2]]))!=[]) or (list(set(groups) & set(getdb(shit[1])['_perm']['_full']))!=[]):
            return ifican[0](ifican[1])
        else:
            return False
    else:
        if (list(set(groups) & set(getdb(shit[1])['_perm'][shit[2]]))!=[]) or (list(set(groups) & set(getdb(shit[1])['_perm']['_full']))!=[]):
            return ifican[0](ifican[1])
        else:
            return False

#def check_rights(user,module,cmd_type,args=()):
    
import core
#from time import time

def __create_taskdict(id, title):
    t={'_id': id,
        'title': title, 
        }
    return t

def _get_all_tasks(uid):
    t=core.getdb('tasks').view('users/gettasklist', key=str(-uid)).rows
    tasklist=t[0]['value']
    return tasklist

def _add_task(uid, task):
    tasks=core.getdoc('tasks', str(-uid))
    tasks['taskcounter']=tasks['taskcounter']+1
    tasks['tasklist'].append(__create_taskdict(tasks['taskcounter'], task_title))
    core.setdoc('tasks', tasks)
    return _get_all_tasks(uid)

def _upd_tasks_pos(uid, taskidlist):
    newdoc=core.getdoc('tasks', str(-uid))
    t=newdoc.copy()['tasklist']
    neworder=[]
    for i in taskidlist:
        x=len(t)
        j=-1
        while len(t)==x:
            j=j+1
            if t[j]['_id']==i:
                neworder.append(t[j])
                del t[j]
    newdoc['tasklist']=neworder
    core.setdoc('tasks', newdoc)
    return _get_all_tasks(uid)

def _del_task(uid, tid):
    t=core.getdb('tasks').view('users/gettask', key=[str(-uid), tid]).rows[0]['value']
    new=core.getdoc('tasks',str(-uid))
    del new['tasklist'][new['tasklist'].index(t)]
    core.setdoc('tasks', new)
    return _get_all_tasks(uid)

def _edit_task(uid, new):
    t=core.getdb('tasks').view('users/gettask', key=[str(-uid), new['_id']]).rows[0]['value']
    doc=core.getdoc('tasks',str(-uid))
    doc['tasklist'][doc['tasklist'].index(t)]=new
    core.setdoc('tasks', doc)
    return _get_all_tasks(uid)

def add_task(uid, task_title):
    t=__create_taskdict(tasks['taskcounter'], task_title)
    

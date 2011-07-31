import core
from time import time

def __create_taskdict(id, title, catid=0):
    t={'_id': id,
        'title': title, 
        'catid': catid, 
        'createtime': time()
        }
    return t

def _get_all_tasks(uid):
    t=core.getdb('tasks').view('users/gettasklist', key=str(-uid)).rows
    tasklist=t[0]['value']
    return tasklist

def _add_task(uid, task_title):
    tasks=core.getdoc('tasks', str(-uid))
    tasks['taskcounter']=tasks['taskcounter']+1
    newtask=__create_taskdict(tasks['taskcounter'], task_title)
    tasks['tasklist'].append(newtask)
    core.setdoc('tasks', tasks)
    return newtask

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

def _del_task(uid, tid):
    t=core.getdb('tasks').view('users/gettask', key=[str(-uid), tid]).rows[0]['value']
    new=core.getdoc('tasks',str(-uid))
    del new['tasklist'][new['tasklist'].index(t)]
    core.setdoc('tasks', new)

def _edit_task(uid, new):
    t=core.getdb('tasks').view('users/gettask', key=[str(-uid), new['_id']]).rows[0]['value']
    doc=core.getdoc('tasks',str(-uid))
    doc['tasklist'][doc['tasklist'].index(t)]=new
    core.setdoc('tasks', doc)

def _change_task_category(uid, tid, newcatid):
    t=core.getdb('tasks').view('users/gettask', key=[str(-uid), tid]).rows[0]['value']
    t['catid']=newcatid
    _edit_task(uid, t)

def _get_tasks_by_category(uid, catid):#nado izmenit'
    t=core.getdb('tasks').view('users/gettasklistbycatid', key=[str(-uid), catid]).rows[0]['value']
    return t

def _finish_task(uid, tid):
    t=core.getdb('tasks').view('users/gettask', key=[str(-uid), tid]).rows[0]['value']
    par=core.getdb('tasks').view('users/gettaskparent', key=[str(-uid), tid]).rows
    if par!=[]:
        for i in par:
            t=core.getdb('tasks').view('users/gettask', key=[str(-uid), i['values']]).rows[0]['value']
            t['subtasks'].remove(i['values'])
            if t['subtasks']==[]:
                del t['subtasks']
            if t.has_key('completed_subtasks'):
                t['completed_subtasks'].append(i['values'])
            else:
                t['completed_subtasks']=[i['values']]
    t['finishtime']=time()
    _edit_task(uid, t)

def __filter_finisthed_tasks(full):
    uncompleted=[]
    for i in full:
        if not i.has_key('finishtime'):
            uncompleted.append(i)
    return uncompleted

def _add_task_to_buf(uid, gid, task_title):
    tasks=core.getdoc('tasks', str(gid))
    buftask={'title':task_title, 'creator_id':uid, '_id':int(str(time()).replace('.', ''))}
    if tasks.has_key('buf'):
        tasks['buf'].append(buftask)
    else:
        tasks['buf']=[buftask]
    core.setdoc('tasks', tasks)
    return buftask

def _add_subtask(uid, gid, ptid, task_title, dest='tasklist'):
    if dest=='tasklist':
        subtask=_add_task(uid, task_title)
        parenttask=core.getdb('tasks').view('users/gettask', key=[str(gid), ptid]).rows[0]['value']
        if parenttask.has_key('subtasks'):
            parenttask['subtasks'].append(subtask['_id'])
        else:
            parenttask['subtasks']=[subtask['_id']]
        _edit_task(uid, parenttask)
    if dest=='buf':
        subtask=_add_task_to_buf(uid, gid, task_title)
        parenttask=core.getdb('tasks').view('users/gettaskfrombuf', key=[str(gid), ptid]).rows[0]['value']
        if parenttask.has_key('subtasks'):
            parenttask['subtasks'].append(subtask['_id'])
        else:
            parenttask['subtasks']=[subtask['_id']]
        _edit_task(uid, parenttask)

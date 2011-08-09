 # -*- coding: utf-8 -*-
import core
from time import time

def _first_time(un):
    _create_view(un, "active", "Current tasks")
    _create_view(un, "buf", "My bufer")
    _create_view(un, "arch", "My archive")
    _create_view(un, "ovr", "oversee")

def __create_taskdict(id, title):
    t={'_id': id, 
        'title': title
        }
    return t

def __create_viewdict(vid, vname, path):
    return {'_id':vid, 'title':vname, 'tasks':[], 'subviews':[], 'path':path}

def __newid():
    return str(time()).remove(".", "")

def _create_task(task_title):
    task=__create_taskdict(__newid(), task_title)
    _set_task(task)
    return task

def _create_view(un, vtitle, pid, vname=__newid(),  path=[]):
    view=__create_viewdict(un+"_cat_"+vname, vtitle, path)
    core.setdoc('task-views', view)
    _change_view_path(pid, view['_id'])
    return view

def _get_view_tidlist(vid, recursive=True):
    view=core.getdoc('task-views', vid)
    tidl=view['tasks']
    if recursive:
        for subview in view['subviews']:
            for tid in _get_view_tasklist(subview):
                if not tid in tidl:
                    tidl.append(tid)
    return tidl

def _add_task_to_view(vid, tid):
    view=core.getdoc('task-views', vid)
    view['tasks'].append(tid)
    core.setdoc('task-views', view)

def _del_task_from_view(vid, tid):
    view=core.getdoc('task-views', vid)
    view['tasks'].remove(tid)
    core.setdoc('task-views', view)

def _change_view_path(pvid, cvid, called_recursive=False):
    new_parent=core.getdoc('task-views', pvid)
    child=core.getdoc('task-views', cvid)
    old_path=child['path'][:]
    new_parent['subviews'].append(cvid)
    child['path']=new_parent['paht']+[new_parent['_id']]
    core.setdoc('task-views', new_parent)
    core.setdoc('task-views', child)
    if not called_recursive:
        toclean=[]
        for i in old_path:
            if not i in child['path']:
                toclean.append(i)
        for i in child['tasks']:
            _del_task_from_views(toclean, i)
    for i in child['subviews']:
        _change_view_path(cvid, i, called_recursive=True)

def _del_task_from_views(vids, tid):
    for vid in vids:
        if vid['tasks'].find(tid)!=-1:
            _del_task_from_view(vid, tid)

def _move_task_beth_views(svid, dvid, tid):
    _add_task_to_view(dvid, tid)
    _del_task_from_view(svid, tid)

def _get_tasklist(tidlist):
    tasklist=[]
    for i in tidlist:
        tasklist.append(_get_task(i))
    return tasklist

def _upd_task_order(vid, neworder):
    newview=core.getdoc('task-views', vid)
    newview['tasks']=neworder
    core.setdoc('task-views', newview)

def _del_task(tid):
    core.deldoc('tasks', tid)

def _get_task(tid):
    return core.getdoc('tasks', tid)

def _set_task(task):
    core.setdoc('tasks', task)

def _add_view_to_task(tid, vid):
    '''
    Следует помнить, что vid, который добавляется к делу, указывает исключительно
    на тот вью, к которому дело принадлежит. То есть тут не должно добавляться 
    больше одного вью на пользователя.
    '''
    t=_get_task(tid)
    t['views'].append(vid)
    _set_task(t)

def _del_view_from_task(tid, vid):
    t=_get_task(tid)
    t['views'].remove(vid)
    _set_task(t)

def _move_task_beth_cat(svid, dvid, tid):
    _add_view_to_task(tid, dvid)
    _del_view_from_task(tid, svid)
    _move_task_beth_views(svid, dvid, tid)

def _finish_task(un, tid):
    t=_get_task(tid)
    for i in t['views']:
        if i.split('_')[0]==username:
            source=i
    _move_task_beth_cat(source, un+"_arch", tid)

def _del_task_from_buf(gid, tid):
    t=_get_task_from_buf(gid, tid)
    new=core.getdoc('tasks',str(gid))
    del new['buf'][new['buf'].index(t)]
    core.setdoc('tasks', new)

def _get_task_from_buf(gid, tid):
    t=core.getdb('tasks').view('users/gettaskfrombuf', key=[str(gid), tid]).rows[0]['value']
    return t

def _postpone_task(sgid, dgid, tid):
    t=_get_task_from_buf(str(sgid), tid)
    t['new']=True
    destbuf=core.getdoc('tasks', str(dgid))
    destbuf['buf'].append(t)
    core.setdoc('tasks', destbuf)
    _del_task_from_buf(sgid, tid)
    return t

def _add_note(authid, text, task):
    if task.has_key('notes'):
        task['notes'].append({'createtime':time.time(), 'authid':authid, 'text':text})
    else:
        task['notes']=[{'createtime':time(), 'authid':authid, 'text':text}]
    return task

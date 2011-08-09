 # -*- coding: utf-8 -*-
import core
from time import time

def _first_time(un):
    _create_view(un, "Current tasks", vname="active")
    _create_view(un, "My bufer", vname="buf")
    _create_view(un, "My archive", vname="arch")
    _create_view(un, "Oversee", vname="ovs")
    _create_view(un, "Work", pid=un+"_active")
    _create_view(un, "Family", pid=un+"_active")
    _create_view(un, "Personal", pid=un+"_active")

def __create_taskdict(id, title):
    t={'_id': id, 
        'title': title
        }
    return t

def __create_viewdict(vid, vname, path):
    return {'_id':vid, 'title':vname, 'tasks':[], 'subviews':[], 'path':path}

def __newid():
    return str(time()).replace(".", "")

def _create_task(task_title):
    task=__create_taskdict(__newid(), task_title)
    _set_task(task)
    return task

def _create_view(un, vtitle, pid=None, vname=""):
    if vname=="":
        vname="cat_"+__newid()
    view=__create_viewdict(un+"_"+vname, vtitle, [])
    core.setdoc('task-views', view)
    if pid:
        _change_view_path(pid, view['_id'])
    return view['_id']

def _get_view_tidlist(vid, recursive=True):
    view=core.getdoc('task-views', vid)
    tidl=view['tasks']
    if recursive:
        for subview in view['subviews']:
            for tid in _get_view_tidlist(subview):
                if not tid in tidl:
                    tidl.append(tid)
    return tidl

def _add_task_to_view(vid, tid):
    view=core.getdoc('task-views', vid)
    view['tasks'].append(tid)
    core.setdoc('task-views', view)

def _del_task_from_view(vid, tid):
    view=core.getdoc('task-views', vid)
    if tid in view['tasks']:
        view['tasks'].remove(tid)
        core.setdoc('task-views', view)

def _change_view_path(pvid, cvid, called_recursive=False):
    new_parent=core.getdoc('task-views', pvid)
    child=core.getdoc('task-views', cvid)
    old_path=child['path'][:]
    new_parent['subviews'].append(cvid)
    child['path']=new_parent['path']+[new_parent['_id']]
    core.setdoc('task-views', new_parent)
    core.setdoc('task-views', child)
    if not called_recursive:
        toclean=[]
        for i in old_path:
            if not i in new_parent['path']:
                toclean.append(i)
        for i in child['tasks']:
            _del_task_from_views(toclean, i)
    for i in child['subviews']:
        _change_view_path(cvid, i, called_recursive=True)

def _del_task_from_views(vids, tid):
    for vid in vids:
        _del_task_from_view(vid, tid)

def _move_task_beth_views(svid, dvid, tid):
    dest=core.getdoc('task-views', dvid)
    sour=core.getdoc('task-views', svid)
    for i in sour['path']:
        if not i in dest['path']:
            _del_task_from_view(i, tid)
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
    _del_task_from_views(core.getview('task-views', 'tasks/getvidlistbytid', tid, reduce=True)[0], tid)

def _get_task(tid):
    return core.getdoc('tasks', tid)

def _set_task(task):
    core.setdoc('tasks', task)

def _finish_task(un, tid):
    t=_get_task(tid)
    t['finished']=__newid()
    _set_task(t)
    _move_task_beth_cat(source, un+"_arch", tid)

def _postpone_task(sgid, dgid, tid):
    t=_get_task(tid)
    for i in t['views']:
        if i.split('_')[0]==dgid:
            already=True
    if not already:
        _add_task_to_view(dgid+"_buf", tid)
    move_task_beth_cat(sgid+"_buf", dgid+"_buf", tid)
    return t

def _add_note(authid, text, task):
    if task.has_key('notes'):
        task['notes'].append({'createtime':time.time(), 'authid':authid, 'text':text})
    else:
        task['notes']=[{'createtime':time(), 'authid':authid, 'text':text}]
    return task

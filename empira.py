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

def __create_projdict(vid, vname, path):
    return {'_id':vid, 'title':vname, 'tasks':[], 'subviews':[], 'path':path, 'finished_tasks':[]}

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

def _create_proj(un, ptitle, pid):
    pname="proj_"+__newid()
    proj=__create_projdict(un+"_"+pname, ptitle, [])
    core.setdoc('task-views', proj)
    _change_view_path(pid, proj['_id'])
    return proj['_id']

def _get_view_tidlist(vid, recursive=True):
    view=core.getdoc('task-views', vid)
    tidl=view['tasks']
    if recursive:
        for subview in view['subviews']:
            for tid in _get_view_tidlist(subview):
                if not tid in tidl:
                    tidl.append(tid)
    return tidl

def _add_task_to_view(vid, tid, dest="tasks"):
    view=core.getdoc('task-views', vid)
    view[dest].append(tid)
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
    _add_task_to_view(dvid, tid)
    for i in sour['path']:
        if not i in dest['path']:
            _del_task_from_view(i, tid)
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
    _del_task_from_views(core.getview('task-views', 'tasks/getvidlistbytid', tid, reduce=True), tid)

def _get_task(tid):
    return core.getdoc('tasks', tid)

def _set_task(task):
    core.setdoc('tasks', task)

def postpone(sgid, dgid, tid):
    t=_get_task(tid)
    t['postponer']=sgid
    _set_task(t)
    _move_task_beth_views(sgid+"_buf", dgid+"_buf", tid)
    subscribe(sgid, tid)
    return True

def accept(un, tid):
    _move_task_beth_views(un+"_buf", un+"_active", tid)
    return True

def refuse(un, tid):
    t=_get_task(tid)
    _move_task_beth_views(un+"_buf", t['postponer']+"_buf", tid)
    unsubscribe(t['postponer'], tid)
    del t['postponer']
    _set_task(t)
    return True

def subscribe(gid, tid):
    _add_task_to_view(gid+"_ovs", tid)
    return True

def unsubscribe(gid, tid):
    _del_task_from_view(gid+"_ovs", tid)
    return True

def new(title, view):
    task=_create_task(title)
    _add_task_to_view(view, task['_id'])
    return task

def mv(tid, vid):
    path=core.getview('task-views', 'tasks/getfullpath', tid, reduce=True)
    _move_task_beth_views(path[-1], vid, tid)
    return True

def finish(un, tid):#optimize it
    t=_get_task(tid)
    t['finished']=time()
    t['finisher']=un
    path=core.getview('task-views', 'tasks/getfullpath', tid, reduce=True)
    t['finish_view']=path[-1]
    _set_task(t)
    view=core.getdoc('task-views', path[-1])
    if view['_id'].split('_')[1]=="proj":
        _add_task_to_view(view['_id'], tid, dest="finished_tasks")
    _move_task_beth_cat(path[-1], un+"_arch", tid)
    return True

def rm(tid):
    _del_task(tid)
    return True

def get(tid):
    return _get_task(tid)

def rename(tid, newtitle):
    task=_get_task(tid)
    task['title']=newtitle
    _set_task(task)
    return True

def neworder(vid, orderlist):
    _upd_task_order(vid, orderlist)
    return True

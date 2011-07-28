import core
from time import time

def get_all_my_tasks(args):
    t=core.getdb('tasks').view('users/gettasksbyuid', key=args['user']['_id']).rows
    tasklist=[]
    for i in t:
        tasklist=[i['value']]+tasklist
    return tasklist

def add_task(args):
    args['user']['taskcount']=args['user']['taskcount']+1
    args['user']['waitcount']=args['user']['waitcount']+1
    t={'_id': args['user']['_id']+"-"+ str(args['user']['taskcount']), 
        'vasya':args['user']['_id'], 
        'title':args['task_title'], 
        'add_time':int(time()), 
        'status':"waiting", 
        'pos':args['user']['waitcount']
        }
    return core.setdoc('tasks', t)

#def empira_add_task_rel(user, tid, gid):
#    check_rights(user,'empira','add_task_rel',(gid, tid ))

def upd_tasks_pos(args):
    t=0
    for i in args['newposarr']:
        t=t+1
        e=core.getdoc('tasks', args['user']['_id']+'-'+str(i))
        if e['pos']!=t:
            e['pos']=t
            core.setdoc('tasks', e)

def read_task_desc(user, tid):
    t=check_rights(user,'empira','read_task_desc',(tid,))

def del_task(user, tid):
    t=check_rights(user,'empira','del_task',(tid,user['id']))

#def empira_start_task(user, tid):
#    t=check_rights(user,'empira','start_task',(tid,user['id']))

#def empira_finish_task(user, tid):
#    t=check_rights(user,'empira','finish_task',(tid,user['id']))

#def empira_postpone_task(user, tid):
#    t=check_rights(user,'empira','postpone_task',(tid,user['id']))

def archive_add(user, tid):
    t=check_rights(user,'empira','add_to_archive',(tid,user['id']))

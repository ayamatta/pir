import core

def __create_group_dict(bossid, name, id):
    return {'perm':{'_full':[-bossid]}, 'name':name, '_id':str(id), 'members':[bossid], 'parents':[1], 'buf':[]}

def _create_group(bossid, name):
    glob=core.getdoc('groups', "glob")
    glob['counter']=glob['counter']+1
    temp=__create_group_dict(bossid, name, glob['counter'])
    core.setdoc('groups', glob)
    return core.setdoc('groups', temp)

def _add_member(uid, gid):
    group=core.getdoc('groups', str(gid))
    group['members'].append(uid)
    core.setdoc('groups', group)

def _del_group(gid):
    del core.getdb('groups')[str(gid)]

#def _add_parent(pid, cid):
#    child=core.getdoc('groups', str(gid))
#    child['parents'].append(pid)
#    core.setdoc('groups', child)

#def _del_parent

#def _compare_groups

#def _edit_group_perm

#def 

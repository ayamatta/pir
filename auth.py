import core
def log_the_user_in(un, pw):
    user=core.getdb('users').view("login/validation",key=[un,pw]).rows
    if user!=[]:
        user=user[0]['value']
        groups=core.getdb('groups').view("users/membership",key=int(user['_id']), reduce=True).rows[0]['value']
        groups.append(-int(user['_id']))
        user['groups']=groups
        user['_id']=int(user['_id'])
        return user
    else:
        return False

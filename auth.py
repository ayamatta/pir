import core
def log_the_user_in(un, pw):
    user=core.getdb('users').view("login/validation",key=[un,pw]).rows
    if user!=[]:
        user=user[0]['value']
        groups=core.getdb('groups').view("users/membership",key=int(user['_id'])).rows[0]['value']
        groups.append(-int(user['_id']))
        user['groups']=groups
        return user
    else:
        return False

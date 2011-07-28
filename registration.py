 # -*- coding: utf-8 -*-
from core import check_rights
from auth import auth_log_the_user_in
regbot={'username':'regbot','groups':[-2],'uid':2}

def reg_username_is_free(un, rfu=regbot):
    t=check_rights(rfu,'reg','un_is_free',(un,))
    if t[0]>0:
        return False
    return True

def reg_user(un, pw, groups=[], rfu=regbot):
    check_rights(rfu,'reg','reg_user',(un,pw))
    return auth_log_the_user_in(un)

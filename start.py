 # -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, url_for, abort, escape
import auth, empira

app = Flask(__name__)

def my_page():
    tasklist=empira.__filter_finisthed_tasks(empira._get_all_tasks(session['user']['_id']))
    return render_template("empira.html", tl=tasklist)

def not_my_page():
    return u"not mine"

@app.route('/ajax/_tasklist/<uid>')
def tasklist(uid):
    tasklist=empira.__filter_finisthed_tasks(empira._get_all_tasks(uid))
    if uid!=session['user']['_id']:
        v=[]
        for i in tasklist:
            if core._perm_check(session['user']['groups'], i['perm']['view']):
                v.append(i)
    tasklist=v
    for i in tasklist:
        i['title']=escape(i['title'])
    return render_template("tasklist", tl=tasklist)

@app.route('/ajax/_del_task/<tid>')
def del_task(tid):
    empira._del_task(session['user']['_id'], tid)
    return redirect("/user/"+session['user']['username'])

@app.route('/ajax/_upd_pos', methods=['POST'])
def upd():
    sl=request.form['sl']
    sl=eval(sl)
    print sl
    empira._upd_tasks_pos(session['user']['_id'], sl)
    return ""#redirect("/"+session['user']['username'])

@app.route('/ajax/_add_new_task', methods=['POST'])
def add_task():
    t=empira._add_task(session['user']['_id'],request.form['title'])
    return render_template("task_elem", t=t)

@app.route('/ajax/_finish_task/<tid>')
def finish_task(tid):
    empira._finish_task(session['user']['_id'], tid)

@app.route('/',methods=['POST','GET'])
def login():
    if request.method=='POST':
        t=auth.log_the_user_in(request.form['username'],request.form['pass'])
        if t:
            session['user']=t
            return redirect("/user/")
        else:
            return 'invalid username/password'
    if 'user' in session:
        return redirect("/user/"+session['user']['un'])
    return '''
    <body>
        <form method=POST id=form>
        <input type=text name=username><br>
        <input type=password name=pass><br>
        <input type="submit" value="Login" />
        </form>
    </body>
    '''

@app.route('/user/')#личная страничка
def user():
    if user in session:
        return my_page()
    else:
        return redirect("/")

@app.route('/user/<username>')#личная страничка
def page(username):
    if session['user']['un']==username:
        return my_page()
    else:
        return not_my_page()
        

@app.route('/version/005')
def vers():
    return """sdf"""

app.secret_key="fwqefADSOFWepjdsOGjewoNGVODSJvgoewvOEWJ#$)T@#G@J$YGEWN(G@$*#FFFEWewf@"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

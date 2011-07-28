 # -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, url_for, abort, escape
import auth, empira

app = Flask(__name__)

def my_page_empira():
    tasklist=empira_get_all_my_tasks(session['user'])
    return render_template("empira.html", tl=tasklist)

def not_my_page_empira():
    return u"not mine"

@app.route('/_del_task/<tid>')
def del_task(tid):
    empira_del_task(session['user'], tid)
    return redirect("/user/"+session['user']['username'])

@app.route('/_upd_pos', methods=['POST'])
def upd():
    sl=request.form['sl']
    x=0
    for i in eval(sl):
        x=x+1
        empira_upd_task_pos(session['user'], i, x)
    return ""#redirect("/"+session['user']['username'])

@app.route('/_add_new_task', methods=['POST'])
def add_task():
    def to_li(t):
        txt='<li class="ui-state-default" id="'+escape(str(t['tid']))+'"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>'+t['title']+'</li>'
        return txt
    t=empira_add_task(session['user'],escape(request.form['title']))
    return to_li(t[0])

@app.route('/',methods=['POST','GET'])#здесь должен быть логин
def login():
    if request.method=='POST':
        t=auth.log_the_user_in(escape(request.form['username']),escape(request.form['pass']))
        if t!=False:
            session['user']=t
            return redirect("/user/"+session['user']['un'])
        else:
            return 'invalid username/password'
    if 'user' in session:
        return redirect("/user/"+session['user']['username'])
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
        return redirect("/user/"+session['user']['username'])
    else:
        return redirect("/")

@app.route('/user/<username>')#личная страничка
def page(username):
    if session['user']['username']==username:
        return my_page_empira()
    else:
        return not_my_page_empira()
        
@app.route('/version/005')
def vers():
    return """
Версия 0.05, которой не должно было быть.<br>
Определённо dev.<br>
<br>
Мой раб, который веб-дизайнер, ушёл в запой. Я пинаю заборы. Такие дела.<br>
Итак, в этой версии:<br>
(извините, мне стыдно это писать, но пока что у нас ровно нихуя. Этого<br>
недорелиза вообще бы не было, если б меня больно не укусила в мозг <br>
мерзкая личинка под названием "совесть")<br>
+ Добавление дел<br>
+ Сортировка дел<br>
+ Сохранение порядка дел<br>
+ Удаление дел<br>
<br>
+ Регистрация (пока что регать могут только админы, то есть только я)<br>
+ Аутентефикация<br>
<br>
Ну а теперь немного о будущем. Начнём, разумеется, с ту-ду листа для <br>
версии 0.1:<br>
* ПРИШИТЬ ДИЗАЙН, БЛЕАТЬ!<br>
* Сделать простенький архив дел, и, соответственно, кнопку "дело сделано"<br>
* Сделать кнопки "взяться за дело" и "отложить дело"<br>
    Эти кнопочки нужны чтобы знать сколько времени на какое дело у вас ушло.<br>
* (Возможно) Просмотр чужих списков дел<br>
* (Возможно) Поручить дело другому человеку (в 0.2 эта возможность должна быть обязательно)<br>
Планируемое время обновления до 0.1 - завтра, 13 июля 2011-го года, ближе к полуночи.<br>

Думаю, кому-то могут быть интересны дальнейшие планы. Что ж, до версии 0.4 проект будет<br>
работать в тестовом режиме, в 0.4 открою регистрацию. С версии 0.7 выложу<br>
сорцы. В том числе всех предыдущих версий. А если говорить о вещах более<br>
насущных - в версии 0.2 должна появиться возможность группировать дела.<br>
В версии 0.3 - возможность строить иерархии дел (на базе майндмапов) и <br>
пользователей (чтобы можно было знать, кто кому может давать задания).<br>
В версии 0.4 хочу реализовать буферы дел для групп и, желательно, <br>
жаббер-гейт к этому добру.<br>
Надеюсь добраться до 0.4 к августу, но сопящая пьяная рожа рядом намекает,<br>
что чёрта с два я успею.<br>
Планы на 0.7 и 1.0 - октябрь и январь соответственно.
    """

app.secret_key="fwqefADSOFWepjdsOGjewoNGVODSJvgoewvOEWJ#$)T@#G@J$YGEWN(G@$*#FFFEWewf@"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

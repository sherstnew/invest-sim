from ast import Try
from cmath import log
import re
from flask import render_template, request, redirect, make_response
from flask import Flask
import sqlite3
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from flask import Flask,send_from_directory
import os
from translate import Translator
translator= Translator(to_lang="ru")
application=Flask(__name__)



chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
login = ''
uname = ''
unamenew = ''
email = ''
password = ''
password2 = ''
last_name = ''
username = ''
token = ''
tokens = []
email_confirm = ''
accounts = ''
email_url = ''
connection = sqlite3.connect('regist_db.db')
cursor = connection.cursor()
cursor.execute("""select * from reg1""")
rows = cursor.fetchall()
for row in rows:
    accounts = accounts + str(row) + ';'
connection.commit()
cursor.close()
connection.close()
app = Flask(__name__)

@app.route('/api',  methods=['GET', 'POST'])
def api():
    if request.method == 'POST':

        connection = sqlite3.connect('regist_db.db')
        cursor = connection.cursor()

        if request.json['action'] == 'accounts':
            accs = {
                "accounts": ""
            }
            accs['accounts'] = accounts
            accs = json.dumps(accs)
            return accs
        elif request.json['action'] == 'changes':
            cursor.execute("update reg1 set name_id='" + request.json['name']  + "', password='" + request.json['password'] +"', email='" + request.json['email'] + "' where token=" + request.json['utoken'])
            connection.commit()
            cursor.close()
            connection.close()
            return 'OK'
        elif request.json['action'] == 'pday':
            pday = '10%'
            return pday
        elif request.json['action'] == 'pyear':
            pyear = '20%'
            return pyear
        elif request.json['action'] == 'history':
            cursor.execute("select * from history where token=" + request.json['utoken'])
            history = cursor.fetchall()
            return history

        cursor.execute("select balance from fin where token=" + request.json['utoken'])

        bal = int(cursor.fetchall()[0][0])
        token = request.json['utoken']

        with open('static/shares.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        cursor.execute("select shares from fin where token=" + token)
        shares = json.loads(cursor.fetchall()[0][0])
        if str(request.json['act_id']) not in shares:
            shares[request.json['act_id']] = "0"

        current_amount = int(shares[str(request.json['act_id'])])

        if request.json['action'] == 'buy':
            if bal >= int(request.json['cost']):
                bal = bal - int(request.json['cost'])
                current_amount+=1
                shares[request.json['act_id']] = str(current_amount)
                cursor.execute("update fin set shares ='" + json.dumps(shares) + "' where token=" + token)
                cursor.execute("update fin set balance =" + str(bal) + " where token=" + token)
                cursor.execute("insert into history (token, method, act_id, cost) values (" + token + ", 'buy', '" + request.json['act_id'] + "', '" + request.json['cost'] + "')")
                connection.commit()
                cursor.close()
                connection.close()
                return 'OK'
            else:
                return 'NO_MONEY'
        elif request.json['action'] == 'sell' and current_amount > 0:
            bal = bal + int(request.json['cost'])
            current_amount-=1
            shares[request.json['act_id']] = str(current_amount)
            cursor.execute("update fin set shares ='" + json.dumps(shares) + "' where token=" + token)
            cursor.execute("update fin set balance =" + str(bal) + " where token=" + token)
            cursor.execute("insert into history (token, method, act_id, cost) values (" + token + ", 'sell', '" + request.json['act_id'] + "', '" + request.json['cost'] + "')")
            connection.commit()
            cursor.close()
            connection.close()
            return 'OK'
        else:
            return('NO_SHARES')

    return 'ok'



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.cookies['token'] != '':
        ic1 = 147
        ic2 = 138
        ic3 = 509
        ic4 = 287
        connection = sqlite3.connect('regist_db.db')
        cursor = connection.cursor()
        cursor.execute('select balance from fin where token=' + request.cookies['token'])
        income = cursor.fetchall()[0][0]
        connection.commit()
        cursor.close()
        connection.close()
        return render_template('/home.html', ic1=ic1, ic2=ic2, ic3=ic3, ic4=ic4, income=income, accounts=accounts)
    else:
        return redirect('/login', 302)

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    actbuy = ''
    actbuy = request.form.get('act_num')  # сколько акций купил
    if actbuy != '' and actbuy != None:
        print(actbuy)
        return redirect('/buy', code=302)
    return render_template('/buy.html', accounts=accounts)

@app.route('/act', methods=['GET', 'POST'])
def buyact():
    act_id = request.args['id']

    with open('static/shares.json', 'r', encoding='utf-8') as f:
        text = json.load(f)

    act_name = text['name'][act_id]

    act_sector = text['sector'][act_id]
    act_sector = translator.translate(act_sector)
    act_desc = act_name + ' is very good shares'
    buy_cost = 13
    sell_cost = 12
    daily_cost = 20
    buy_comission = 1
    sell_comission = 1
    buy_total = 12
    sell_total = 12
    lots = 100


    return render_template('/act.html', act_name = act_name, act_desc = act_desc, act_sector = act_sector, buy_cost = buy_cost, sell_cost = sell_cost, daily_cost = daily_cost, buy_comission = buy_comission, sell_comission = sell_comission, buy_total = buy_total, sell_total = sell_total, lots = lots)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    userpic = '/static/userpic.svg'
    if request.method == 'POST':
        resp = make_response(redirect('/', 302))
        resp.set_cookie('token', '')
        return resp
    return render_template('/profile.html', userpic=userpic, accounts=accounts)


@app.route('/reg', methods=['GET', 'POST'])
def reg():

    global login
    global password2
    global password
    global email
    global uname
    password = str(request.form.get('password'))
    password2 = str(request.form.get('password2'))
    login = str(request.form.get('login'))
    email = str(request.form.get('email'))
    uname = login
    if password == password2 and len(password) >= 6 and "@" in email and "." in email and login != "None" and len(
            login) >= 3 or request.method == 'POST':
        connection = sqlite3.connect('regist_db.db')
        cursor = connection.cursor()

        num = 0

        result = cursor.execute("select token from reg1")
        arr = result.fetchall()
        tokens = [str(i[0]) for i in arr]

        for n in range(1):
            token_new = ''
            for i in range(20):
                token_new += random.choice(chars)

        while num <= 1:
            for i in tokens:
                if i == token_new:
                    result = cursor.execute("select token from reg1")
                    arr = result.fetchall()
                    tokens = [str(i[0]) for i in arr]
                    for n in range(1):
                        token_new = ''
                        for i in range(20):
                            token_new += random.choice(chars)
                else:
                    num = 5


        for n in range(1):
            email_url = ''
            for i in range(20):
                email_url += random.choice(chars)

        sqle = f"""insert into  reg1 (token, name_id, email, password, email_key)
        Values ("{token_new}", "{login}","{email}","{password}", "{email_url}"
        )"""
        cursor.execute(sqle)

        sqle = 'insert into  fin (token, balance, shares) Values ("' + token_new + ' ", 500, "{"0: "0"}")'
        cursor.execute(sqle)

        email_confirm = 'http://127.0.0.1:5000/emailconfirm' + '?' + 'key=' + email_url
        connection.commit()
        cursor.close()
        connection.close()

        email = str(email)
        msg = MIMEMultipart()
        msg['From'] = 'Invest Simulator'
        msg['To'] = email
        msg['Subject'] = 'Please, confim your e-mail'
        message = """    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400&display=swap" rel="stylesheet">
        <title>Email</title>
    </head>
    <body style="font-family: 'Montserrat', sans-serif;
                margin: 0;
                padding: 0;">
    <div class="container" style="width: 1000px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;">
        <div class="desc" style="font-size: 20px;
                width: 1000px;
                color: black;
                background: #fcbb4a;
                padding: 30px;
                border-radius: 20px;">
            <img src="http://shite.rf.gd/valeraicon.png" alt="logo" class="logo" style="width: 75px;
                height: 75px;
                margin: 0px 0px 30px 0px;">
            <a href=""" + email_confirm + """ style="text-decoration: none; color: black;">
            <div class="conf-btn" style="font-size: 25px;
                width: 300px;
                background: #fffbff;
                border-radius: 20px;
                margin-top: 30px;
                text-align: center;
                padding: 20px;">Подтвердить</div>
            </a>
            <br><br>
            <span class="up-desc">Здравствуйте, """ + login + """, чтобы пользоваться нашими услугами осталось только подтвердить вашу электронную почту. Чтобы подтвердить почту нажмите на кнопку выше или перейдите по ссылке: """ + email_confirm + """</span>
            <br><br>
            <span class="alert">Если это были не вы, проигнорируйте данное письмо</span>
            <br><br>
            <span class="und-desc" style="color: grey;
                font-size: 15px;">Данное письмо формируется автоматически, пожалуйста, не отвечайте на него </span>
        </div>
    </div>
    </body>
    </html>"""
        msg.attach(MIMEText(message, 'html'))
        mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mailserver.ehlo()
        mailserver.ehlo()
        mailserver.login('simulatorinvestment@gmail.com', 'gjhwrskytmcqzqlk') # для яндекса использовать пароль aagajxrvrwkznihm для гугл gjhwrskytmcqzqlk
        mailserver.sendmail('simulatorinvestment@gmail.com', email, msg.as_string())
        mailserver.quit()
        return render_template('/reg.html', password=password, login=login, password2=password2, email=email)
    else:
        return render_template('/reg.html', password=password, login=login, password2=password2, email=email)

@app.route('/emailconfirm', methods=['GET', 'POST'])
def emailpage():
    try:
        key = request.args['key']
    except:
        return render_template('/emailconfirm.html')
    if key != '':
        connection = sqlite3.connect('regist_db.db')
        cursor = connection.cursor()
        key = "'" + key + "'"
        cursor.execute("""select token from reg1 where email_key=""" + key)
        rows = cursor.fetchall()

        for row in rows:
            key = row

        key = str(key)
        key = key.replace('(', '')
        key = key.replace(')', '')
        key = key.replace(',', '')
        key = key.replace("'", "")

        resp = make_response(redirect('/emailconfirm', 302))
        resp.set_cookie('token', key)
        sqle = f"""insert into  reg1 (email_confirm) Values (true)"""
        cursor.execute(sqle)
        connection.commit()
        cursor.close()
        connection.close()
        return resp
    else:
        return render_template('/emailconfirm.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
        email = str(request.form.get('email'))
        if request.method == 'POST':
            connection = sqlite3.connect('regist_db.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT token FROM reg1 WHERE email='{email}'")
            token = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()

            token = str(token[0])
            token = token.replace('(', '')
            token = token.replace(')', '')
            token = token.replace(',', '')
            token = token.replace("'", "")


            resp = make_response(redirect('/', 302))
            resp.set_cookie('token', token)

            return resp
        else:
            return render_template('/login.html', accounts = accounts)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global login
    global uname
    global username
    global unamenew
    global password
    global email
    global last_name
    userpic = '/static/userpic.svg'
    passw = password  # пароль
    email = email
    unamenew = str(request.form.get('uname'))
    passwnew = str(request.form.get('pass'))
    emailnew = str(request.form.get('email'))

    if uname != unamenew and unamenew != 'None':
        uname = unamenew
        print(uname)
        unamenew = ''

    if passw != passwnew and passwnew != 'None':
        passw = passwnew
        print(passw)
        passwnew = ''
        # редактировать пароль
    if email != emailnew and emailnew != 'None' and "@" in emailnew and "." in emailnew:
        email = emailnew
        print(email)
        emailnew = ''
    # редактировать email
    return render_template('/settings.html', userpic=userpic, uname=uname, passw=passw, email=email)


@app.errorhandler(404)
def err404(e):
    return render_template('/404.html'), 404


@app.route('/plan', methods=['GET', 'POST'])
def plan():
    return render_template('/plan.html')


@app.route('/attr', methods=['GET', 'POST'])
def attr():
    return render_template('/attr.html')

@app.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('/history.html')

app.run()

connection = sqlite3.connect('regist_db.db')
cursor = connection.cursor()
cursor.execute("""select * from reg1""")
rows = cursor.fetchall()


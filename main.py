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




@app.route('/', methods=['GET', 'POST'])
def index():
    timebut = "day"
    perinc = 15
    ic1 = 147
    ic2 = 138
    ic3 = 509
    ic4 = 287
    income = ic1 + ic2 + ic3 + ic4
    userpic = 'userpic'
    timebut = "за день"
    timech = request.form.get('timebut')
    if timech == "за день":
        timebut = "за год"
        perinc = "-3"
    elif timech == "за год":
        timebut = "за день"
        perinc = "15"
    return render_template('/home.html', ic1=ic1, ic2=ic2, ic3=ic3, ic4=ic4, income=income, perinc=perinc,
                           userpic=userpic, timebut=timebut, accounts=accounts)

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    actbuy = ''
    actbuy = request.form.get('act_num')  # сколько акций купил
    if actbuy != '' and actbuy != None:
        print(actbuy)
        return redirect('/buy', code=302)
    return render_template('/buy.html')


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
    key = request.args['key']
    connection = sqlite3.connect('regist_db.db')
    cursor = connection.cursor()
    key = "'" + key + "'"
    print(key)
    cursor.execute("""select token from reg1 where email_key=""" + key)
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    connection.commit()
    cursor.close()
    connection.close()
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


app.run()

connection = sqlite3.connect('regist_db.db')
cursor = connection.cursor()
cursor.execute("""select * from reg1""")
rows = cursor.fetchall()


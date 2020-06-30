import os
import re
import smtplib
import datetime
import psycopg2
from flask import Flask, render_template, request
import random
import sys

# Global Variables
email = ""
regemail = ''
password = ""
regpassword = ''
resetlink = ''
headinglist = []
regheadinglist = []
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
names = {'francopret@gmail.com': 'Franco', 'franco.pretorius@pretoriusse.net': 'Franco',
         'franco.pretorius@psg.co.za': 'Franco', 'heliztap@gmail.com': 'Helizta', 'heyssen@consol.co.za': 'Helizta',
         'helizta.pretorius@pretoriusse.net': 'Helizta', 'lorrein.pretorius@gmail.com': 'Lorrein',
         'lorrein.pretorius@pretoriusse.net': 'Lorrein', 'lorrein.pretorius@icloud.com': 'Lorrein',
         'liam.pretorius@pretoriusse.net': 'Liam', 'liam.pretorius2@gmail.com': 'Liam', 'liamp@orban.co.za': 'Liam',
         'liam.pretorius2@outlook.com': 'Liam', 'raine.pretorius1@gmail.com': 'Raine',
         'raine.pretorius@pretoriusse.net': 'Raine', 'ruddieprettie@gmail.com': 'Rudolph',
         'rudolph.pretorius@pretoriusse.net': 'Rudolph', 'sileziap@gmail.com': 'Silezia',
         'silezia.pretorius@pretoriusse.net': 'Silezia', 'spretorius@consol.co.za': 'Silezia',
         'tekara.pretorius@pretoriusse.net': 'Tekara', 'tekarahelizta@gmail.com': 'Tekara',
         'info@pretoriusse.net': 'Info'}


def mailnew(enteredemail, enteredpassword, name):
    """
    DOCSTRING : Sends an email to create a new user.
    :param enteredemail: Email entered into form
    :param enteredpassword: Password entered into form.
    :param name: name of the new user.
    """
    # =============================================================================
    # SET EMAIL LOGIN REQUIREMENTS
    # =============================================================================
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    recipientlist = ['raine.pretorius@pretoriusse.net', 'charl.botha@pretoriusse.net', 'tech@pretoriusse.net']
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Create new User.\n
    Hi Raine and Charl,

    Please create new user in the website table. The email is : {enteredemail}.   The password is {enteredpassword}.   The name of the user is {name}.

    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()


def mailreset(name, enteredemail, link):
    """
    DOCSTRING : Sends an email to create a new user.
    :param enteredemail: Email entered into form
    :param enteredpassword: Password entered into form.
    :param name: name of the new user.
    """
    # =============================================================================
    # SET EMAIL LOGIN REQUIREMENTS
    # =============================================================================
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    recipientlist = []
    recipientlist.append(enteredemail)
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Reset Password
    Hi {name},

    Here is the link to reset your password :
    {link}

    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()


def checklogin(email, password):
    """
    DOCSTRING : Checks if the users username and passwords are correct. If correct updates last login.
    :param email: Email user entered into the login form.
    :param password: Password the user entered into the login form.
    :return: True or False.
    """
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Authentication')
    s1cursor = server_1.cursor()
    sqlcheck = f"SELECT PASSWORD FROM website WHERE email = '{email.lower()}'"
    s1cursor.execute(sqlcheck)
    sqlpassword = s1cursor.fetchall()
    sqlpassword = str(sqlpassword).replace("[('", "").replace("',)]", "")
    if password == sqlpassword:
        sqlupdate = f"UPDATE website SET last_login = NOW() WHERE email = '{email.lower()}';"
        s1cursor.execute(sqlupdate)
        server_1.commit()
        s1cursor.close()
        server_1.close()
        return True
    else:
        return False


def isemail(email):
    """
    DOCSTRING : Checks if parameter entered is an email.
    :param email:
    :return: True or False.
    """
    global regex
    if (re.search(regex, email)):
        return True
    else:
        return False


app = Flask(__name__)


@app.route("/")
def home():
    """
    DOCSTRING : Returns login screen.
    :return: Rendered index.html.
    """
    return render_template("index.html")


@app.route("/index.html")
def index():
    """
    DOCSTRING : Returns index.html if it is asked for.
    :return: Rendered index.html
    """
    return render_template("index.html")


@app.route("/helpdesk", methods=["GET", "POST"])
def need_input():
    """
    DOCSTRING : Checks if the login details provided are correct and the returns helpdesk{user's name}.html. Else it returns forbidden.html.
    :return: helpdesk{user's name}.html or forbidden.html
    """
    global email
    global password
    global headinglist
    headinglist = []
    for key, value in request.form.items():
        if key == "Email":
            email = value
        elif key == "Password":
            password = value
    if checklogin(email, password):
        cwd = os.getcwd()
        t = "templates"
        location = f"heldesk{names[email]}.html"
        locationmain = f"{cwd}\{t}\heldeskmain.html"
        html = open(locationmain)
        file = html.readlines()
        html.close()
        for i in file:
            headinglist.append(i)
        headinglist[9] = f'    <h1>Hello {names[email]}.</h1>\n'
        htmltemplate = open(f"server/templates\{location}", "w+")
        for j in headinglist:
            if j not in htmltemplate.readline():
                htmltemplate.writelines(j)
        htmltemplate.close()
        return render_template(location)
    else:
        return render_template("forbidden.html")


@app.route("/register.html", methods=["GET"])
def register():
    """
    DOCSTRING : New user enters their details.
    :return: Details entered into form.
    """
    return render_template("register.html")


@app.route("/registernew", methods=["POST"])
def get_input():
    """
    DOCSTRING : Sends email to IT to create an new User.
    :return The html to let the user know support will create a new user.
    """
    for key, value in request.form.items():
        if key == "Email":
            pemail = value
        elif key == "Password":
            ppassword = value
        elif key == 'Name':
            pname = value
    mailnew(pemail, ppassword, pname)
    return (f"""
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Registered</title>
    <link rel="stylesheet" href="/static/css/master.css">
    <link rel="icon" href="/static/images/profile.png">
  </head>
  <body>
    <h1>Hello {pname}.</h1>
    <p>You have been successfully registered. Please wait 24 hours before logging in.</p>
  </body>
</html>
""")


@app.route('/reset', methods=['get'])
def reset():
    """
    DOCSTRING : Returns form to reset password.
    :return:
    """
    return render_template('reset.html')


@app.route("/resetpassword", methods=['Get', 'Post'])
def change_password():
    for key, value in request.form.items():
        if key == "Email":
            pemail = value
        elif key == "Password":
            ppassword = value
        elif key == 'Newpassword':
            pnewpassword = value
        elif key == "Newpassword1":
            pnewpassword1 = value
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Authentication')
    s1cursor = server_1.cursor()
    s1cursor.execute(f"SELECT password FROM website WHERE email = '{pemail}'")
    sqlpass = s1cursor.fetchall()
    sqlpass = str(sqlpass).replace("[('", "").replace("',)]", "")
    if ppassword == sqlpass:
        s1cursor.execute(f"UPDATE WEBSITE SET password = '{pnewpassword}' WHERE email = '{pemail}'")
    else:
        return (f"""
        <html lang="en" dir="ltr">
            <head>
                <meta charset="utf-8">
                <title>Wrong Password</title>
                <link rel="stylesheet" href="/static/css/master.css"> 
                <link rel="icon" href="/static/images/profile.png">
            </head>
            <body>
                <h1>Hello {names[pemail]}.</h1>
                <p>The old password you entered does not match any password assosiated with your email in our records.</p>
            </body>
        </html>

        """)
    return (f"""
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Pasword Changed</title>
    <link rel="stylesheet" href="/static/css/master.css"> 
    <link rel="icon" href="/static/images/profile.png">
  </head>
  <body>
    <h1>Hello {names[pemail]}.</h1>
    <p>Your password has been changed to : {pnewpassword}.</p>
  </body>
</html>
""")


@app.route("/create_ticket.html", methods=['get', "Post"])
def tickethtml():
    return render_template("create_ticket.html")


@app.route('/create_ticket', methods=['get', "post"])
def create_ticket():
    global names
    tiketemail = ''
    comments = ""
    for key, value in request.form.items():
        if key == "Email":
            tiketemail = value
        elif key == "Comments":
            comments = value
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')
    s1cursor = server_1.cursor()
    postgreSQL_select_Query = f"SELECT help_id FROM OPEN ORDER BY help_id DESC LIMIT 1;"
    s1cursor = server_1.cursor()
    s1cursor.execute(postgreSQL_select_Query)
    pid = s1cursor.fetchall()
    pid = str(pid).replace("[(", "").replace(",)]", "")
    uid = int(pid) + 1
    tiketnum = f"{names[tiketemail][0]}{uid}P"
    sqlupdate = f"INSERT INTO open(help_id, ticketnum, date_opened, email, comments, closed) VALUES({uid}, '{tiketnum}', NOW(), '{tiketemail}', '{comments}', False);"
    s1cursor.execute(sqlupdate)
    server_1.commit()
    s1cursor.close()
    server_1.close()
    return (f"""
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
        <head>
            <meta charset="utf-8">
            <title>Ticket Created</title>
            <link rel="stylesheet" href="/static/css/master.css">
            <link rel="icon" href="/static/images/default.png">
        </head>
        <body>
            <h1>Your Ticket : {tiketnum} has successfully been created on {datetime.datetime.now()}</h1>
            <h2>An email has been sent to : {tiketemail} with further details.</h2>
            <h2>Upload any files about your problem <a href='https://pretoriusse1.sharepoint.com/sites/Support/Shared%20Documents/Forms/AllItems.aspx'>here</a>. Save it as Ticket and what error.</h2>
            <br>
            <br>
            <h2>Format (ticket)(error)</h2>
            <br>
            <h3>e.g R3PPlexError.png</h3>
            <h3>Yours would be like : {tiketnum}(error).exetention</h3>
        </body>
    </html>""")


@app.route("/track.html", methods=['get', 'post'])
def trackhtml():
    return render_template("track.html")


@app.route('/track', methods=['get', 'post'])
def track():
    for key, value in request.form.items():
        if key == "ticketnum":
            tiketnum = value
        try:
            server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                        host='db1.pretoriusse.net', port='5432', database='Helpdesk')
            s1cursor = server_1.cursor()
            postgreSQL_select_Query = f"SELECT * FROM OPEN WHERE ticketnum = '{tiketnum}';"
            s1cursor = server_1.cursor()
            s1cursor.execute(postgreSQL_select_Query)
            ticket = s1cursor.fetchall()
            if ticket:
                return (f"""
        <!DOCTYPE html>
        <html lang="en" dir="ltr">
            <head>
                <meta charset="utf-8">
                <title>Ticket Open</title>
                <link rel="stylesheet" href="/static/css/master.css">
                <link rel="icon" href="/static/images/default.png">
            </head>
            <body>
                <h1>Your Ticket : {tiketnum} has successfully been found as open.</h1>
                <br>
                <h2>Support hasn't had time to look at your ticket yet.</h2>
            </body>
        </html>""")
            else:
                try:
                    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')
                    s1cursor = server_1.cursor()
                    postgreSQL_select_Query = f"SELECT * FROM in_progress WHERE ticketnum = '{tiketnum}';"
                    s1cursor = server_1.cursor()
                    s1cursor.execute(postgreSQL_select_Query)
                    ticket = s1cursor.fetchall()
                    if ticket:
                        return (f"""
                            <!DOCTYPE html>
                            <html lang="en" dir="ltr">
                                <head>
                                    <meta charset="utf-8">
                                    <title>Ticket In Progress</title>
                                    <link rel="stylesheet" href="/static/css/master.css">
                                    <link rel="icon" href="/static/images/default.png">
                                </head>
                                <body>
                                    <h1>Your Ticket : {tiketnum} has successfully been found as in progress.</h1>
                                    <br>
                                    <h2>Support is look at your ticket.</h2>
                                </body>
                            </html>""")
                    else:
                        try:
                            server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                                        host='db1.pretoriusse.net', port='5432', database='Helpdesk')
                            s1cursor = server_1.cursor()
                            postgreSQL_select_Query = f"SELECT CAST(date_closed) FROM date_closed WHERE ticketnum = '{tiketnum}';"
                            s1cursor = server_1.cursor()
                            s1cursor.execute(postgreSQL_select_Query)
                            date_closed = s1cursor.fetchall()
                            if date_closed:
                                date_closed = str(date_closed).replace("[(", "")
                                return (f"""
                                <!DOCTYPE html>
                                <html lang="en" dir="ltr">
                                    <head>
                                        <meta charset="utf-8">
                                        <title>Ticket Created</title>
                                        <link rel="stylesheet" href="/static/css/master.css">
                                        <link rel="icon" href="/static/images/default.png">
                                    </head>
                                    <body>
                                        <h1>Your Ticket : {tiketnum} has successfully been found as closed.</h1>
                                        <br>
                                        <h2>Support has marked your ticket as closed on {date_closed}.</h2>
                                    </body>
                                </html>""")
                            else:
                                return (f"""
                                        <!DOCTYPE html>
                                            <html lang="en" dir="ltr">
                                                <head>
                                                    <meta charset="utf-8">
                                                    <title>Ticket Created</title>
                                                    <link rel="stylesheet" href="/static/css/master.css">
                                                    <link rel="icon" href="/static/images/default.png">
                                                </head>
                                                <body>
                                                    <h1>Your ticket : {tiketnum} has not been found.</h1>
                                                </body>
                                            </html>""")
                        except psycopg2.Error:
                            return (f"""
                                <!DOCTYPE html>
                                <html lang="en" dir="ltr">
                                    <head>
                                        <meta charset="utf-8">
                                        <title>Ticket Created</title>
                                        <link rel="stylesheet" href="/static/css/master.css">
                                        <link rel="icon" href="/static/images/default.png">
                                    </head>
                                    <body>
                                        <h1>Your ticket : {tiketnum} has not been found.</h1>
                                    </body>
                                </html>""")
                        finally:
                            a = 0
                finally:
                    a = 0
        finally:
            a = 0


@app.errorhandler(404)
def error_404(er):
    """Page not found."""
    return render_template("404.html")


@app.route("/forgot", methods=["post", "get"])
def forgot():
    return render_template("forgot.html")


@app.route("/forgottenpassword", methods=["post", "get"])
def forgotten():
    global resetlink
    for key, value in request.form.items():
        if key == "Email":
            remail = value
    try:
        server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                    host='db1.pretoriusse.net', port='5432', database='Authentication')
        s1cursor = server_1.cursor()
        s1cursor.execute(f"SELECT email FROM website WHERE email = '{remail}';")
        email = s1cursor.fetchall()
        if len(email) > 0:
            resetlink = str(random.randrange(10000, 100000))
            print(resetlink)
            emailresetlink = f"http://helpdesk.pretoriusse.net/{resetlink}"
            print(emailresetlink)
            mailreset(names[remail], remail, emailresetlink)
            cwd = os.getcwd()
            approute = open('approute.config', "w+")
            approute.seek(0)
            approute.close()
            approute.write(resetlink)
            os.system(f'cd "{cwd}"')
            os.system('python add_approute.py')
            sys.exit()
    finally:
        return (f"""
            <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>Recieved forgot password Reset</title>
        <link rel="stylesheet" href="/static/css/login.css">
        <link rel="icon" href="/static/images/default.png">
      </head>
      <body>
        <h1>If {remail} is in our records we will send you a email link to reset your password.</h1>
      </body>
    </html>
            """)


@app.route(f'/{str(resetlink)}')
def resetuserpass():
    return (f"""
                    <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>Reset Password</title>
        <link rel="stylesheet" href="/static/css/login.css">
        <link rel="icon" href="/static/images/default.png">
      </head>
      <body>
        <form class="frm" action="/resetpassword" method="post">
          <br>
          <input type="text" class="edit" name="Email" value"{email}">
          <br>
          <br>
          <input type="text" class="edit" name="Newpassword"  placeholder="New password">
          <br>
          <input type="text" class="edit" name="Newpassword1" placeholder="New password">
          <br>
          <br>
          <input type="submit" class="edit" name="" value="Reset Password" style='font'>
          <br>
        </form>
        <br>
        <br>
      </body>
    </html>""")


def run():
    global resetlink
    app.run(debug="true", port=81, host='0.0.0.0')


if __name__ == "__main__":
    run()

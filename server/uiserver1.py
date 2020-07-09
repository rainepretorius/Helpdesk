import os
import re
import smtplib
import datetime
import psycopg2
from flask import Flask, render_template, request
import random
from Encryption import encrypt
import pymsteams

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


def teams_new_user(enteredemail, enteredpassword, name):
    myTeamsMessage = pymsteams.connectorcard(
        "https://outlook.office.com/webhook/24fc7b72-425b-4860-b462-3fa49f413874@c4131197-dd20-4fcf-8a1b-22639884c728/IncomingWebhook/d5c4297ca2894c5f98fe40aab766f43b/96016278-e391-4907-ba76-21c05da22b86")
    myTeamsMessage.text(
        f"New user with name : {name}. Their email is : {enteredemail} and their password is : {enteredpassword}")
    myTeamsMessage.send()


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
    gmail_user = 'email'
    gmail_app_password = 'thepassword'
    recipientlist = ['raine.pretorius@pretoriusse.net', 'charl.botha@pretoriusse.net', 'tech@pretoriusse.net']
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Create new User.\n
    Hi Raine and Charl,

    Please create new user in the website table. The email is : {enteredemail}.   The password is {enteredpassword}.   The name of the user is {name}.

    Kind Regards,
    Python Support Bot.
    """
    teams_new_user(enteredemail,enteredpassword, name)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()


def mailreset(name, email_recipient, link):
    """
    DOCSTRING : Sends an email to reset a password.
    :param link: Link to reset password
    :param enteredemail: Email entered into form
    :param name: name of the user.
    """
    # =============================================================================
    # SET EMAIL LOGIN REQUIREMENTS
    # =============================================================================
    gmail_user = 'email'
    gmail_app_password = 'thepassword'
    recipientlist = ['raine.pretorius@pretoriusse.net', email_recipient]
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Reset Forgotten Password.\n
    Hi {name},

    We recieved a request to reset your password. Click the link below.
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
    server_1 = psycopg2.connect(user='username', password='thepassword',
                                host='server', port='XXXX', database='Authentication')
    s1cursor = server_1.cursor()
    sqlcheck = f"SELECT PASSWORD FROM website WHERE email = '{email.lower()}'"
    s1cursor.execute(sqlcheck)
    sqlpassword = s1cursor.fetchall()
    sqlpassword = encrypt.decrypt(sqlpassword)
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
        print(names[email])
        for i in file:
            headinglist.append(i)
        headinglist[25] = f'    <h1>Hello {names[email]}.</h1>\n'
        htmltemplate = open(f"templates\{location}", "w+")
        for j in headinglist:
            if j not in htmltemplate.readline():
                htmltemplate.writelines(j)
        htmltemplate.close()
        server_1 = psycopg2.connect(user='username', password='thepassword',
                                    host='server', port='XXXX', database='Helpdesk')
        s1cursor = server_1.cursor()
        query = f"""
        SELECT ticketnum, date_opened, email FROM open WHERE email = '{email}'"""
        s1cursor.execute(query)
        result = s1cursor.fetchall()
        return render_template(location, data=result)
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
    :return: Rendered reset.html
    """
    return render_template('reset.html')


@app.route("/resetpassword", methods=['Get', 'Post'])
def change_password():
    """
    DOCSTRING : used to update user's password from helpdesk.
    :return:
    """
    for key, value in request.form.items():
        if key == "Email":
            pemail = value
        elif key == "Password":
            ppassword = value
        elif key == 'Newpassword':
            pnewpassword = value
        elif key == "Newpassword1":
            pnewpassword1 = value
    server_1 = psycopg2.connect(user='username', password='thepassword',
                                host='server', port='XXXX', database='Authentication')
    s1cursor = server_1.cursor()
    s1cursor.execute(f"SELECT password FROM website WHERE email = '{pemail}'")
    sqlpass = s1cursor.fetchall()
    sqlpass = str(sqlpass).replace("[('", "").replace("',)]", "")
    sqlpass = encrypt.decrypt(sqlpass)
    if ppassword == sqlpass:
        updatepassword = encrypt.encrypt(pnewpassword)
        s1cursor.execute(f"UPDATE WEBSITE SET password = '{updatepassword}' WHERE email = '{pemail}'")
        server_1.commit()
        s1cursor.close()
        server_1.close()
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


@app.route("/resetpasswordmail", methods=['Get', 'Post'])
def change_password_mail():
    """
    DOCSTRING : Used to reset the users password.
    :return:
    """
    for key, value in request.form.items():
        if key == "Email":
            pemail = value
        elif key == 'Newpassword':
            pnewpassword = value
    server_1 = psycopg2.connect(user='username', password='thepassword',
                                host='server', port='XXXX', database='Authentication')
    s1cursor = server_1.cursor()
    newpassword = encrypt.encrypt(pnewpassword)
    s1cursor.execute(f"UPDATE WEBSITE SET password = '{newpassword}' WHERE email = '{pemail}'")
    server_1.commit()
    s1cursor.close()
    server_1.close()
    return (f"""
        <html lang="en" dir="ltr">
            <head>
                <meta charset="utf-8">
                <title>We changed your password</title>
                <link rel="stylesheet" href="/static/css/master.css"> 
                <link rel="icon" href="/static/images/profile.png">
            </head>
            <body>
                <h1>Hello {names[pemail]}.</h1>
                <p>Your password has been changed to : {pnewpassword}.</p>
                <br>
                <a href="/"><p class="edit">Click here to log in.</p></a>
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
    server_1 = psycopg2.connect(user='username', password='thepassword',
                                host='server', port='XXXX', database='Helpdesk')
    s1cursor = server_1.cursor()
    postgreSQL_select_Query = f"SELECT help_id FROM OPEN ORDER BY help_id DESC LIMIT 1;"
    s1cursor = server_1.cursor()
    s1cursor.execute(postgreSQL_select_Query)
    pid = s1cursor.fetchall()
    pid = str(pid).replace("[(", "").replace(",)]", "")
    uid = int(pid) + 1
    tiketnum = f"{names[tiketemail][0]}{uid}P"
    sqlupdate = f"INSERT INTO open(help_id, ticketnum, date_opened, email, comments, in_progress) VALUES({uid}, '{tiketnum}', NOW(), '{tiketemail}', '{comments}', False);"
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
            server_1 = psycopg2.connect(user='username', password='thepassword',
                                        host='server', port='XXXX', database='Helpdesk')
            s1cursor = server_1.cursor()
            postgreSQL_select_Query = f"SELECT * FROM OPEN WHERE ticketnum = '{tiketnum}';"
            inpquery = f"SELECT in_progress FROM OPEN WHERE ticketnum = '{tiketnum}';"
            s1cursor.execute(inpquery)
            in_progress = s1cursor.fetchall()
            in_progress = str(in_progress).replace("[(", "").replace(",)]", "").capitalize()
            s1cursor = server_1.cursor()
            s1cursor.execute(postgreSQL_select_Query)
            ticket = s1cursor.fetchall()
            print(f"This is in_progress : {in_progress}")
            if ticket and (in_progress == 'False' or in_progress == 'false'):
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
                    server_1 = psycopg2.connect(user='username', password='thepassword',
                                                host='server', port='XXXX', database='Helpdesk')
                    s1cursor = server_1.cursor()
                    postgreSQL_select_Query = f"SELECT closed FROM in_progress WHERE ticketnum = '{tiketnum}';"
                    s1cursor = server_1.cursor()
                    s1cursor.execute(postgreSQL_select_Query)
                    ticket = s1cursor.fetchall()
                    closedq = f"SELECT closed FROM in_progress WHERE ticketnum = '{tiketnum}';"
                    s1cursor.execute(closedq)
                    closed = s1cursor.fetchall()
                    closed= str(closed).replace("[(", "").replace(",)]", "").capitalize()
                    print(f"This is closed : {closed}")
                    if not ticket and (closed == 'False'or closed =='false'):
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
                                    <h2>Support is looking at your ticket.</h2>
                                </body>
                            </html>""")
                    else:
                        try:
                            server_1 = psycopg2.connect(user='username', password='thepassword',
                                                        host='server', port='XXXX', database='Helpdesk')
                            s1cursor = server_1.cursor()
                            s1cursor = server_1.cursor()
                            postgreSQL_select_Query = f"SELECT CAST(date_closed) FROM closed WHERE ticketnum = '{tiketnum}';"
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
                                        <title>Ticket not found</title>
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
        server_1 = psycopg2.connect(user='username', password='thepassword',
                                host='server', port='XXXX', database='Authentication')
        s1cursor = server_1.cursor()
        s1cursor.execute(f"SELECT * FROM website WHERE email = '{remail}';")
        femail = s1cursor.fetchall()
        print(femail)
        if len(femail) > 0:
            resetlink = str(random.randrange(10000, 100000))
            emailresetlink = f"https://helpdesk.pretoriusse.net/{resetlink}"
        print(f"Full resetlink : {emailresetlink}")
        mailreset(name=names[remail], email_recipient=remail, link=emailresetlink)
        cwd = os.getcwd()
        approute = open('../approute.config', "w+")
        approute.seek(0)
        approute.writelines(resetlink)
        approute.close()
        if os.path.isfile('../email.config'):
            os.remove('../email.config')
        emailconf = open('../email.config', "w+")
        emailconf.write(remail)
        emailconf.close()
        py = "add_approute.py"
        os.system(f'python "{cwd}\{py}"')
    finally:
        a = 0
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
                                                        </html>""")


@app.route("/4")
def resetuserpass():
    if os.path.isfile('../email.config'):
        emailconf = open("../email.config")
        resetemail = emailconf.readline()
        emailconf.close()
    else:
        resetemail = 'john.doe@pretoriusse.net'
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
        <form class="frm" action="/resetpasswordmail" method="post">
          <br>
          <input type="text" class="edit" name="Email" value="{resetemail}">
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
    app.run(host="0.0.0.0", port=XXXX, debug=True, ssl_context=('certificate.crt', 'private.key'))


if __name__ == "__main__":
    run()

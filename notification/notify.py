import psycopg2
import smtplib
import os
from datetime import datetime

ticket_id = []
status = None
last_id = None
ticket_dict = {}
names = {'francopret@gmail.com': 'Franco', 'franco.pretorius@pretoriusse.net': 'Franco',
         'franco.pretorius@psg.co.za': 'Franco', 'heliztap@gmail.com': 'Helizta', 'heyssen@consol.co.za': 'Helizta',
         'helizta.pretorius@pretoriusse.net': 'Helizta', 'lorrein.pretorius@gmail.com': 'Lorrein',
         'lorrein.pretorius@pretoriusse.net': 'Lorrein', 'lorrein.pretorius@icloud.com': 'Lorrein',
         'liam.pretorius@pretoriusse.net': 'Liam', 'liam.pretorius2@gmail.com': 'Liam', 'liamp@orban.co.za': 'Liam',
         'liam.pretorius2@outlook.com': 'Liam', 'raine.pretorius1@gmail.com': 'Raine',
         'raine.pretorius@pretoriusse.net': 'Raine', 'ruddieprettie@gmail.com': 'Rudolph',
         'rudolph.pretorius@pretoriusse.net': 'Rudolph', 'sileziap@gmail.com': 'Silezia',
         'silezia.pretorius@pretoriusse.net': 'Silezia', 'spretorius@consol.co.za': 'Silezia',
         'tekara.pretorius@pretoriusse.net': 'Tekara', 'tekarahelizta@gmail.com': 'Tekara', 'info@pretoriusse.net': 'Info'}


def get_tiketnum():
    global ticket_id
    global last_id

    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')

    s1cursor = server_1.cursor()
    postgreSQL_select_Query = f"SELECT help_id FROM OPEN;"
    s1cursor.execute(postgreSQL_select_Query)
    weird = s1cursor.fetchall()
    sql_ans = str(weird).replace("(", "").replace(")", "").replace(",,", ",").replace(",]", "").replace("[",
                                                                                                        "").replace("]",
                                                                                                                    "")
    final = sql_ans.split(',')
    for i in final:
        try:
            i = int(i)
            if i not in ticket_id:
                ticket_id.append(i)
        except ValueError as er:
            errort = open('error', "w+")
            errort.write(str(er))
            errort.close()


def get_status():
    global ticket_id
    global status
    global ticket_dict
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')

    s1cursor = server_1.cursor()
    for i in ticket_id:
        i = int(i)
        postgreSQL_select_Query = f"SELECT closed FROM OPEN WHERE help_id = {i};"
        s1cursor.execute(postgreSQL_select_Query)
        weird = s1cursor.fetchall()
        tic_status = str(weird).replace("[(", "").replace(",)]", "")
        if i not in ticket_dict:
            ticket_dict[i] = tic_status


def check_new():
    global ticket_id
    global last_id
    global status
    global ticket_dict
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')
    postgreSQL_select_Query = f"SELECT help_id FROM OPEN ORDER BY help_id DESC LIMIT 1;"
    s1cursor = server_1.cursor()
    s1cursor.execute(postgreSQL_select_Query)
    pid = s1cursor.fetchall()
    pid = str(pid).replace("[(", "").replace(",)]", "")
    uid = int(pid)
    try:
        if pid != last_id and ticket_dict[uid] == 'False':
            s1cursor.execute(f"SELECT email FROM OPEN WHERE help_id = {pid}")
            email = s1cursor.fetchall()
            email = str(email).replace("[('", "").replace("',)]", "").replace("'", "")
            s1cursor.execute(f"SELECT comments FROM OPEN WHERE help_id = {pid}")
            comments = s1cursor.fetchall()
            comments = str(comments).replace("[(", "").replace(",)]", "")
            s1cursor.execute(f"SELECT ticketnum FROM OPEN WHERE help_id = {pid}")
            ticketnum = s1cursor.fetchall()
            ticketnum = str(ticketnum).replace("[(", "").replace(",)]", "")
            s1cursor.execute(f"SELECT CAST(date_opened AS DATE) FROM OPEN WHERE help_id = {pid}")
            opened = s1cursor.fetchall()
            name = names[email]
            send_mail_new(name, email, ticketnum, comments, opened)
    except KeyError as error:
        key = open('keyerror.txt', "w+")
        key.write(str(error))
        key.close()
    finally:
        last_id = pid
        last_id_save = open('../last_id', "w+")
        last_id_save.write(str(last_id))
        last_id_save.close()


def send_mail_closed(name, email, tickets_id):
    # =============================================================================
    # SET EMAIL LOGIN REQUIREMENTS
    # =============================================================================
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    recipientlist = [email, 'raine.pretorius@pretoriusse.net', 'charl.botha@pretoriusse.net', 'tech@pretoriusse.net']
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Ticket: {tickets_id} closed.\n
    Hi {name},
    Your ticket : {tickets_id} has been closed. Please check if the ploblem is resolved.

    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()




def send_mail_new(name, email, new_ticket_id, comments, date_opened):
    date_opened = str(date_opened).replace("[(datetime.date(", "").replace(",", "/").replace(")/)]", "")
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    recipientlist = [email, 'raine.pretorius@pretoriusse.net', 'charl.botha@pretoriusse.net', 'tech@pretoriusse.net']
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: We recieved ticket: {new_ticket_id} opened on: {date_opened}\n
    Hi {name},
    We have recieved your ticket with id : {new_ticket_id} that was opened on {date_opened}.  Raine or Charl will take a look ASAP. Your comments about the problem were : 
    
    {comments}
    
    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()


def check_inprogress():
    global ticket_dict
    global ticket_id
    global status
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')
    s1cursor = server_1.cursor()
    for i in ticket_id:
        status = ticket_dict[i]
        if status.capitalize() == 'True':
            s1cursor.execute(f"SELECT email FROM OPEN WHERE help_id = {i}")
            email = s1cursor.fetchall()
            email = str(email).replace("[('", "").replace("',)]", "").replace("'", "")
            s1cursor.execute(f"SELECT CAST(date_opened AS DATE) FROM OPEN WHERE help_id =  {i}")
            date_opened = s1cursor.fetchall()
            date_opened = str(date_opened).replace("[(datetime.date(", "").replace(",", "/").replace(")/)]", "")
            s1cursor.execute(f"SELECT ticketnum FROM OPEN WHERE help_id = {i}")
            ticketnum = s1cursor.fetchall()
            ticketnum = str(ticketnum).replace("[(", "").replace(",)]", "")
            name = names[email]
            send_mail_closed(name, email, ticketnum)
            ticket_dict[i] = ''
            sql_update1 = f"""INSERT INTO inprogress(help_id, ticketnum, date_opened, email) 
            VALUES({i}, {ticketnum}, '{date_opened.replace("/ ", "-")}', '{email}') """
            s1cursor.execute(sql_update1)
            server_1.commit()
            sqldelete = f"DELETE FROM OPEN WHERE help_id = {i}"
            s1cursor.execute(sqldelete)
            ticket_dict[i] = ""


def check_closed():
    global ticket_dict
    global ticket_id
    global status
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')
    s1cursor = server_1.cursor()
    for i in ticket_id:
        status = ticket_dict[i]
        if status.capitalize() == 'True':
            s1cursor.execute(f"SELECT email FROM OPEN WHERE help_id = {i}")
            email = s1cursor.fetchall()
            email = str(email).replace("[('", "").replace("',)]", "").replace("'", "")
            s1cursor.execute(f"SELECT CAST(date_opened AS DATE) FROM OPEN WHERE help_id =  {i}")
            date_opened = s1cursor.fetchall()
            date_opened = str(date_opened).replace("[(datetime.date(", "").replace(",", "/").replace(")/)]", "")
            s1cursor.execute(f"SELECT ticketnum FROM OPEN WHERE help_id = {i}")
            ticketnum = s1cursor.fetchall()
            ticketnum = str(ticketnum).replace("[(", "").replace(",)]", "")
            name = names[email]
            send_mail_closed(name, email, ticketnum)
            ticket_dict[i] = ''
            sql_update1 = f"""INSERT INTO inprogress(help_id, ticketnum, date_opened, email) 
                VALUES({i}, {ticketnum}, '{date_opened.replace("/ ", "-")}', '{email}') """
            s1cursor.execute(sql_update1)
            sqldelete = f"DELETE FROM OPEN WHERE help_id = {i}"
            s1cursor.execute(sqldelete)
            ticket_dict[i] = ""


if os.path.isfile('../last_id'):
    file = open('../last_id')
    last_id = file.read()
    file.close()

while True:
    get_tiketnum()
    get_status()
    check_new()
    check_inprogress()
    check_closed()

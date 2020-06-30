import psycopg2
import smtplib
import os
from datetime import datetime
import pymsteams

ticket_id = []
ticket_id1 = []
status = None
status1 = None
last_id = None
last_id1 = None
ticket_dict = {}
ticket_dict1 = {}
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


def get_tiketnum_open():
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


def get_status_open():
    global ticket_id
    global status
    global ticket_dict
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')

    s1cursor = server_1.cursor()
    for i in ticket_id:
        i = int(i)
        postgreSQL_select_Query = f"SELECT in_progress FROM OPEN WHERE help_id = {i};"
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
            send_teams_new(ticketnum, comments, opened)
    except KeyError as error:
        key = open('keyerror.txt', "w+")
        key.write(f"{datetime.now()} - {str(error)}")
        key.close()
    finally:
        last_id = pid
        last_id_save = open('../last_id', "w+")
        last_id_save.write(str(last_id))
        last_id_save.close()


def send_mail_new(name, email, new_ticket_id, comments, date_opened):
    date_opened = str(date_opened).replace("[(datetime.date(", "").replace(",", "/").replace(")/)]", "")
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    msg = f"""From: {gmail_user}
    To: {email}\n
    Subject: We recieved ticket: {new_ticket_id} opened on: {date_opened}\n
    Hi {name},
    We have recieved your ticket with id : {new_ticket_id} that was opened on {date_opened}. My support technicians will be in contact with the system engineers. 
    Your comments about the problem were : 
    
    {comments}
    
    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user,email, msg)
    server.quit()


def send_mail_in_progress(name, email, ticket_id):
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    recipientlist = [email, 'raine.pretorius@pretoriusse.net', 'charl.botha@pretoriusse.net', 'tech@pretoriusse.net']
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Ticket: {ticket_id} In Progress\n
    Hi {name},
    
    One of the Support technicians is looking at your ticket : {ticket_id}.

    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()


def send_mail_closed(name, email, tickets_id, date_closed):
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

    One of my support technicians has marked your ticket : {tickets_id} as closed on {date_closed}.
    Please check if the problem has been resolved.

    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()


def check_in_progress():
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
            send_mail_in_progress(name, email, ticketnum)
            ticket_dict[i] = None
            sql_update1 = f"""INSERT INTO in_progress(help_id, ticketnum, date_opened, email) 
                    VALUES({i}, {ticketnum}, '{date_opened.replace("/ ", "-")}', '{email}') """
            s1cursor.execute(sql_update1)
            sqldelete = f"DELETE FROM OPEN WHERE help_id = {i}"
            s1cursor.execute(sqldelete)
            ticket_dict[i] = None


def check_closed():
    global ticket_dict1
    global ticket_id1
    global status1
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')
    s1cursor = server_1.cursor()
    for i in ticket_id1:
        status1 = ticket_dict1[i]
        if status1.capitalize() == 'True':
            s1cursor.execute(f"SELECT email FROM in_progress WHERE help_id = {i}")
            email = s1cursor.fetchall()
            email = str(email).replace("[('", "").replace("',)]", "").replace("'", "")
            s1cursor.execute(f"SELECT CAST(date_opened AS DATE) FROM OPEN WHERE help_id =  {i}")
            date_opened = s1cursor.fetchall()
            date_opened = str(date_opened).replace("[(datetime.date(", "").replace(",", "/").replace(")/)]", "")
            s1cursor.execute(f"SELECT ticketnum FROM OPEN WHERE help_id = {i}")
            ticketnum = s1cursor.fetchall()
            ticketnum = str(ticketnum).replace("[(", "").replace(",)]", "")
            name = names[email]
            ticket_dict1[i] = None
            sql_update1 = f"""INSERT INTO closed(help_id, ticketnum, date_opened, date_closed, email) 
                    VALUES({i}, {ticketnum}, '{date_opened.replace("/ ", "-")}', {datetime.now()}, '{email}') """
            s1cursor.execute(sql_update1)
            sqldelete = f"DELETE FROM in_progress WHERE help_id = {i}"
            s1cursor.execute(sqldelete)
            ticket_dict[i] = None
            send_mail_closed(name, email, ticketnum, datetime.now())


def get_tiketnum_in_progress():
    global ticket_id1
    global last_id1

    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')

    s1cursor = server_1.cursor()
    postgreSQL_select_Query = f"SELECT help_id FROM in_progress;"
    s1cursor.execute(postgreSQL_select_Query)
    weird = s1cursor.fetchall()
    sql_ans = str(weird).replace("(", "").replace(")", "").replace(",,", ",").replace(",]", "").replace("[",
                                                                                                        "").replace("]",
                                                                                                                    "")
    final = sql_ans.split(',')
    for i in final:
        try:
            i = int(i)
            if i not in ticket_id1:
                ticket_id1.append(i)
        except ValueError as er:
            errort = open('error', "w+")
            errort.write(str(er))
            errort.close()


def get_status_in_progress():
    global ticket_id1
    global status1
    global ticket_dict1
    server_1 = psycopg2.connect(user='Python', password='VVd%MBK0i@8#86GJibThMi2sE&e*tb',
                                host='db1.pretoriusse.net', port='5432', database='Helpdesk')

    s1cursor = server_1.cursor()
    for i in ticket_id1:
        i = int(i)
        postgreSQL_select_Query = f"SELECT in_progress FROM OPEN WHERE help_id = {i};"
        s1cursor.execute(postgreSQL_select_Query)
        weird = s1cursor.fetchall()
        tic_status1 = str(weird).replace("[(", "").replace(",)]", "")
        if i not in ticket_dict1:
            ticket_dict1[i] = tic_status1

def send_teams_new(ticketnumber,comments1,opened1):
    myTeamsMessage = pymsteams.connectorcard("https://outlook.office.com/webhook/24fc7b72-425b-4860-b462-3fa49f413874@c4131197-dd20-4fcf-8a1b-22639884c728/IncomingWebhook/d5c4297ca2894c5f98fe40aab766f43b/96016278-e391-4907-ba76-21c05da22b86")
    myTeamsMessage.text(f"New Ticket with ticketnumber {ticketnumber} has been created. It was opened on {opened1}.\nThe comments were : \n{comments1}")
    myTeamsMessage.send()


def run():
    while True:
        get_tiketnum_open()
        get_status_open()
        check_new()
        check_in_progress()
        get_tiketnum_in_progress()
        get_status_in_progress()
        check_closed()


if __name__ == "__main__":
    run()
import smtplib

def send_up():
    # =============================================================================
    # SET EMAIL LOGIN REQUIREMENTS
    # =============================================================================
    gmail_user = 'pretoriusspprt@gmail.com'
    gmail_app_password = 'ybfmeopuajmexkwd'
    recipientlist = ['raine.pretorius@pretoriusse.net', 'charl.botha@pretoriusse.net', 'tech@pretoriusse.net', 'technical@pretoriusse.net']
    msg = f"""From: {gmail_user}
    To: {", ".join(recipientlist)}\n
    Subject: Helpdesk is up..\n
    Hi Raine and Charl,

    The helpdesk app is up and running.

    Kind Regards,
    Python Support Bot.
    """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, ', '.join(recipientlist), msg)
    server.quit()
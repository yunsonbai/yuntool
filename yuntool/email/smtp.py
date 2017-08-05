#!/usr/bin/env python
# coding:utf8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from email.MIMEImage import MIMEImage
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.header import Header
from email.encoders import encode_base64


def send_mail(from_user, from_user_passwd,
              to_users, subject, content, mail_server,
              mail_server_port='25', picture=None,
              picture_url=None, file=None, login=False):
    '''
    parameter:
        from_user: 'test@yunson.com'
        from_user_passwd: '*****'
        to_users: ['das@das.com', 'asdad@das.co']
        subject: 'dsaddsadasd'
        content:  'sssssd,dsda,ds'
        mail_server: mail.yunson.net
        picture: default None, to_users shoud give img file
        picture_url: picture_url
    '''

    msg = MIMEMultipart()
    msg['Subject'] = subject
    con = MIMEText('<b>{0}</b>'.format(content), 'html', 'utf-8')
    if file:
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(file.read())
        encode_base64(file_msg)
        file_msg.add_header(
            'Content-Disposition',
            'attachment', filename=file.name)
        msg.attach(file_msg)

    if picture:
        con = MIMEText(
            '<b>{0}</b><img alt="" src="cid:picture" />'.format(
                content), 'html', 'utf-8')
        msg.attach(con)
        img = MIMEImage(picture)
        img.add_header('Content-ID', 'picture')
        msg.attach(img)
    if picture_url:
        con = MIMEText(
            '<b>{0}</b><img alt="" src="{1}" />'.format(
                content, picture_url), 'html', 'utf-8')
        msg.attach(con)
    server = smtplib.SMTP(mail_server, mail_server_port)
    if login:
        server.login(from_user, from_user_passwd)
    msg['From'] = Header(from_user)
    str_to_users = ','.join(to_users)
    msg['To'] = Header(str_to_users)
    server.sendmail(from_user, to_users, msg.as_string())
    server.quit()

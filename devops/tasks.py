#!/usr/bin/python
#coding:utf-8 
 
import smtplib
from email.mime.text import MIMEText
import sys 
from celery import Celery,platforms

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')
platforms.C_FORCE_ROOT = True  

mail_host = 'smtp.163.com'
mail_user = '18878774260@163.com'
mail_pass = 'LUOhui123456'
mail_postfix = '163.com'


@celery.task
def sendMail(mailto,subject,body,format='plain'):
    if isinstance(body,unicode):
        body = str(body)
    me= mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(body,format,'utf-8')
    if not isinstance(subject,unicode):
        subject = unicode(subject)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = mailto
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, mailto, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False 

 
if __name__ == "__main__":
    sendMail(sys.argv[1], sys.argv[2], sys.argv[3])

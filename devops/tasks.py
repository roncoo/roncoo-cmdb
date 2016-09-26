#!/usr/bin/python
#coding:utf-8 
 
import smtplib
from email.mime.text import MIMEText
import sys,os 
from celery import Celery,platforms
import util

work_dir = os.path.dirname(os.path.realpath(__file__))
service_conf = os.path.join(work_dir, 'conf/service.conf')

config = util.get_config(service_conf, 'celery')

celery = Celery('tasks', broker=config['redis_host'])
platforms.C_FORCE_ROOT = True  

mail_host = config['mail_host']
mail_user = config['mail_user']
mail_pass = config['mail_pass']
mail_postfix = config['mail_postfix']


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

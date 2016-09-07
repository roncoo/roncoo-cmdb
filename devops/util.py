#!/bin/env python
# -*- encoding: utf-8 -*-

import os, os.path 
import time,json
import base64,glob
import hashlib
import traceback
import ConfigParser
import logging,logging.config

def get_config(service_conf, section=''):
    config = ConfigParser.ConfigParser()
    config.read(service_conf)

    conf_items = dict(config.items('common')) if config.has_section('common') else {}
    if section and config.has_section(section):
       conf_items.update(config.items(section))
    return conf_items

def write_log(loggername):
    work_dir = os.path.dirname(os.path.realpath(__file__))
    log_conf= os.path.join(work_dir, 'conf/logger.conf')
    logging.config.fileConfig(log_conf)
    logger = logging.getLogger(loggername)
    return logger


def get_validate(username, uid, role, fix_pwd):
    t = int(time.time())
    validate_key = hashlib.md5('%s%s%s' % (username, t, fix_pwd)).hexdigest() 
    return base64.b64encode('%s|%s|%s|%s|%s' % (username, t, uid, role, validate_key)).strip()

def validate(key, fix_pwd):
    t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|') 
    if len(x) != 5:
        write_log('api').warning("token参数数量不足")
        return json.dumps({'code':1,'errmsg':'token参数不足'})

    if t > int(x[1]) + 2*60*60:
        write_log('api').warning("登录已经过期")
        return json.dumps({'code':1,'errmsg':'登录已过期'})
    validate_key = hashlib.md5('%s%s%s' % (x[0], x[1], fix_pwd)).hexdigest()
    if validate_key == x[4]:
        write_log('api').info("api认证通过")
        return json.dumps({'code':0,'username':x[0],'uid':x[2],'r_id':x[3]})
    else:
        write_log('api').warning("密码不正确")
        return json.dumps({'code':1,'errmsg':'密码不正确'})
def check_name(name):
    if isinstance(name, str) or isinstance(name, unicode):
        return name.isalnum() and len(name) >= 2
    else:
        return False
   
def copy_file(name):
    inputFile = open("/var/lib/cobbler/kickstarts/demo.cfg","r")
    outputFile = open("/var/lib/cobbler/kickstarts/%s" %name,"a") 
    alllines = inputFile.readlines()
    for eachline in alllines:
	outputFile.write(eachline)
    inputFile.close()
    outputFile.close()

def write_file(name,para):
    with open('/var/lib/cobbler/kickstarts/%s'%name,'a+') as f:
        for k,v in para.items():
	    if k == "swap":
		line = "part %s --size=%s\n"%(k,v)
	    else:
                line = "part %s --fstype ext4 --size=%s\n"%(k,v)
            f.write(line)
	    addline = "%pre\n$SNIPPET('log_ks_pre')\n$SNIPPET('kickstart_start')\n$SNIPPET('pre_install_network_config')\n$SNIPPET('pre_anamon')\n%post\n%end\n"
	f.write(addline)	
def replace_url(name,url):
    with open('/var/lib/cobbler/kickstarts/%s'%name,'r') as r:
        lines=r.readlines()
    with open('/var/lib/cobbler/kickstarts/%s'%name,'w') as w:
        for l in lines:
            w.write(l.replace('urllist',url))

def graph_file(name):
    try:
        file = glob.glob(name+'/*') 
        for i in file:
	    os.remove(i)
    except:	
        return 1

def graph_img(name):
    try:
	ret = []
	file = glob.glob(name+'/*')
	for i in file:
	    ret.append(i.split("web")[1])
	return ret
    except:
	return ret

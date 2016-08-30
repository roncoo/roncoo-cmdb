#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util
from zabbix_api import *
#这里是关于用户角色的增删改查及组对应的权限id2name

@jsonrpc.method('zbhost.create')
@auth_login
def idc_create(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
	print data 
        if not util.check_name(data['name']):
            return json.dumps({'code': 1, 'errmsg': 'name must be string or int'})
        app.config['cursor'].execute_insert_sql('zbhost', data)
        util.write_log('api').info(username, "create idc %s scucess" %  data['name'])
        return json.dumps({'code':0,'result':'create idc %s scucess' % data['name']})
    except:
        util.write_log('api').error(username,"create idc error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create idc fail'})

@jsonrpc.method('zbhost.getlist')
@auth_login
def zbhost_select(auth_info,**kwargs):
    datadict = {}
    ret = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
	init()
	fields = ['id','cmdb_hostid','hostid','host','ip']
	zabbix_hosts = app.config['cursor'].get_results('zbhost', fields)
	hostid = [str(zb["cmdb_hostid"]) for zb in zabbix_hosts]
	server_hosts = app.config['cursor'].get_results('server',["id"])	
	for i in server_hosts:	 
	    if str(i["id"]) not in hostid:
		datadict["id"] = i["id"]		
		#all_host = app.config['cursor'].get_results('server',["ip"],datadict)
		get_ip = app.config['cursor'].get_where_results('server',["id","ip"],datadict)
		ret.append(get_ip[0])
                util.write_log('api').info(username, 'select zabbix list success')
	return json.dumps({'code':0, 'result':ret})
	
    except:
        util.write_log('api').error("select zabbixgroup list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'getzabbixgroup failed'})


@jsonrpc.method('zbhost_allhost.getlist')
@auth_login
def zbhost_allhost_select(auth_info,**kwargs):
    datalist = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        data = app.config['zabbix'].get_hosts()
	#print data
        return json.dumps({'code':0, 'result':data})
    except:
        util.write_log('api').error("select zabbixgroup list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get zabbixgroup failed'})

@jsonrpc.method('zbhost.update')
@auth_login
def idc_update(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no idc' })
    try:
        data = request.get_json()['params']
	print data
        where = data.get('where',None)
        data = data.get('data',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_update_sql('idc', data, where)
        if not result:
            return json.dumps({'code':1, 'errmsg':'result is  null'})
        util.write_log('api').info(username, 'update idc success!' )
        return json.dumps({'code':0,'result':'update idc scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update idc failed"})

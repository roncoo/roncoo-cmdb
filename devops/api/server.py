#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util
from datetime import date, datetime

#这里是关于用户角色的增删改查及组对应的权限id2name

@jsonrpc.method('server.create')
def server_create(**kwargs):
#    if auth_info['code'] == 1:
#        return json.dumps(auth_info)
#    username = auth_info['username']
    try:
        data = request.get_json()['params']
#        if not util.check_name(data['name']):
#            return json.dumps({'code': 1, 'errmsg': 'name must be string or int'})
	print data
        res = app.config['cursor'].execute_insert_sql('server', data)
	print res
#        util.write_log('api').info(username, "create server %s scucess" %  data['name'])
        return json.dumps({'code':0,'result':'create server  scucess'})
    except:
        util.write_log('api').error(username,"create server error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create server fail'})



@jsonrpc.method('server.radd')
def server_radd(**kwargs):
    try:
        data = request.get_json()['params']
	#查询是否含有mac_address
	where = {"mac_address":str(data['mac_address'])}
	fields = ['mac_address']
	result = app.config['cursor'].get_one_result('server', fields, where)
	if result:
	    res = app.config['cursor'].execute_update_sql('server', data, where)
            return json.dumps({'code':0,'result':'update server  scucess'})
	else:
	    res = app.config['cursor'].execute_insert_sql('server', data)
	    return json.dumps({'code':0,'result':'create server  scucess'})
    except:
        return json.dumps({'code':1,'errmsg':'create server fail'})


@jsonrpc.method('server.getlist')
@auth_login
def server_select(auth_info,**kwargs):
    data_result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        fields = ['id','hostname','ip','vm_status','st','uuid','manufacturers','server_type','server_cpu','os','server_disk','server_mem','mac_address','manufacture_date','check_update_time','server_purpose','server_run','expire','server_up_time','idc_id','cabinet_id','supplier','supplier_phone']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        res = app.config['cursor'].get_results('server', fields)
	for i in res: 
	    i['check_update_time'] = str(i['check_update_time'])
	    i['manufacture_date'] = str(i['manufacture_date'])
	    i['expire'] = str(i['expire'])
	    i['server_up_time'] = str(i['server_up_time'])
	    if i["idc_id"]:
	        idc = app.config['cursor'].get_one_result('idc', ['name'],{"id":int(i["idc_id"])})
	  	cabinet = app.config['cursor'].get_one_result('cabinet', ['name'],{"id":int(i["cabinet_id"])})
	        i['idc_name'] = str(idc['name'])
	        i['cabinet_name'] = str(cabinet['name'])
	        data_result.append(i)
	    else:
		data_result.append(i)
        util.write_log('api').info(username, 'select server list success')
        return json.dumps({'code':0,'result':data_result})
    except:
        util.write_log('api').error("select server list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get serverlist failed'})

@jsonrpc.method('server.get')
@auth_login
def server_get(auth_info, **kwargs):
    res = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        output = ['id','hostname','ip','vm_status','st','uuid','manufacturers','server_type','server_cpu','os','server_disk','server_mem','mac_address','manufacture_date','check_update_time','supplier','supplier_phone','idc_id','cabinet_id','cabinet_pos','expire','server_up_time','server_purpose','server_run','host']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].get_one_result('server', fields, where)
	result['check_update_time'] = str(result['check_update_time'])
	result['manufacture_date'] = str(result['manufacture_date'])
	result['expire'] = str(result['expire'])
	result['server_up_time'] = str(result['server_up_time'])
#	print result
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        else:
            util.write_log('api').info(username, "select server by id success")
            return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('select server by id error: %s'  % traceback.format_exc())
        return  json.dumps({'code':1,'errmsg':'get server failed'})

@jsonrpc.method('server.update')
@auth_login
def idc_update(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no server' })
    try:
        data = request.get_json()['params']
#	print data
        where = data.get('where',None)
        data = data.get('data',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_update_sql('server', data, where)
        if not result:
            return json.dumps({'code':1, 'errmsg':'result is  null'})
        util.write_log('api').info(username, 'update server success!' )
        return json.dumps({'code':0,'result':'update server scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update server failed"})

@jsonrpc.method('server.delete')
@auth_login
def idc_delete(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no idc' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_delete_sql('server', where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete server successed')
        return json.dumps({'code':0,'result':'delete server scucess'})
    except:
        util.write_log('api'). error('delete idc error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete server failed'}) 


#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util


#这里是关于用户角色的增删改查及组对应的权限id2name

@jsonrpc.method('switch.create')
@auth_login
def switch_create(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
#	print data
	data['cabinet']= int(data['cabinet'])
	data['idc'] = int(data['idc'])
	data['port'] = int(data['port'])
        app.config['cursor'].execute_insert_sql('switch', data)
        util.write_log('api').info(username, "create switch %s scucess" %  data['ip'])
        return json.dumps({'code':0,'result':'create switch %s scucess' % data['ip']})
    except:
        util.write_log('api').error(username,"create switch error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create switch fail'})

@jsonrpc.method('switch.getlist')
@auth_login
def switch_select(auth_info,**kwargs):
    data_result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        fields = ['id','ip','device','port','port','cabinet','idc']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        res = app.config['cursor'].get_results('switch', fields)
	for i in res:
	    if i['idc']:
		idc = app.config['cursor'].get_one_result('idc', ['name'],{"id":int(i["idc"])})
		cabinet = app.config['cursor'].get_one_result('cabinet', ['name'],{"id":int(i["cabinet"])})
                i['idc_name'] = str(idc['name'])
                i['cabinet_name'] = str(cabinet['name'])
		data_result.append(i)
	    else:
		data_result.append(i)
        util.write_log('api').info(username, 'select switch list success')
        return json.dumps({'code':0,'result':data_result})
    except:
        util.write_log('api').error("select switch list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get switch failed'})

@jsonrpc.method('switch.get')
@auth_login
def switch_get(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        output = ['id','ip','device','port','cabinet','idc']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where',None)
#	print where
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].get_one_result('switch', fields, where)
#	print result
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        else:
            util.write_log('api').info(username, "select role by id success")
            return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('select switch by id error: %s'  % traceback.format_exc())
        return  json.dumps({'code':1,'errmsg':'get switch failed'})

@jsonrpc.method('switch.update')
@auth_login
def switch_update(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no idc' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        data = data.get('data',None)
#	print where
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_update_sql('switch', data, where)
        if not result:
            return json.dumps({'code':1, 'errmsg':'result is  null'})
        util.write_log('api').info(username, 'update switch success!' )
        return json.dumps({'code':0,'result':'update switch scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update switch failed"})

@jsonrpc.method('switch.delete')
@auth_login
def switch_delete(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no switch' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_delete_sql('switch', where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete switch successed')
        return json.dumps({'code':0,'result':'delete switch scucess'})
    except:
        util.write_log('api'). error('delete switch error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete switch failed'}) 

@jsonrpc.method('switch.add')
def server_radd(**kwargs):
    try:
        data = request.get_json()['params']
#	print data
        #查询是否含有mac_address
        where = {"ip":str(data['ip'])}
        fields = ['ip']
        result = app.config['cursor'].get_one_result('switch', fields, where)
	idc_id_ret = app.config['cursor'].get_one_result('idc',['id'],{"id":int(data['idc'])})
	cabinet_id_ret = app.config['cursor'].get_one_result('cabinet',['id'],{"id":int(data['cabinet'])})
        if result and idc_id_ret and cabinet_id_ret:
            res = app.config['cursor'].execute_update_sql('switch', data, where)
            return json.dumps({'code':0,'result':'update switch  scucess'})
        if idc_id_ret and cabinet_id_ret:
            res = app.config['cursor'].execute_insert_sql('switch', data)
            return json.dumps({'code':0,'result':'create switch  scucess'})
	else:
	    return json.dumps({'code':1,'errmsg':'create switch fail, please check idcid or cabinet id'})
    except:
        return json.dumps({'code':1,'errmsg':'create switch fail'})

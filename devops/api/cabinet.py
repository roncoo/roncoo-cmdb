#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util


#这里是关于用户角色的增删改查及组对应的权限id2name

@jsonrpc.method('cabinet.create')
@auth_login
def idc_create(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
	check_name = str(data['name'])
##        if not util.check_name(check_name):
#            return json.dumps({'code': 1, 'errmsg': 'name must be string or int'})
        app.config['cursor'].execute_insert_sql('cabinet', data)
        util.write_log('api').info(username, "create cabinet %s scucess" %  data['name'])
        return json.dumps({'code':0,'result':'create cabinet %s scucess' % data['name']})
    except:
        util.write_log('api').error(username,"create cabinet error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create cabinet fail'})

@jsonrpc.method('cabinet.getlist')
@auth_login
def cabinet_select(auth_info,**kwargs):
    data_result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        fields = ['id','name','idc_id','power']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        res = app.config['cursor'].get_results('cabinet', fields)
	for i in res: 
	    where = {'id':int(i['idc_id'])}
	    result = app.config['cursor'].get_results('idc',['id','idc_name'],where)	
	    i["idc_name"] = result[0]['idc_name']
	    data_result.append(i)
        util.write_log('api').info(username, 'select cabinet list success')
        return json.dumps({'code':0,'result':data_result})
    except:
        util.write_log('api').error("select role list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get rolelist failed'})

@jsonrpc.method('cabinet.get')
@auth_login
def idc_get(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        output = ['id','name','idc_id','power']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].get_one_result('cabinet', fields, where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        else:
            util.write_log('api').info(username, "select cabinet by id success")
            return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('select idc by id error: %s'  % traceback.format_exc())
        return  json.dumps({'code':1,'errmsg':'get idc failed'})

@jsonrpc.method('cabinet.update')
@auth_login
def idc_update(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no idc' })
    try:
        data = request.get_json()['params']
#	print data
        where = data.get('where',None)
        data = data.get('data',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_update_sql('cabinet', data, where)
        if not result:
            return json.dumps({'code':1, 'errmsg':'result is  null'})
        util.write_log('api').info(username, 'update cabinet success!' )
        return json.dumps({'code':0,'result':'update cabinet scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update cabinet failed"})

@jsonrpc.method('cabinet.delete')
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
        result = app.config['cursor'].execute_delete_sql('cabinet', where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete cabinet successed')
        return json.dumps({'code':0,'result':'delete cabinet scucess'})
    except:
        util.write_log('api'). error('delete idc error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete cabinet failed'}) 


#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util


#这里是关于用户角色的增删改查及组对应的权限id2name

@jsonrpc.method('idc.create')
@auth_login
def idc_create(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
#	print data
        if not util.check_name(data['name']):
            return json.dumps({'code': 1, 'errmsg': 'name must be string or int'})
        app.config['cursor'].execute_insert_sql('idc', data)
        util.write_log('api').info(username, "create idc %s scucess" %  data['name'])
        return json.dumps({'code':0,'result':'create idc %s scucess' % data['name']})
    except:
        util.write_log('api').error(username,"create idc error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create idc fail'})

@jsonrpc.method('idc.getlist')
@auth_login
def idc_select(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        fields = ['id','name','idc_name','address','phone','email','user_interface','user_phone','rel_cabinet_num','pact_cabinet_num']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        res = app.config['cursor'].get_results('idc', fields)
        util.write_log('api').info(username, 'select idc list success')
        return json.dumps({'code':0,'result':res})
    except:
        util.write_log('api').error("select role list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get rolelist failed'})

@jsonrpc.method('idc.get')
@auth_login
def idc_get(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        output = ['id','name','idc_name','address','phone','email','user_interface','user_phone','rel_cabinet_num','pact_cabinet_num']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where',None)
#	print where
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].get_one_result('idc', fields, where)
#	print result
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        else:
            util.write_log('api').info(username, "select role by id success")
            return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('select idc by id error: %s'  % traceback.format_exc())
        return  json.dumps({'code':1,'errmsg':'get idc failed'})

@jsonrpc.method('idc.update')
@auth_login
def idc_update(auth_info, **kwargs):
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
        result = app.config['cursor'].execute_update_sql('idc', data, where)
        if not result:
            return json.dumps({'code':1, 'errmsg':'result is  null'})
        util.write_log('api').info(username, 'update idc success!' )
        return json.dumps({'code':0,'result':'update idc scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update idc failed"})

@jsonrpc.method('idc.delete')
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
        result = app.config['cursor'].execute_delete_sql('idc', where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete idc successed')
        return json.dumps({'code':0,'result':'delete idc scucess'})
    except:
        util.write_log('api'). error('delete idc error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete idc failed'}) 


#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util,datetime
from cobbler_api import *
# 权限的增删改查

@jsonrpc.method('cobbler.create')
@auth_login
def create(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params'] 
	print data
        app.config['cursor'].execute_insert_sql('cobbler', data)
        util.write_log('api').info(username, "create cobbler %s success"  %  data['ip'])
        return json.dumps({'code':0,'result':'create %s success' %  data['ip']})
    except:
        util.write_log('api').error('create cobbler error:%s' % traceback.format_exc())
        return json.dumps({'code':1,'errmsg': 'create cobbler failed'})

@jsonrpc.method('cobbler.delete')
@auth_login
def delete(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in  auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1,'errmsg':'must need a condition'})
	output = ['hostname']
        ret_data = app.config['cursor'].get_one_result('cobbler', output, where)
	ret = system_remove(app.config["cobbler_url"],app.config["cobbler_user"],app.config["cobbler_password"],str(ret_data['hostname'])) 
	if str(ret['result']) == "True":		
            result = app.config['cursor'].execute_delete_sql('cobbler', where) 
            util.write_log('api').info(username, "delete cobbler  success")
            return json.dumps({'code':0,'result':'delete cobbler success'})
    except:
        util.write_log('api').error("delete power error:%s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg': 'delete power failed'})

@jsonrpc.method('cobbler.getlist')
@auth_login
def getlist(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        output = ['id','ip','hostname','MAC','os','status']
        data = request.get_json()['params']
        fields = data.get('output', output)
        result = app.config['cursor'].get_results('cobbler', fields)
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':result,'count':len(result)})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get cobbler failed'})


@jsonrpc.method('cobbler_profile.getlist')
@auth_login
def profile_getlist(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
     	result = get_profile(app.config['cobbler_url'],app.config['cobbler_user'],app.config['cobbler_password'])  
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get cobbler failed'})


@jsonrpc.method('cobbler.get')
@auth_login
def getapi(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
	output = ['id','ip','hostname','MAC','os','status','gateway','subnet']
	data = request.get_json()['params']
	fields = data.get('output', output)
	where = data.get('where',None)		
	if not where:
	    return json.dumps({'code':1,'errmsg':'must need a condition'})
	result = app.config['cursor'].get_one_result('cobbler', fields, where)
	ret_system = system(app.config['cobbler_url'],app.config['cobbler_user'],app.config['cobbler_password'],result['hostname'],result['ip'],result['MAC'],result['os'],result['gateway'],result['subnet'])
	if str(ret_system['result']) != "True":
	    return json.dumps({'code':1,'errmsg':'please check your system name'})
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data_insert = {'ip':result['ip'],'os':result['os'],'install_time':now}
	ret = app.config['cursor'].execute_insert_sql('install', data_insert)
	up_date = app.config['cursor'].execute_update_sql('cobbler', {"status":1}, where)	
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':up_date})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get cobbler failed'})


@jsonrpc.method('up_cObbler.get')
@auth_login
def up_cobbler_api(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        output = ['id','ip','hostname','MAC','os','status','gateway','subnet']
        data = request.get_json()['params']	
        fields = data.get('output', output)
        where = data.get('where',None)
        result = app.config['cursor'].get_one_result('cobbler', fields, where)
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get cobbler failed'})


@jsonrpc.method('cobbler.update')
@auth_login
def cobbler_update(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cobbler' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        data = data.get('data',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
	data['os']=data['upos']
	data.pop('upos')
        result = app.config['cursor'].execute_update_sql('cobbler', data, where)
        if not result:
            return json.dumps({'code':1, 'errmsg':'result is  null'})
        util.write_log('api').info(username, 'update cobbler success!' )
        return json.dumps({'code':0,'result':'update cobbler scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update cobbler failed"})


@jsonrpc.method('install.getlist')
@auth_login
def install_getlist(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        output = ['id','ip','install_time','os']
	data_result = []
        data = request.get_json()['params']
        fields = data.get('output', output)
        result = app.config['cursor'].get_results('install', fields)
	for ret in result:
	    ret['install_time']=str(ret['install_time'])
	    data_result.append(ret)
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':data_result})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get install failed'})

@jsonrpc.method('cobbler_distro.getlist')
@auth_login
def distro_getlist(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        result = get_distro(app.config['cobbler_url'],app.config['cobbler_user'],app.config['cobbler_password'])
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get cobbler failed'})

@jsonrpc.method('cobbler_profile.create')
@auth_login
def create_profile(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
	para = eval(str(data["partion"]))
	name = data['profile']
	filename = str(name)
	util.copy_file(filename)
	util.write_file(filename,para)
	util.replace_url(filename,str(data['url']))
	ret = profile_create(app.config['cobbler_url'],app.config['cobbler_user'],app.config['cobbler_password'],filename,str(data['distro']),'/var/lib/cobbler/kickstarts/%s'%filename)
	print "xiaoluoge"
	
	print ret
	if str(ret['result']) == "True": 
	    data = {"distro":str(data['distro']),"os":filename,"ks":'/var/lib/cobbler/kickstarts/%s'%filename} 
	    app.config['cursor'].execute_insert_sql('profile', data)
	    util.write_log('api').info(username, "create cobbler profile %s success"  %filename)
	else:
	    util.write_log('api').info(username, "create cobbler profile %s faile"  %  data['ip'])
        return json.dumps({'code':0,'result':'create %s success' % filename})
    except:
        util.write_log('api').error('create cobbler error:%s' % traceback.format_exc())
        return json.dumps({'code':1,'errmsg': 'create cobbler failed'})

@jsonrpc.method('profile.getlist')
@auth_login
def profil_list(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        output = ['id','distro','os','ks']
        data = request.get_json()['params']
        fields = data.get('output', output)
        result = app.config['cursor'].get_results('profile', fields)
        util.write_log('api').info(username, 'select permission list success')
        return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get cobbler failed'})

@jsonrpc.method('cobbler_profile.delete')
@auth_login
def profile_delete(auth_info,**kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in  auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no power' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1,'errmsg':'must need a condition'})
	output = ['os']
	result = app.config['cursor'].get_one_result('profile', output, where)	
	ret = profile_remove(app.config["cobbler_url"],app.config["cobbler_user"],app.config["cobbler_password"],str(result['os']))	
	if str(ret['result']) == "True":
	    result = app.config['cursor'].execute_delete_sql('profile', where)
	    util.write_log('api').info(username, "delete profile  success")
            return json.dumps({'code':0,'result':'delete profile success'})
	else:
	    util.write_log('api').info(username, "delete profile  faild")
	    return json.dumps({'code':1,'errmsg': 'delete profile failed'})
    except:
        util.write_log('api').error("delete profile error:%s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg': 'delete profile failed'})

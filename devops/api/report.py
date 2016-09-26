#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util,datetime
from tasks import sendMail

#这里是关于用户角色的增删改查及组对应的权限id2name

@jsonrpc.method('report.create')
@auth_login
def report_create(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
	reporttime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#	print type(reporttime)
        data = request.get_json()['params']	
	data['username']= username
	data['reporttime'] = reporttime
#	print data	
    #    if not util.check_name(check_name):
    #        return json.dumps({'code': 1, 'errmsg': 'name must be string or int'})
        app.config['cursor'].execute_insert_sql('report', data)
	sendMail.delay(str(data['mail']),username+"提交了故障申报",str(data['remark'])+str(data['ip']))
        util.write_log('api').info(username, "create report %s scucess" %  data['ip'])
        return json.dumps({'code':0,'result':'create report %s scucess' % data['ip']})
    except:
        util.write_log('api').error(username,"create report error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create report fail'})

@jsonrpc.method('report.getlist')
@auth_login
def report_select(auth_info,**kwargs):
    data_result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
#    if '1' not in auth_info['r_id']:
#        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        fields = ['id','username','mail','server_run','ip','remark','reporttime','status']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        res = app.config['cursor'].get_results('report', fields)
#	print res
        util.write_log('api').info(username, 'select report list success')
        return json.dumps({'code':0,'result':res})
    except:
        util.write_log('api').error("select report list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get report failed'})

@jsonrpc.method('report.get')
@auth_login
def report_get(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_update_sql('report', {'status': 1 }, where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        else:
            util.write_log('api').info(username, "update report by id success")
        return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('select report by id error: %s'  % traceback.format_exc())
        return  json.dumps({'code':1,'errmsg':'get report failed'})

@jsonrpc.method('maintain.get')
@auth_login
def maintain_get(auth_info, **kwargs):
    if auth_info['code']==1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        output = ['id','ip','server_run','mail']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1,'errmsg':'must need a condition'})
        result = app.config['cursor'].get_one_result('report', fields, where)
	if not result:
	    return json.dumps({'code':1, 'errmsg':'result is null'})
	else:
	    util.write_log('api').info(username, "get report by id success")
	return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error("get list permission error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get report failed'})

@jsonrpc.method('maintain.update')
@auth_login
def maintain_update(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
	reporttime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        where = data.get('where',None)
        data = data.get('data',None)
        data['username']= username
        data['xiajia'] = reporttime
	result = app.config['cursor'].execute_insert_sql('maintain', data)
	sendMail.delay(str(data['mail']),str(data['ip'])+str(data['server_run']),str(data['remark']))
        if not result:
            return json.dumps({'code':1, 'errmsg':'the result may be repeat'})
        util.write_log('api').info(username, 'update maintain success!' )
        return json.dumps({'code':0,'result':'update maintain scucess'})
    except:
        util.write_log('api' ).error("update error: %s"  % traceback.format_exc())
        return  json.dumps( {'code':1,'errmsg':"update maintain failed"})

@jsonrpc.method('maintain.getlist')
@auth_login
def maintain_select(auth_info,**kwargs):
    data_result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        fields = ['id','username','server_run','ip','remark','xiajia']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        res = app.config['cursor'].get_results('maintain', fields)
#       print res
        util.write_log('api').info(username, 'select report list success')
        return json.dumps({'code':0,'result':res})
    except:
        util.write_log('api').error("select report list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get report failed'})


@jsonrpc.method('report.update')
@auth_login
def report_update(auth_info, **kwargs):
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

@jsonrpc.method('report.delete')
@auth_login
def report_delete(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no idc' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
	print where 
	print "xiaoluoge1111111"
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].execute_delete_sql('report', where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete report successed')
        return json.dumps({'code':0,'result':'delete report scucess'})
    except:
        util.write_log('api'). error('delete report error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete report failed'}) 


@jsonrpc.method('maintain.delete')
@auth_login
def maintain_delete(auth_info,**kwargs):
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
        result = app.config['cursor'].execute_delete_sql('maintain', where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete maintain successed')
        return json.dumps({'code':0,'result':'delete maintain scucess'})
    except:
        util.write_log('api'). error('delete maintain error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete maintain failed'})

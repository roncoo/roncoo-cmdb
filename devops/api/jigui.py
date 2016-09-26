#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util

@jsonrpc.method('jigui.getlist')
@auth_login
def jigui_select(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
 	data_result = []
	ret_json = {}
	fields = ['id','vm_status','os','server_purpose','idc_id','cabinet_id','cabinet_pos','host_status','ip','host_models']
        #将角色对应的p_id都转为name,最终返回的结果p_id的值都是name 
        data = app.config['cursor'].get_results('server', fields)
        for i in data:
            if i["idc_id"]:
                idc = app.config['cursor'].get_one_result('idc', ['name'],{"id":int(i["idc_id"])})
                cabinet = app.config['cursor'].get_one_result('cabinet', ['name'],{"id":int(i["cabinet_id"])})
                i['idc_name'] = str(idc['name'])
                i['cabinet_name'] = str(cabinet['name'])
                data_result.append(i)   
#	print data_result
        util.write_log('api').info(username, 'select jigui list success')
        return json.dumps({'code':0,'result':data_result})
    except:
        util.write_log('api').error("select role list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'get rolelist failed'})

#!/usr/bin/env python
#coding:utf-8
from flask import Flask, request
from . import app,jsonrpc
import  util
from auth import auth_login
import json,time,traceback

@jsonrpc.method('selected.get')
@auth_login
def selected(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data=request.get_json()['params']
        where = data.get('where',None)
        m_table = data.get('m_table',None)
        field = data.get('field',None)
        s_table = data.get('s_table',None)
        res = app.config['cursor'].get_one_result(m_table,[field],where) 
        res=res[field].split(',')  #eg: ['1','2']
        result = app.config['cursor'].get_results(s_table,['id','name'])
        for x in result: #eg: [{'id':1,'name':'sa'},{'id':2,'name':'php'}]
           for r_id in res:
               if r_id in str(x['id']): 
                    x['selected'] = 'selected="selected"'
        util.write_log('api').info(username,'selected  %s  successfully' % (s_table))
        return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('selected  error: %s' % traceback.format_exc())
        return json.dumps({'code':'1','errmsg':'selected.get  error'})



#!/usr/bin/env python
#coding:utf-8
from flask import  request
from . import app , jsonrpc
from auth import auth_login
import json, traceback
import util
import time,datetime
from zabbix_api import *

#这里是关于用户角色的增删改查及组对应的权限id2name
def timeturnmap(a):
    ltime=time.localtime(a)
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    return timeStr

@jsonrpc.method('zabbix.add')
@auth_login
def zabbix_add(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
	hosts = data['hostids'][0].split(",")
        result = create_zabbix_host(hosts,data['groupid'])
        util.write_log('api').info(username, "create zabbix host %s scucess" %  result[0]['hostids'])
        return json.dumps({'code':0,'result':'create zabbix host %s scucess' % result[0]['hostids']})
    except:
        util.write_log('api').error(username,"create zabbix error: %s" % traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'create zabbix fail'})

@jsonrpc.method('zabbix.getlist')
@auth_login
def zabbix_select(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        hostgroup = app.config['zabbix'].get_hostgroup()
        util.write_log('api').info(username, 'select zabbix list success')
        return json.dumps({'code':0,'result': hostgroup})
    except:
        util.write_log('api').error("select zabbixgroup list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'getzabbixgroup failed'})

@jsonrpc.method('zabbix_maintenance.getlist')
@auth_login
def zabbix_maintenance(auth_info,**kwargs):
    ret = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        data = app.config['zabbix'].get_maintenance()
        for i in data:
            i['active_since'] = timeturnmap(float(i['active_since']))
            i['active_till'] = timeturnmap(float(i['active_till']))
            i['hosts']  = len(i['hosts'])
            ret.append(i)
        util.write_log('api').info(username, 'select zabbix list success')
        return json.dumps({'code':0,'result': ret})
    except:
        util.write_log('api').error("select zabbixgroup list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'getzabbixgroup failed'})


@jsonrpc.method('zabbix_maintenance.delete')
@auth_login
def zabbix_maintenance_delete(auth_info,**kwargs):
    result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no root' })
    try:
        data = request.get_json()['params']
        where = data.get('where',None)
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
#       result =  app.config['zabbix'].del_maintenance(where['id'])
        ret = app.config['zabbix'].get_maintenance()
        for i in ret:
            if int(i['maintenanceid']) == where['id']:
                for host in i['hosts']: 
                    result.append(app.config['zabbix'].host_status(hostid=host['hostid'],status='0'))      
        app.config['zabbix'].del_maintenance(where['id'])
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        util.write_log('api').info(username, 'delete zabbix_maintenance successed')
        return json.dumps({'code':0,'result':'delete zabbix_maintenance scucess'})
    except:
        util.write_log('api'). error('delete zabbix_maintenance error: %s' %  traceback.format_exc())
        return json.dumps({'co de':1,'errmsg':'delete zabbix_maintenance failed'})


@jsonrpc.method('zabbix.link_tem')
@auth_login
def zabbix_link_tem(auth_info,**kwargs):
    result = []
    tem = []
    template = {}
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        data = request.get_json()['params']
#       {u'hostids': [u'10157,10158'], u'groupid': u'10001'}
        data_host = data['hostids'][0].split(',')
        for i in data_host:
            if len(app.config['zabbix'].hostid_get_template(i)[0]['parentTemplates']) == 0:
                result.append(app.config['zabbix'].link_template(int(i),data['groupid']))
            else:
                template['templateid']=data['groupid']
                data_mu = app.config['zabbix'].hostid_get_template(i)[0]['parentTemplates']
                data_mu.append(template)
                result.append(app.config['zabbix'].link_template(int(i),data_mu))
        util.write_log('api').info(username, 'select zabbix template list success')
        return json.dumps({'code':0,'result': result})
    except:
        util.write_log('api').error("link zabbix templeate  error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'link zabbix template failed'})

@jsonrpc.method('zabbix.unlink_tem')
@auth_login
def zabbix_unlink_tem(auth_info,**kwargs):
    result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        data = request.get_json()['params']	
#       {u'hostids': [u'10157,10158'], u'groupid': u'10001'}
        data_host = data['hostids'][0].split(',')
        for i in data_host:
            result.append(app.config['zabbix'].unlink_template(int(i),data['templateid']))
        util.write_log('api').info(username, 'select zabbix template list success')
        return json.dumps({'code':0,'result': result})
    except:
        util.write_log('api').error("link zabbix templeate  error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'link zabbix template failed'})


@jsonrpc.method('zabbix_maintenance.create')
@auth_login
def zabbix_main_add(auth_info,**kwargs):
    ret = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        data = request.get_json()['params']
#       {u'host_id': u'10157,10158', u'name': u'xiaoluo', u'time': u'2'} 
        start = (str(time.time())).split('.')[0]
        stop = (int(start) + 7200)
        hostids = data['host_id'].split(',')
        result = create_maintenance(data['name'],start,stop,hostids,int(data['time']))
        for i in hostids:
            ret.append(app.config['zabbix'].host_status(hostid=i,status='1'))
        util.write_log('api').info(username, 'select zabbix template list success')
        return json.dumps({'code':0,'result': ret})
    except:
        util.write_log('api').error("create zabbix mainchare  error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'please check you maintenance'})


@jsonrpc.method('zabbix_tem.getlist')
@auth_login
def zabbix_get_templeate(auth_info,**kwargs):
    result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        result = app.config['zabbix'].get_host_tem()
        #print result
        util.write_log('api').info(username, 'select zabbix template list success')
        return json.dumps({'code':0,'result': result})
    except:
        util.write_log('api').error("link zabbix templeate  error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'link zabbix template failed'})



@jsonrpc.method('zabbix_gettem.getlist')
@auth_login
def zabbix_gettem_select(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        tem = app.config['zabbix'].get_template()
        util.write_log('api').info(username, 'select zabbix template list success')
        return json.dumps({'code':0,'result': tem})
    except:
        util.write_log('api').error("select zabbix templeate list error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'getzabbix template failed'})


@jsonrpc.method('zabbix.get')
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
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        result = app.config['cursor'].get_one_result('idc', fields, where)
        if not result :
            return json.dumps({'code':1, 'errmsg':'result is null'})
        else:
            util.write_log('api').info(username, "select role by id success")
            return json.dumps({'code':0,'result':result})
    except:
        util.write_log('api').error('select idc by id error: %s'  % traceback.format_exc())
        return  json.dumps({'code':1,'errmsg':'get idc failed'})

@jsonrpc.method('zabbix.update')
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



@jsonrpc.method('zabbix_template.unlink_tem')
@auth_login
def zabbix_unlink_tem(auth_info,**kwargs):
    result = []
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1,'errmsg':'you not admin,no cmdb' })
    try:
        data = request.get_json()['params']
	print data
#       {u'hostids': [u'10157,10158'], u'groupid': u'10001'}
        data_host = data['hostids'][0].split(',')
        for i in data_host:
            result.append(app.config['zabbix'].unlink_template(int(i),data['templateid']))
        util.write_log('api').info(username, 'select zabbix template list success')
        return json.dumps({'code':0,'result': result})
    except:
        util.write_log('api').error("link zabbix templeate  error: %s"  %  traceback.format_exc())
        return json.dumps({'code':1,'errmsg':'link zabbix template failed'})

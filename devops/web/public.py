#coding:utf-8
from __future__ import unicode_literals
from flask import Flask, render_template,session,redirect,request
from  . import app  
import requests,json 
import util,urllib

headers = {"Content-Type": "application/json"}
data = {
        "jsonrpc": "2.0",
        "id":1,
}

def get_url():
    return "http://%s/api" % app.config['api_host']

def Handleformdata(formdata):
    res = {}
    for x in formdata.split('&'): #formdata="id=1&id=2&id=3&name=lzp&passwd=1111" > ['id=1','id=2','name=lzp'......]
        k, v = x.split('=', 1)  # x: id=1,name=wd, >  k=id,v=1
        if k in res and isinstance(res[k], list):
            res[k].append(v)    # 3: res['id']=[1,2,3]
        elif k in res:
            res[k] = [res[k], v] #2: res['id']=[1,2]
        else:
            res[k] = v     #1: res['id']=1
            #res={'id': ['1', '2','3'], 'name': 'wd', 'passwd': '1111'}

    for k in res:
        if isinstance(res[k] , list):
            res[k] = ','.join(res[k])
    return res
           #res={'id': ['1,2,3'], 'name': 'wd', 'passwd': '1111'}


@app.route('/listapi')
def listapi():
    headers['authorization'] = session['author']
    method = request.args.get('method')
    data['method'] = method+".getlist"
    data['params'] = {} 
    util.write_log('web').info(data)  
    r = requests.post(get_url(),headers=headers,json=data)
   # print r.text 
    util.write_log('web').info(r.text) 
    return r.text 

@app.route('/addapi', methods=['GET','POST'])
def addapi():
    headers['authorization'] = session['author']
    method = request.form.get('method') 
    formdata = request.form.get('formdata')  #str
    print repr(formdata)    #flask默认解码为unicode格式如： u'id=13&name=aa&remark=%E4%BD%A0%E5%A5%BD' 中文部分python无法解析 
    try:
        formdata = urllib.unquote(formdata).encode('iso-8859-1') 
        #print repr(formdata)          #解码后中文为utf8格式： u'id=13&name=aa&remark==\xe4\xbd\xa0\xe5\xa5\xbd' 
    except:
       pass
    formdata = Handleformdata(formdata)
    data['method'] = method+".create"
    data['params']=formdata  
    util.write_log('web').info(data)
    r = requests.post(get_url(),headers=headers,json=data)
    return r.text

@app.route('/getapi')
def getapi():
    headers['authorization'] = session['author']
    method = request.args.get('method') 
    data['method'] = method+".get" 
    uid = request.args.get('id')
    data['params'] = {
        "m_table":request.args.get('m_table',None),
        'field':request.args.get('field',None),
        's_table':request.args.get('s_table',None),
        'where':{'id':int(request.args.get('id'))}
    }   
    util.write_log('web').info(data)
    r = requests.post(get_url(),headers=headers,json=data)
    return r.text


@app.route('/updateapi',methods=['GET','POST'])
def updateapi():
    headers['authorization'] = session['author']
    method = request.form.get('method')
    formdata = request.form.get('formdata')  #str
   # print formdata   
    try:
        formdata = urllib.unquote(formdata).encode('iso-8859-1')
    except:
       pass
    formdata = Handleformdata(formdata)
    data['method'] = method+".update"
    data['params'] = {
        "data":formdata,
        "where":{
            "id":int(formdata['id'])
        }
    }
    util.write_log('web').info(data)
    r = requests.post(get_url(), headers=headers, json=data)
    return r.content

@app.route('/deleteapi')
def deleteapi():
    headers['authorization'] = session['author']
    method = request.args.get('method')
    data['method'] = method+".delete"
    data['params'] = {
        "where":{
         "id":int(request.args.get('id'))
         }
    }
    util.write_log('web').info(data)
    r = requests.post(get_url(),headers=headers,json=data)
    return r.text

@app.route('/updateserverapi',methods=['GET','POST'])
def updateserverapi():
    headers['authorization'] = session['author']
    method = request.form.get('method')
    formdata = request.form.get('formdata')  #str
#    print formdata
    try:
        formdata = urllib.unquote(formdata).encode('iso-8859-1')
    except:
       pass
    formdata = Handleformdata(formdata)
    data['method'] = method+".update"
    data['params'] = {
        "data":formdata,
        "where":{
            "ip":formdata['ip']
        }
    } 
    util.write_log('web').info(data)
    r = requests.post(get_url(), headers=headers, json=data)
    return r.content

@app.route('/zabbixapi',methods=['GET','POST'])
def add_zabbix_api():
    headers['authorization'] = session['author']
    params = dict(request.form) 
    data['method']= 'zabbix.'+str(params['method'][0]) 
    data['params'] = {
	"hostids": params["hostids"],
	"groupid": params["groupid"][0]
	} 
    util.write_log('web').info(data)
    r = requests.post(get_url(), headers=headers, json=data)  
    return r.content


@app.route('/zabbix_template',methods=['GET','POST'])
def zabbix_template():
    headers['authorization'] = session['author']
    params = dict(request.form)
    data['method']= 'zabbix_template.'+str(params['method'][0])
    data['params'] = {
        "hostids": params["hostid"],
        "templateid": params["templateid"][0]
        }
    util.write_log('web').info(data)
    r = requests.post(get_url(), headers=headers, json=data)
    return r.content

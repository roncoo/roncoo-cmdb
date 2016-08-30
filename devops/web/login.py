#coding:utf-8
from flask import Flask,request,session,render_template,redirect
from  . import app  
import requests,json 
import util 

headers = {'content-type': 'application/json'}

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passwd')
        url = "http://%s/api/login?username=%s&passwd=%s" % (app.config['api_host'],username,password)
        r = requests.get(url, headers=headers)      #请求API验证用户，并获取token
        result = json.loads(r.content)
        if result['code'] == 0:
            token = result["authorization"]
            res = util.validate(token,app.config['passport_key'])  #解密token 
            res = json.loads(res)         #return : dict(username:*,uid:*,role:*)
            session['author'] = token
            session['username'] = username 
    	    return json.dumps({'code':0})
        else:
            return json.dumps({'code':1,'errmsg':result['errmsg']})
    return render_template('login.html')

@app.route("/logout",methods=['GET','POST'])
def logout():
    if session.get('author','nologin') == 'nologin':
        return redirect('/login')
    session.pop('author',None)
    return redirect('/login')  

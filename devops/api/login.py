#!/usr/bin/env python
#coding:utf-8
from flask import Flask, request
from . import app
import  util
import json,time,traceback,hashlib

#用户登录验证，并生成token
@app.route('/api/login', methods=['GET'])
def login():
        try:
            username = request.args.get('username', None)
            passwd = request.args.get('passwd', None)
            passwd = hashlib.md5(passwd).hexdigest()	
            if not (username and passwd):
                return json.dumps({'code': 1, 'errmsg': "需要输入用户名和密码"})
            result = app.config['cursor'].get_one_result('user', ['id', 'username', 'password', 'r_id', 'is_lock'], {'username': username}) 
            if not result:
                return json.dumps({'code': 1, 'errmsg': "用户不存在"})
            if result['is_lock'] == 1:
                return json.dumps({'code': 1, 'errmsg': "用户已被锁定"})

            if passwd == result['password']:
                data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')} 
                app.config['cursor'].execute_update_sql('user', data, {'username': username})
                token = util.get_validate(result['username'], result['id'], result['r_id'], app.config['passport_key'])	
                return json.dumps({'code': 0, 'authorization': token})
            else:
                return json.dumps({'code': 1, 'errmsg': "输入密码有误"})
        except:
            util.write_log('api').error("login error: %s" % traceback.format_exc())
            return json.dumps({'code': 1, 'errmsg': "登录失败"})



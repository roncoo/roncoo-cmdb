#!/bin/env python
# -*- encoding: utf-8 -*-
from api import app, zabbix_api, zabbix_Graph_api
import os,sys,logging,logging.config
import db,util
from celery import Celery

#session使用需要设置secret_key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#导入自定义的各种配置参数，最终参数以字典形式返回
work_dir = os.path.dirname(os.path.realpath(__file__))
service_conf = os.path.join(work_dir, 'conf/service.conf')
img = os.path.join(work_dir,'web/static/zabbix')
img_url = {"zabbix_img_url":img}


config = util.get_config(service_conf, 'api')
cobbler_config = util.get_config(service_conf, 'cobbler')
zabbix_config = util.get_config(service_conf, 'zabbix')



#将参数追加到app.config字典中，就可以随意调用了
app.config.update(config)
app.config.update(cobbler_config)
app.config.update(img_url)
app.config.update(zabbix_config)
#print app.config



#实例化数据库类，并将实例化的对象导入配置
app.config['cursor'] = db.Cursor(config)
app.config['zabbix'] = zabbix_api.Zabbix(zabbix_config)

########celery实例化加载###########




if __name__ == '__main__':
    app.run(host=config.get('bind', '0.0.0.0'),port=int(config.get('port')), debug=True)

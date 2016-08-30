#!/bin/env python
# -*- encoding: utf-8 -*-
from web import app
import os,sys,logging,logging.config
import db,util

work_dir = os.path.dirname(os.path.realpath(__file__))
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

service_conf = os.path.join(work_dir, 'conf/service.conf')
config = util.get_config(service_conf, 'web')
#print config

#将参数追加到app.config字典中，就可以随意调用了
app.config.update(config)



if __name__ == '__main__':
    app.run(host=config.get('bind', '0.0.0.0'),port=int(config.get('port')), debug=True)

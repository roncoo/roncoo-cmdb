from flask import Flask                                                                    
from flask_jsonrpc import JSONRPC
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')

import login
import power
import role
import user
import select
import idc
import cabinet
import server
import zabbix
import zbhost
import zabbix_api
import cobbler
import zabbix_Graph_api
import switch

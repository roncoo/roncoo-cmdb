from flask import Flask                        
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

import demo,public,login


'''
    logmon
    ------
    
    Realtime log monitor.
'''

from flask import Flask

app = Flask(__name__)
app.config.from_object('logmon.config.Config')

import logmon.views

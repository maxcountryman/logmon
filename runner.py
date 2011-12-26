if __name__ == '__main__': 
    from logmon import app
    
    from flask import escape
    from juggernaut import Juggernaut
    
    import gevent
    from gevent import monkey
    from gevent.wsgi import WSGIServer
    from werkzeug.contrib.fixers import ProxyFix
    
    import time
    
    monkey.patch_all()
    jug = Juggernaut()
    
    LOG_FILE = app.config['LOG_FILE']
    
    
    def follow(follow_file):
        follow_file.seek(0, 2)
        while True:
            line = follow_file.readline()
            if not line:
                time.sleep(0.1)
                continue
            line = escape(line)
            jug.publish('logger', line)
    
    
    # fixes the X-Real-IP header
    app.wsgi_app = ProxyFix(app.wsgi_app)
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    jobs = [gevent.spawn(follow, open(LOG_FILE)),
            gevent.spawn(http_server.serve_forever)]
    gevent.joinall(jobs)


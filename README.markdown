# Logmon

Logmon is a realtime log reader written with Flask and Juggernaut.

![Realtime log reader in Flask](http://f.cl.ly/items/113H1p1T2C3D251p2z1o/Screen%20Shot%202011-12-26%20at%207.35.52%20AM.png "Logmon")

## Installation

Start by cloning this repository:

    $ git clone git://github.com/maxcountryman/logmon.git

This application does assume you have Node.js installed so that you can make
use of npm and run Juggernaut. You will need npm to install Juggernaut if not
already installed:

    $ curl http://npmjs.org/install.sh | sh

Now you should be able to install Juggernaut:

    $ npm install -g juggernaut 

Once installed you will now need to run Juggernaut. Juggernaut serves as an
interface between the frontend of the application and the backend.

Finally before you can use the included runner you will need to install gevent.
Gevent is a coroutine-based module for concurrency. Here it serves the simple
task of reading off a file without blocking execution:

    $ pip install -U gevent

At this point you should be able to execute the runner script and point your
browser to `http://127.0.0.1:5000`.

## Usage

Once set up, ensure the Juggernaut server is already running and then simply
execute the runner script:

    $ python runner.py
    
## A Note On Rotating Logs

Depending upon how log rotating is setup, the follow function in the runner 
script will break when the log is rotated. In order to get around this you 
may need to do some hacking related to your specific set up. 

Assuming you're using logrotated and nginx you can edit the logrotated 
config to use a customized sh command when rotating. For instance, let's 
assume your config is located `/etc/logrotate.d/nginx`, then you might 
edit it to look like this:
    
        /var/log/nginx/*log {
                create 640 http log
                compress
                postrotate
                        /bin/kill -USR1 `cat /var/run/nginx.pid 2>/dev/null` 2> /dev/null || true
                        /bin/kill -HUP `cat /tmp/Logmon.pid`
                endscript
        }

Notice we are sending a SIGHUP to the logmon script. In order for this 
to work we need to modify the runner to save its PID as well as 
respond to SIGHUP in a favorable way.

Because the runner is making use of gevent and due to some pecularities 
of the specifics of the way libev is wrapped, the gevent.signals 
wrapper must be used in place of Python's built-in module.

The rewrite should look something like this, although depending on your 
situation you may find this needs to be modified:

    if __name__ == '__main__':
        from logmon import app
        
        from flask import escape
        from juggernaut import Juggernaut
        
        import gevent
        from gevent import monkey
        from gevent.wsgi import WSGIServer
        from werkzeug.contrib.fixers import ProxyFix
        
        import os
        import time
        import signal
        
        monkey.patch_all()
        jug = Juggernaut()
        f = None
        
        LOG_FILE = app.config['LOG_FILE']
        
        
        def write_pid(filepath='/tmp/{}.pid'):
            with open(filepath.format(app.config['SITE_NAME']), 'w') as f:
                pid = str(os.getpid())
                f.write(pid)
        
        
        def follow(filepath):
            global f
            f = open(filepath)
            f.seek(0, 2)
            
            def rotate_handler():
                global f
                f.close()
                f = open(filepath)
            
            # bind to SIGHUP
            gevent.signal(signal.SIGHUP, rotate_handler)
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                line = escape(line)
                jug.publish('logger', line)
        
        
        # write the PID to a file
        write_pid()
        
        # fixes the X-Real-IP header
        app.wsgi_app = ProxyFix(app.wsgi_app)
        http_server = WSGIServer(('127.0.0.1', 5051), app)
        jobs = [gevent.spawn(follow, LOG_FILE),
                gevent.spawn(http_server.serve_forever)]
        gevent.joinall(jobs)

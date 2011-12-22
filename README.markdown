# Logger

Logger is a realtime log reader written with Flask and Juggernaut.

![Realtime log reader in Flask](http://f.cl.ly/items/3D1P000W1i2y1V2x3W3M/Screen%20Shot%202011-12-22%20at%202.01.12%20PM.png "Logger")

## Requirements

Logger depends on Juggernaut and the Python bindings for Juggernaut. It also 
makes use of gevent. Running this application assumes the Juggernaut server is 
already set up and running. If already running all you should need to do is 
execute the runner:
    
    $ python runner.py


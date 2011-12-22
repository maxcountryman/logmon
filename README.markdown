# Logger

Logger is a realtime log reader written with Flask and Juggernaut.

## Requirements

Logger depends on Juggernaut and the Python bindings for Juggernaut. It also 
makes use of gevent. Running this application assumes the Juggernaut server is 
already set up and running. If already running all you should need to do is 
execute the runner:
    
    $ python runner.py

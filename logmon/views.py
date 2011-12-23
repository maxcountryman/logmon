from logmon import app
from flask import render_template

LOG_FILE = app.config['LOG_FILE']
MAX_LEN = -100


@app.route('/')
def index():
    with open(LOG_FILE, 'r') as f:
        log_buffer = f.readlines()
    return render_template('index.html', log_buffer=log_buffer[MAX_LEN:])


if __name__ == '__main__':
    app.run()

from logger import app
from flask import render_template

app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

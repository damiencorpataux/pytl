import flask

import sys; sys.path.append('../..')
import data

app = flask.Flask(__name__)

@app.route('/')
def index():
    return app

@app.route('/line')
def line():
    return flask.jsonify({
        'data': data.line()
    })

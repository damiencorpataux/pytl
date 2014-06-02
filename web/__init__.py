import flask

import sys; sys.path.append('../..')
import data

app = flask.Flask(__name__)

@app.errorhandler(Exception)
def error(e):
    if app.debug:
        raise
    else:
        return flask.jsonify({
            'error': str(e)
        })

@app.route('/')
def index():
    return flask.jsonify({
        'routes': [str(r) for r in app.url_map.iter_rules()]
    })

@app.route('/search/')
@app.route('/search/<text>')
def search(text=None):
    return flask.jsonify({
        'suggest': [data.dic(row) for row in data.suggest(text)]#, line=line, station=station)]
    })

@app.route('/deps/<station>')
@app.route('/deps/<station>/<line>')
def departures(station, line=None):
    return flask.jsonify({
        'departures': [data.dic(row) for row in data.departures(station, line)]
    })

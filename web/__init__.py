import flask

import sys; sys.path.append('../..')
import data

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.jsonify({
        'routes': [str(r) for r in app.url_map.iter_rules()]
    })

@app.route('/s/')
@app.route('/s/<text>')
@app.route('/search/')
@app.route('/search/<text>')
def search(text=None):
    return flask.jsonify({
        'suggest': data.suggest(text)#, line=line, station=station)
    })

@app.route('/deps/<line>/<station>')
def departures(station, line):
    return flask.jsonify({
        'departures': [d for d in data.departures(station, line)]
    })

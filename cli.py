import argh
import data
import warnings; warnings.filterwarnings("ignore", category=UserWarning)

@argh.arg('string', help='search string')
@argh.arg('-l', '--line', help='line name filter string')
@argh.arg('-s', '--station', help='station name filter string')
def search(string,line=None,station=None):
    """
    lists matching stations and lines
    """
    for item in data.suggest(string, line=line, station=station):
        print('%(line)s:\t%(station)s (%(direction)s %(orientation)s) (%(lon)s, %(lat)s)' % item)

#@argh.aliases('dep')
@argh.arg('station', help='station search string')
@argh.arg('-l', '--line', help='line search string')
def deps(station,line=None):
    """
    lists departures for matching stations and lines
    """
    for item in data.departures(station, line):
        print('%(station)s %(line)s %(direction)s %(timetable)s (%(lon)s, %(lat)s)' % item)

def web():
    """
    starts the standalone webserver (for dev purpose)
    """
    import web
    web.app.run(host='0.0.0.0', port=5000, debug=True)

def init():
    """
    Initializes database (WARNING: drops, creates and popoulates)
    """
    y = raw_input('This will drop, create and populate database. '
                  'Continue [y/N] ?')
    if y in ['y', 'yes']:
        import data.db
        data.db.populate()

def web():
    """
    starts the standalone webserver (for dev purpose)
    """
    import web
    web.app.run(host='0.0.0.0', port=5000, debug=True)

def run():
    argh.dispatch_commands([search, deps, web, init])

import argh
import data
import warnings; warnings.filterwarnings("ignore", category=UserWarning)

def search(string : 'search string',
           line : 'line name filter string' = None,
           station : 'station name filter string' = None):
    """
    lists matching stations and lines
    """
    for item in data.suggest(string, line=line, station=station):
        print('%(line)s:\t%(station)s (%(direction)s %(orientation)s)' % item)

#@argh.aliases('dep')
def deps(station : 'station search string',
         line : 'line search string' = None):
    """
    lists departures for matching stations and lines
    """
    for item in data.departures(station, line):
        print('%(station)s %(line)s %(direction)s %(departures)s' % item)

def run():
    argh.dispatch_commands([search, deps])

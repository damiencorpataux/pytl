"""
Provides timetable data. For humans.

Usage:

>>> tl.line()
<line-nr>: <terminus-a> <terminus-r>
...
>>> tl.line(1)
1: Maladiere, Blecherette
>>> tl.line(1).next()
<direction-a>: <stop-name>: <time>
<direction-a>: ...
...
<direction-r>: <stop-name>: <time>
<direction-r>: ...
...
>>> tl.line(1).station('blech')
>>> tl.line(1).station('blech').next()
>>> tl.station()
>>> tl.station('georg')
>>> tl.station('georg').next()
>>> tl.station('georg').line()

>>> #displays next departure for stations matching string
>>> tl.next('blech')
<stop-name>: <direction-going>: <time> <direction-coming>: <time>
...

>>> #displays next departure for 
>>> tl.travel('blech geor')

>>> #displays all lines servicing stations matching string
>>> tl.lines()
>>> tl.lines(2)
>>> tl.lines('georg')
<station>:
<line-nr>: <terminus-a> <terminus-r>
...
<station>:
<line-nr>: <terminus-a> <terminus-r>
...

>>> #displays all stations for line matching
"""

import data.scrap as scrap
from data.db import models as m
from data.db import session as s
from sqlalchemy import or_

def dic(result):
    if type(result) is list:
        return [{k:v for k,v in row.__dict__.items()
                if not k.startswith('_sa')} for row in result]
    else:
        return result.__dict__

def suggest(fulltext=None, line=None, station=None, order=None,
            gowild=lambda s: s if str(s).count('%') else '%%%s%%'%s):
    """
    Returns matching line and stations.
    Search uses a "LIKE %string%" comparator.
    :param fulltext: filters all searchable fields with an OR operator
    :param line: filters on line name
    :param station: filters on station name
    """
    # Querying
    q = s.query(m.stop).join(m.line, m.station)
    searchable = {
        'line': m.line.name,
        'station': m.station.name
    }
    for arg,column in searchable.items():
        if locals().get(arg):
            string = locals().get(arg)
            if arg not in ['line']: string = gowild(string)
            q = q.filter(column.like(string))
    if fulltext:
        q = q.filter(or_(*[column.like(gowild(fulltext))
                           for column in searchable.values()]))
    if order:
        q = q.order_by(*order)
    # Results processing
    return [{
        'line': r.line.name,
        'station': r.station.name,
        'root': r.station.root,
        'direction': r.direction,
        'orientation': r.orientation
    } for r in q.all()]

def departures(station, line=None):
    if len(station) < 3:
        raise ValueError('Please specify at leat 3 characters for "station"')
    #FIXME: collect alerts too (item['alerts'])
    for item in suggest(station=station, line=line, order=[m.station.name, m.line.name, m.stop.direction]):
        departures = scrap.departures(
            item['line'],
            '%(root)s_%(orientation)s'%item,
            item['direction'].upper())
        yield {
            'line': item['line'],
            'station': item['station'],
            'departures': departures['departures'],
            'direction': item['direction']}
t=departures

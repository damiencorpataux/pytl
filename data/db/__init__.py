"""
Database component
"""

import os
import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.automap as am

import sys; sys.path.append('../..') 
from data.scrapper import tl, osm

# Basic engine
e = engine = sa.create_engine('mysql+mysqlconnector://tl:tl@localhost/tl')
sm = sessionmaker = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))
s = session = sessionmaker()

# Automap
Base = am.automap_base()
Base.prepare(engine, reflect=True, generate_relationship=am.generate_relationship)
m = models = Base.classes

# Cration and population
def create():
    """
    Drops and creates database
    """
    filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'database.sql')
    with open(filename) as f:
        sql = f.read()
    for stmt in [stmt.strip() for stmt in sql.split(';')]:
        print(stmt)
        try: session.execute(stmt)
        except Exception as e:#sa.exc.StatementError as e:
            if '1051' in str(e): pass # drop if exists: unknown table
            else:
                print('Error with:', stmt)
                raise

def populate():
    """
    Propulates database from data.scrap.
    """
    # Truncates tables (rough way)
    create() 
    # Scraps data
    populate_tl()
    populate_osm()

def populate_tl():
    for line in tl.lines():
        print(line)
        s.add(m.line(**line))  # inserts line
        for stop in tl.stops(line['id']):
            print(stop)
            if not s.query(m.station).filter(
            m.station.name == stop['name']).count():
                session.add(m.station(  # inserts station
                    name=stop['name'],
                    root=stop['id'].split('_').pop(0)))
            s.add(m.stop(
                orientation=stop['id'].split('_').pop(),
                direction=stop['direction'],
                line_id=s.query(m.line).filter(m.line.name==stop['line']).first().id,
                station_name=stop['name']))
            s.flush()
    s.commit()

def populate_osm():
    for stop in osm.stops():
        s.add(m.osm(
            lon=stop['lon'],
            lat=stop['lat'],
            name=stop.get('name'),
            name_uic=stop.get('uic_name'),
            operator=stop.get('operator'),
            uid=stop['uid'],
            version=stop['version']))
        s.flush()
    s.commit()

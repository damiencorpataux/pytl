"""
Database component
"""

import os
import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.automap as am

# Basic engine
e = engine = sa.create_engine('mysql+mysqlconnector://tl:tl@localhost/tl')
sm = sessionmaker = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))
s = session = sessionmaker()

# Automap
Base = am.automap_base()
Base.prepare(engine, reflect=True)
m = models = Base.classes

# Usable models


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
    import sys; sys.path.append('../..') 
    import data.scrap as scrap
    try:
        # Truncates tables (rough way)
        create() 
        # Scraps data
        for line in scrap.lines():
            print(line)
            session.add(m.line(**line))  # inserts line
            for stop in scrap.stops(line['id']):
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
        session.commit()
    except:
        session.rollback()
        raise

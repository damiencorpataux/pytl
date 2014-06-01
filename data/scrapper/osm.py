"""
Retrieves Switzerland bus stops from OSM extract (geofabrik).
"""

import sys, subprocess
import xml.etree.cElementTree as tree

# Alternative filtering, using osmosis
#     from http://zippy1978.tumblr.com/post/21800273257/extracting-data-from-openstreetmap-to-build-nice
# sudo apt-get install osmosis
# wget http://download.geofabrik.de/europe/switzerland-latest.osm.bz2
# bunzip2 switzerland-latest.osm.bz2
# osmosis --read-xml switzerland-latest.osm --tf accept-nodes highway=bus_stop --write-xml file=stops.osm

def stops_bs4():
    import bs4
    with open(filename) as file:
        filename = '/tmp/ch.osm'
        soup = bs4.BeautifulSoup(file.read())

def stops_etree():
    cmd = 'wget -O - http://download.geofabrik.de/europe/switzerland-latest.osm.bz2 | bunzip2 -'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    count = 0
    # http://effbot.org/zone/element-iterparse.htm#incremental-parsing
    context = iter(tree.iterparse(process.stdout, events=("start", "end")))
    event, root = context.next()
    for event, elem in context:
        count += 1
        sys.stdout.write('Processing: node %s %s %s\r'
                         % (count, elem.tag, ' '*5))
        if event == 'end':
            if elem.tag == "node":
                if [tag for tag in elem.findall('tag')
                    if tag.get('k') == 'highway'
                    and tag.get('v') == 'bus_stop']:
                    stop = dict(
                        {tag.get('k'):tag.get('v') for tag in elem.findall('tag')},
                        **{'lon': elem.get('lon'),
                           'lat': elem.get('lat'),
                           'uid': elem.get('uid'),
                           'version': elem.get('version')})
                    print '\n%s'%stop
                    yield stop
                elem.clear()
            root.clear()

stops = stops_etree

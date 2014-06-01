import os, sys, json
import subprocess
import xml.etree.cElementTree as tree

# TODO: from http://zippy1978.tumblr.com/post/21800273257/extracting-data-from-openstreetmap-to-build-nice
# sudo apt-get install osmosis
# wget http://download.geofabrik.de/europe/switzerland-latest.osm.bz2
# bunzip2 switzerland-latest.osm.bz2
# osmosis --read-xml switzerland-latest.osm --tf accept-nodes highway=bus_stop --write-xml file=stops.osm

filename = '/tmp/ch.osm'

def stops_bs4():
    import bs4
    with open(filename) as file:
        soup = bs4.BeautifulSoup(file.read())

def stops_etree():
    ##cmd = 'wget -O - http://download.geofabrik.de/europe/switzerland-latest.osm.bz2 2>/dev/null | bunzip2 - > %s' % filename
    cmd = 'wget -O - http://download.geofabrik.de/europe/switzerland-latest.osm.bz2 | bunzip2 - > %s' % filename
    p = subprocess.call(cmd, shell=True)
    with open(filename) as file:
        c = 0
        stops = []
        # http://effbot.org/zone/element-iterparse.htm#incremental-parsing
        context = iter(tree.iterparse(file, events=("start", "end")))
        event, root = context.next()
        for event, elem in context:#tree.iterparse(file): #p.stdout ? it has a .read() too
            c += 1
            sys.stdout.write('Processing: node %s %s %s\r' % (c, elem.tag, ' '*5))
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
    os.remove(filename)


stops = stops_etree

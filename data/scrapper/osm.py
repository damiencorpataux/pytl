import sys, json
import xml.etree.cElementTree as tree

# TODO: from http://zippy1978.tumblr.com/post/21800273257/extracting-data-from-openstreetmap-to-build-nice
# sudo apt-get install osmosis
# wget http://download.geofabrik.de/europe/switzerland-latest.osm.bz2
# bunzip2 switzerland-latest.osm.bz2
# osmosis --read-xml switzerland-latest.osm --tf accept-nodes highway=bus_stop --write-xml file=stops.osm

with open('stops.osm') as file:
    c = 0
    stops = []
    for event, elem in tree.iterparse(file):
        c += 1
        sys.stdout.write('node %s %s %s\r' % (c, elem.tag, ' '*5))
        if elem.tag == "node":
            #if [tag for tag in elem.findall('tag') if tag.get('k') == 'operator' and tag.get('v') == 'TL']:
            if [tag for tag in elem.findall('tag') if tag.get('k') == 'highway' and tag.get('v') == 'bus_stop']:
                stop = {tag.get('k'):tag.get('v') for tag in elem.findall('tag')}
                stop = dict(stop, **{'lon': elem.get('lon'),'lat': elem.get('lat'), 'uid': elem.get('uid'), 'version': elem.get('version')})
                print '\n', json.dumps(stop, indent=4)
                stops.append(stop)
            elem.clear()


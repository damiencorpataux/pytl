"""
Retrieves network and timetable data from tl website.
"""

import re, requests, bs4

def pour(url, **kwargs):
    """
    Creates a BeautifulSoup instance from the given url.
    :param url: url to request (GET)
    :param kwargs: additionnal arguments for request.get()
    """
    kwargs.update({'headers':{'User-Agent':None}})
    html = str(requests.get(url, **kwargs).content)
    return bs4.BeautifulSoup(html) 

def lines():
    """
    Returns a list of existing bus lines
    """
    #soup = pour('http://www.t-l.ch/horaires-par-arrets.html')
    #tags = soup.find_all('a', **{'class':'horaires_numbers_box'})
    #lines = [{'id': tag.get('id'),
    #FIXME: doesn't work; workaround:
    html = requests.get('http://www.t-l.ch/horaires-par-arrets.html',
                        headers={'User-Agent':None}).content
    r = re.compile('<.+?horaires_numbers_box.+?name="(.*?)".*?>(.*?)<.+?>')
    lines = [{'id': id,
              'name': name} for id,name in r.findall(str(html))]
    return lines

def stops(line):
    """
    Returns a list of bus stops for the given line.
    :param line: 'id' of the line
    """
    soup = pour(
        'http://www.t-l.ch/index.php',
        params={
            'option': 'com_tl',
            'task': 'get_arrets',
            'Itemid': '3',
            'format': 'raw',
            'choix': '11',
            'line': line})
    tags = soup.find_all('a', **{'class':'thermo_links'})
    r = re.compile('.*/(?P<line>.+?)_(?P<direction>.+?)_(?P<id>.+?).pdf')
    stops = [dict(r.search(tag.get('href')).groupdict(),
                  **{'name': tag.text}) for tag in tags]
    return stops

def departures(line, station, direction):
    """
    Returns the next departures for the given line and station
    and optionnal alerts about this line/station.
    :param line: 'name' of the line
    :param station: 'name' of the station
    """
    if direction not in ['A', 'R']:
        raise ValueError('"direction" valid values are "A", "B"')
    soup = pour(
        'http://www.t-l.ch/htr.php',
        params={
            'ligne': line,
            'arret': station,
            'sens': direction})
    departures = soup.find_all('tr', **{'class':'param'})
    alerts = soup.find_all('p', **{'class':'htr_perturbation_detail'})
    return {
        'departures': [tag.text for tag in departures
                       if not tag.text.startswith('*')],
        'alerts': [tag.text for tag in alerts]
    }

# Aliases
ln = lines
st = stops
dp = deps = departures

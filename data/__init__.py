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

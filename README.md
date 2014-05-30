pytl
====

Python TL* interface (transports lausannois)

--

## Installation
```
git clone <url> tl
cd !$
virtualenv --python=`which python3` --no-site-packages venv
source venv
pip install -r requirements.txt
python -c"import data.db as db; db.create(); db.populate()"
```
Run the standalone webserver: ```./tl web```

## CLI usage (intended)
```
./tl show 4
./tl show joliette
./tl search jo
```

## Console usage (intended)
```
import tl
tl.show(4)
tl.show('joliette')
tl.search('jo')
```

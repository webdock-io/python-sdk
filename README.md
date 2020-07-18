# Python SDK for Webdock API
This is the Python SDK to interact with Webdock API.

## Installation
Install from PyPi:
```shell
pip install webdock
```
or clone this repo and run:
```python
python setup.py install
```
## Usage
```python
from webdock.webdock import Webdock

wd = Webdock('your-api-token-here')
```

### Ping
```python
wd.ping()
```

### List servers
```python
servers = wd.servers()
```

### Get a server
```python
try:
    server = wd.get_server('server-slug')
except Exception as e:
    print('An error occured: {}'.format(str(e)))
```

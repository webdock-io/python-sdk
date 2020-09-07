# Python SDK for Webdock API
This is the Python SDK to interact with Webdock API. Please visit [https://apidocs.beta.webdock.io](https://apidocs.beta.webdock.io) to read the API documentation.

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

### Provision a Server
Data dictionary should contain these params:
| Param | Type | Details |
| ------- | --- | -- |
| name | string | A descriptive name for your server |
| slug | string | A unique slug for your server |
| locationId | string | ID of a location obtained from locations endpoint |
| profileSlug | string | ID of a profile obtained from profiles endpoint |
| imageSlug | string | ID of an image obtained from images endpoint |
| snapshotId (Optional) | string | ID of a snapshot obtained from snapshots endpoint |

```python
server = wd.provision_server(data)
```

### Get a server
```python
try:
    server = wd.get_server(serverSlug)
except Exception as e:
    print('An error occured: {}'.format(str(e)))
```

### Patch a server
```python
data = {
    'name': 'MyAwesomeServer',
    'description': 'My awesome Webdock server',
    'nextActionDate': 'A date time for next action',
    'notes': 'Some notes on this server'
}
wd.patch_server(serverSlug, data)
```

### Fetch a file from server
```python
res = wd.fetch_file(serverSlug, filePath)
```

### Get server locations
```python
locations = wd.get_locations()
```

### Get profiles
```python
profiles = wd.get_profiles()
```

### Get images
```python
images = wd.get_images()
```

### Get public SSH keys
```python
pubkeys = wd.get_pubkeys()
```

### Create a public key
```python
res = wd.create_key(keyName, publicKey)
```

### Delete a public key
```python
wd.delete_key(keyId)
```

### Get all shell users on a server
```python
users = wd.get_shellusers(serverSlug)
```

### Create a new shell user
`publicKeys` list should contain IDs of SSH keys
```python
res = wd.create_shelluser(serverSlug, username, password, group, shell, publicKeys=[])
```

### Delete a shell user
```python
wd.delete_shelluser(serverSlug, 'user-id')
```

### Update a shell user
`publicKeys` list should contain IDs of SSH keys
```python
res = wd.create_shelluser(serverSlug=serverSlug, shellUserId='shell-user-id-to-update', username='username', password='password', group='group', shell='default-shell', publicKeys=[])
```

### Get public scripts
```python
pubscripts = wd.get_pubscripts()
```

### Get public scripts for a server
```python
pubscripts = wd.get_serverscripts()
```

### Create a server script
```python
res = wd.create_serverscript(serverSlug, scriptId, path, makeScriptExecutable=False, executeImmediately=False)
```

### Get a server script by ID
```python
res = wd.get_serverscript(serverSlug, scriptId)
```

### Delete a server script ID
```python
wd.delete_serverscript(serverSlug, scriptId)
```

### Execute a server script
```python
res = wd.execute_serverscript(serverSlug, scriptId)
```

### Metrics
Get all metrics.

```python
res = wd.get_server_metrics(serverSlug)
```

Or get instant metrics.

```python
res = wd.get_instant_metrics(serverSlug)
```

### Get server snapshots
```python
res = wd.get_snapshots(serverSlug)
```

### Create a server snapshot
```python
res = wd.create_snapshots(serverSlug, name)
```

### Get a snapshot by ID
```python
res = wd.get_snapshot(serverSlug, snapshotId)
```

### Delete a snapshot by ID
```python
wd.delete_snapshot(serverSlug, snapshotId)
```

### Restore a snapshot
```python
res = wd.restore_snapshot(serverSlug, snapshotId)
```

### Get list of hooks
```python
res = wd.get_hooks()
```

### Get a hook by ID
```python
res = wd.get_hook(hookId)
```

### Delete a hook by ID
```python
wd.delete_hook(hookId)
```

### Create a hook
```python
res = wd.create_hook(hookType, hookValue)
```

### Get events
```python
res = wd.get_events()
```
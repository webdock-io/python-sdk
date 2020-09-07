import requests, json
from .exceptions import ValidationException, WebdockException

class Webdock:
    def __init__(self, apiToken):
        self.baseurl = 'https://api.webdock.io/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(apiToken),
            'X-Client': 'webdock-python-sdk/v1.0.0'
        }
        self.endpoints = {
            'ping': 'ping',
            'servers': 'servers',
            'locations': 'locations',
            'profiles': 'profiles',
            'images': 'images',
            'pubkeys': 'account/publicKeys',
            'scripts': 'scripts',
            'hooks': 'hooks',
            'events': 'events'
        }
        self.params = {}
        self.expectsRaw = False

    # Send API call's response
    def send_response(self, res, json=True):
        if res.status_code in [200, 201, 202, 418]:
            if self.expectsRaw:
                return res.content
            else:
                if json:
                    return {
                        'status': res.status_code,
                        'data': res.json()
                    }
                else:
                    return True
        else:
            raise WebdockException('{} Error: {}'.format(res.status_code, res.reason))

    # Make an API request
    def make_request(self, endpoint, requestType='GET', data=None):
        if requestType == 'GET':
            res = requests.get('{}/{}'.format(self.baseurl, endpoint), params=self.params, headers=self.headers)
        elif requestType == 'POST':
            res = requests.post('{}/{}'.format(self.baseurl, endpoint), data=json.dumps(data), headers=self.headers)
        elif requestType == 'PATCH':
            res = requests.patch('{}/{}'.format(self.baseurl, endpoint), data=json.dumps(data), headers=self.headers)
        elif requestType == 'DELETE':
            res = requests.delete('{}/{}'.format(self.baseurl, endpoint), headers=self.headers)
            return self.send_response(res, False)
        return self.send_response(res)
    
    # Ping the API
    def ping(self):
        return self.make_request(self.endpoints.get('ping'))

    # Get servers
    def servers(self):
        return self.make_request(self.endpoints.get('servers'))
    
    # Provision a new server
    def provision_server(self, data):
        for field in ['name', 'slug', 'locationId', 'profileSlug', 'imageSlug']:
            if field not in data:
                raise ValidationException('Required fields are missing.')
        return self.make_request(self.endpoints.get('servers'), requestType='POST', data=data)
    
    # Get a server by slug
    def get_server(self, slug):
        return self.make_request('{}/{}'.format(self.endpoints.get('servers'), slug))

    # Patch a server
    def patch_server(self, slug, data):
        required = ['name', 'description', 'nextActionDate', 'notes']
        for required_field in required:
            if required_field not in data:
                raise ValidationException(f'Required field {required_field} is missing.')
        return self.make_request(endpoint='{}/{}'.format(self.endpoints.get('servers'), slug), requestType='PATCH', data=data)
    
    # Delete a server
    def delete_server(self, slug):
        return self.make_request(endpoint='{}/{}'.format(self.endpoints.get('servers'), slug), requestType='DELETE')

    # Server action
    def server_action(self, serverSlug, action, data={}):
        supported_actions = ['start', 'stop', 'reboot', 'suspend', 'reinstall', 'snapshot', 'restore', 'resize/dryrun', 'resize']
        if action not in supported_actions:
            raise ValidationException(f'The action {action} is not supported.')
        
        if action == 'reinstall':
            if not data.get('snapshotId'):
                raise ValidationException('The field snapshotId is required')
        
        if action in ['resize', 'resize/dryrun']:
            if not data.get('profileSlug'):
                raise ValidationException('The field profileSlug is required.')
        
        if action in ['snapshot', 'restore']:
            if not data.get('snapshotId'):
                raise ValidationException('The field snapshotId is required.')
        
        return self.make_request(endpoint='{}/{}/actions/{}'.format(self.endpoints.get('servers'), serverSlug, action), requestType='POST')

    # Get server locations
    def get_locations(self):
        return self.make_request(self.endpoints.get('locations'))
    
    # Get profiles
    def get_profiles(self, location):
        self.params['locationId'] = location
        return self.make_request(self.endpoints.get('profiles'))
    
    # Get images
    def get_images(self):
        return self.make_request(self.endpoints.get('images'))
    
    # Public keys
    def get_pubkeys(self):
        return self.make_request(self.endpoints.get('pubkeys'))
    
    # Create a public key
    def create_key(self, keyName, publicKey):
        data = {
            'name': keyName,
            'publicKey': publicKey
        }
        return self.make_request(self.endpoints.get('pubkeys'), requestType='POST', data=data)
    
    # Delete a public key
    def delete_key(self, keyId):
        return self.make_request('{}/{}'.format(self.endpoints.get('pubkeys'), keyId), 'DELETE')
    
    # Get shell users of a server
    def get_shellusers(self, serverSlug):
        return self.make_request('{}/{}/shellUsers'.format(self.endpoints.get('servers'), serverSlug))
    
    # Create a shell user
    def create_shelluser(self, serverSlug, username, password, group='sudo', shell='/bin/bash', publicKeys=[]):
        data = {
            'username': username,
            'password': password,
            'group': group,
            'shell': shell,
            'publicKeys': publicKeys
        }
        return self.make_request('{}/{}/shellUsers'.format(self.endpoints.get('servers'), serverSlug), requestType='POST', data=data)
    
    # Delete a shell user
    def delete_shelluser(self, serverSlug, shellUserId):
        return self.make_request('{}/{}/shellUsers/{}'.format(self.endpoints.get('servers'), serverSlug, shellUserId), requestType='DELETE')
    
    # Update a shell user
    def update_shelluser(self, serverSlug, shellUserId, username, password, group='sudo', shell='/bin/bash', publicKeys=[]):
        data = {
            'username': username,
            'password': password,
            'group': group,
            'shell': shell,
            'publicKeys': publicKeys
        }
        return self.make_request('{}/{}/shellUsers.{}'.format(self.endpoints.get('servers'), serverSlug, shellUserId), requestType='PATCH', data=data)
    
    # Get public scripts
    def get_pubscripts(self):
        return self.make_request(self.endpoints.get('scripts'))
    
    # Get server scripts
    def get_serverscripts(self, serverSlug):
        return self.make_request('{}/{}/scripts'.format(self.endpoints.get('servers'), serverSlug))
    
    # Create a server script
    def create_serverscript(self, serverSlug, scriptId, path, makeScriptExecutable=False, executeImmediately=False):
        data = {
            'scriptId': scriptId,
            'path': path,
            'makeScriptExecutable': makeScriptExecutable,
            'executeImmediately': executeImmediately
        }
        return self.make_request('{}/{}/scripts'.format(self.endpoints.get('servers'), serverSlug), requestType='POST', data=data)
    
    # Get a server script by ID
    def get_serverscript(self, serverSlug, scriptId):
        return self.make_request('{}/{}/scripts/{}'.format(self.endpoints.get('servers'), serverSlug, scriptId))
    
    # Delete a server script by ID
    def delete_serverscript(self, serverSlug, scriptId):
        return self.make_request('{}/{}/scripts/{}'.format(self.endpoints.get('servers'), serverSlug, scriptId), requestType='DELETE')
    
    # Execute a server script
    def execute_serverscript(self, serverSlug, scriptId):
        return self.make_request('{}/{}/scripts/{}/execute'.format(self.endpoints.get('servers'), serverSlug, scriptId), requestType='POST')
    
    # Fetch a file from the server
    def fetch_file(self, serverSlug, filePath):
        self.expectsRaw = True
        return self.make_request('{}/{}/fetchFile'.format(self.endpoints.get('servers'), serverSlug), data={'filePath': filePath}, requestType='POST')

    # Get snapshots of a server
    def get_snapshots(self, serverSlug):
        return self.make_request('{}/{}/snapshots'.format(self.endpoints.get('servers'), serverSlug))
    
    # Create a snapshot of a server
    def create_snapshots(self, serverSlug, name):
        data = {
            'name': name
        }
        return self.make_request('{}/{}/snapshots'.format(self.endpoints.get('servers'), serverSlug), requestType='POST', data=data)
    
    # Get a server snapshot by ID
    def get_snapshot(self, serverSlug, snapshotId):
        return self.make_request('{}/{}/snapshots/{}'.format(self.endpoints.get('servers'), serverSlug, snapshotId))
    
    # Delete a server snapshot by ID
    def delete_snapshot(self, serverSlug, snapshotId):
        return self.make_request('{}/{}/snapshots/{}'.format(self.endpoints.get('servers'), serverSlug, snapshotId), requestType='DELETE')
    
    # Restore a server snapshot by ID
    def restore_snapshot(self, serverSlug, snapshotId):
        return self.make_request('{}/{}/snapshots/{}/restore'.format(self.endpoints.get('servers'), serverSlug, snapshotId), requestType='DELETE')
    
    # Get server metrics
    def get_server_metrics(self, serverSlug):
        return self.make_request('{}/{}/metrics'.format(self.endpoints.get('servers'), serverSlug))
    
    # Get instant server metrics
    def get_instant_metrics(self, serverSlug):
        return self.make_request('{}/{}/metrics/now'.format(self.endpoints.get('servers'), serverSlug))

    # Get hooks list
    def get_hooks(self):
        return self.make_request(self.endpoints.get('hooks'))
    
    # Get a hook by ID
    def get_hook(self, hookId):
        return self.make_request('{}/{}'.format(self.endpoints.get('hooks'), hookId))

    # Delete a hook by ID
    def delete_hook(self, hookId):
        return self.make_request('{}/{}'.format(self.endpoints.get('hooks'), hookId), requestType='DELETE')

    # Create a hook
    def create_hook(self, hookType, hookValue):
        data = {
            'type': hookType,
            'value': hookValue
        }
        return self.make_request(self.endpoints.get('hooks'), data=data, requestType='POST')
    
    # Get events list
    def get_events(self, callbackId=None, eventType=None):
        if callbackId is None and eventType is None:
            raise ValidationException('Either callbackId or eventType is required')
        if callbackId:
            self.params['callbackId'] = callbackId
        if eventType:
            self.params['eventType'] = eventType
        return self.make_request(self.endpoints.get('events'))
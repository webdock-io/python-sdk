import requests, json

class Webdock:

    def __init__(self, clientId, apiKey):
        self.BaseUrl = 'https://api.serverpilot.io/v1'
        self.Headers = {
            'Content-Type': 'application/json'
        }
        self.endpoints = {
            'servers': 'servers',
            'users': 'sysusers',
            'apps': 'apps',
            'databases': 'dbs',
            'actions': 'actions'
        }

    def send_response(self, res, json=True):
        if res.status_code in [200, 201]:
            if json:
                return res.json()
            else:
                return True
        else:
            raise Exception('{} Error: {}'.format(res.status_code, res.reason))

    def make_request(self, endpoint, requestType='GET', data=None):
        if requestType == 'GET':
            res = requests.get('{}/{}'.format(self.BaseUrl, endpoint), auth=self.Auth)
        elif requestType == 'POST':
            res = requests.post('{}/{}'.format(self.BaseUrl, endpoint), data=json.dumps(data), auth=self.Auth, headers=self.Headers)
        elif requestType == 'DELETE':
            res = requests.delete('{}/{}'.format(self.BaseUrl, endpoint), auth=self.Auth)
        return self.send_response(res)

    # Servers
    def list_servers(self):
        return self.make_request('{}'.format(self.endpoints.get('servers')))

    def create_server(self, data):
        # data = {'name': 'myserver', 'plan': 'business', 'enable_ssh_password_auth': True}
        params = ['name']
        for item in params:
            if not item in data:
                raise Exception('{} is a required parameter.'.format(item))
        return self.make_request('{}'.format(self.endpoints.get('servers')), requestType='POST', data=data)

    def get_server(self, serverId):
        return self.make_request('{}/{}'.format(self.endpoints.get('servers'), serverId))

    def update_server(self, serverId, data):
        # i.e. data = {'firewall': False}
        return self.make_request('{}/{}'.format(self.endpoints.get('servers'), serverId), requestType='POST', data=data)

    def delete_server(self, serverId):
        return self.make_request('{}/{}'.format(self.endpoints.get('servers'), serverId), requestType='DELETE')

    # Sys users
    def list_users(self):
        return self.make_request('{}'.format(self.endpoints.get('users')))

    def create_user(self, serverId, data):
        # data = {'name': 'newsysuser', 'password': 'sysuserpass'}
        params = ['name', 'password']
        for item in params:
            if not item in data:
                raise Exception('{} is a required parameter.'.format(item))
        data['serverid'] = serverId
        return self.make_request('{}'.format(self.endpoints.get('users')), requestType='POST', data=data)

    def get_user(self, userId):
        return self.make_request('{}/{}'.format(self.endpoints.get('users'), userId))

    def delete_user(self, userId):
        return self.make_request('{}/{}'.format(self.endpoints.get('users'), userId), requestType='DELETE')

    def update_user(self, userId, data):
        # data = {'password': 'newpassword'}
        params = ['password']
        for item in params:
            if not item in data:
                raise Exception('{} is a required parameter.'.format(item))
        return self.make_request('{}/{}'.format(self.endpoints.get('users'), userId), requestType='POST', data=data)

    # Apps
    def list_apps(self):
        return self.make_request('{}'.format(self.endpoints.get('apps')))

    def create_app(self, data):
        params = ['name', 'sysuserid', 'runtime']
        for item in params:
            if not item in data:
                raise Exception('{} is a required parameter.'.format(item))
        return self.make_request('{}'.format(self.endpoints.get('apps')), requestType='POST', data=data)

    def get_app(self, appId):
        return self.make_request('{}/{}'.format(self.endpoints.get('apps'), appId))

    def update_app(self, appId, data):
        # i.e. data = {'runtime': 'php7.3'}
        return self.make_request('{}/{}'.format(self.endpoints.get('apps'), appId), requestType='POST', data=data)

    def enable_ssl(self, appId, data=None):
        # data = {'key': 'privateKey', 'cert': 'SSLCertContent', 'cacerts': 'CACertsIfApplicable'}
        if data is None:
            # Use auto-SSL
            data = data={'auto': True}
        return self.make_request('{}/{}/ssl'.format(self.endpoints.get('apps'), appId), requestType='POST', data=data)

    def force_ssl(self, appId):
        return self.make_request('{}/{}/ssl'.format(self.endpoints.get('apps'), appId), requestType='POST', data={'force': True})

    def disable_ssl(self, appId):
        return self.make_request('{}/{}/ssl'.format(self.endpoints.get('apps'), appId), requestType='DELETE')

    def delete_app(self, appId):
        return self.make_request('{}/{}'.format(self.endpoints.get('apps'), appId), requestType='DELETE')

    # Databases
    def list_databases(self):
        return self.make_request('{}'.format(self.endpoints.get('databases')))

    def create_database(self, data):
        params = ['appid', 'name', 'user']
        # user must be a dictionary: {'user': {'name': 'dbusername', 'password': 'dbpassword'}}
        for item in params:
            if not item in data:
                raise Exception('{} is a required parameter.'.format(item))
        return self.make_request('{}'.format(self.endpoints.get('databases')), requestType='POST', data=data)

    def update_database(self, databaseId, data):
        params = ['user']
        # user must be a dictionary: {'user': {'id': 'userId', 'password': 'newdbpassword'}}
        for item in params:
            if not item in data:
                raise Exception('{} is a required parameter.'.format(item))
        return self.make_request('{}/{}'.format(self.endpoints.get('databases'), databaseId), requestType='POST', data=data)

    def get_database(self, databaseId):
        return self.make_request('{}/{}'.format(self.endpoints.get('databases'), databaseId))

    def delete_database(self, databaseId):
        return self.make_request('{}/{}'.format(self.endpoints.get('databases'), databaseId), requestType='DELETE')

    def check_action(self, actionId):
        return self.make_request('{}/{}'.format(self.endpoints.get('actions'), actionId))

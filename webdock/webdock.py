import requests, json

class Webdock:

    def __init__(self, apiToken):
        self.baseurl = 'https://api.webdock.io'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(apiToken)
        }
        self.endpoints = {
            'ping': 'ping',
            'servers': 'servers'
        }

    # Send API call's response
    def send_response(self, res, json=True):
        if res.status_code in [200, 201]:
            if json:
                return res.json()
            else:
                return True
        else:
            raise Exception('{} Error: {}'.format(res.status_code, res.reason))

    # Make an API request
    def make_request(self, endpoint, requestType='GET', data=None):
        if requestType == 'GET':
            res = requests.get('{}/{}'.format(self.baseurl, endpoint), headers=self.headers)
        elif requestType == 'POST':
            res = requests.post('{}/{}'.format(self.baseurl, endpoint), data=json.dumps(data), headers=self.headers)
        elif requestType == 'PATCH':
            res = requests.patch('{}/{}'.format(self.baseurl, endpoint), data=json.dumps(data), headers=self.headers)
        elif requestType == 'DELETE':
            res = requests.delete('{}/{}'.format(self.baseurl, endpoint), headers=self.headers)
        return self.send_response(res)
    
    # Ping the API
    def ping(self):
        return self.make_request(self.endpoints.get('ping'))

    # Get servers
    def servers(self):
        return self.make_request(self.endpoints.get('servers'))
    
    # Get a server by slug
    def get_server(self, slug):
        return self.make_request('{}/{}'.format(self.endpoints.get('servers'), slug))
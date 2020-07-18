import requests, json

class Webdock:

    def __init__(self, apiToken):
        self.BaseUrl = 'https://api.webdock.io'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(apiToken)
        }
        self.endpoints = {}

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
            res = requests.get('{}/{}'.format(self.BaseUrl, endpoint), headers=self.headers)
        elif requestType == 'POST':
            res = requests.post('{}/{}'.format(self.BaseUrl, endpoint), data=json.dumps(data), headers=self.headers)
        elif requestType == 'DELETE':
            res = requests.delete('{}/{}'.format(self.BaseUrl, endpoint), headers=self.headers)
        return self.send_response(res)

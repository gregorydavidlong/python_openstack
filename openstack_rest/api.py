import httplib, urllib
import json
import re

class OpenstackRESTConnection(object):

    # Takes a username and password for authentication
    def __init__(self, username, password, keystone_url):
        self.token = ''
        self.username = username
        self.password = password
        self.keystone_url = keystone_url
        self.nova_server_url = ''
        self.nova_dirs_url = ''
        self.nova_port = ''

    def _make_json_request(self, server_url, request_method, dirs_url, json_request):
       conn = httplib.HTTPConnection(server_url)
       conn.request(request_method, dirs_url, json_request, {'Content-type': 'application/json'})
       return json.loads(conn.getresponse().read())

    def _make_request(self, server_url, request_method, dirs_url):
        conn = httplib.HTTPConnection(server_url)
        conn.port = self.nova_port
        headers = {'X-Auth-Token': self.token, 'Content-type': 'application/json'}
        conn.request(request_method, dirs_url, None, headers)
        return json.loads(conn.getresponse().read())

    # Authenticate by getting a token
    def authenticate(self):
        json_request = json.dumps({
            'auth': {
                'passwordCredentials': {
                    'username': self.username,
                    'password': self.password
                    }
                }
            })
        response = self._make_json_request(
                self.keystone_url, "POST", "/v2.0/tokens",
                json_request)

        #set token
        try:
            self.token = response['access']['token']['id']
            regex = 'http://(.+):(.+?)(/.+)'
            endpoint = response['access']['serviceCatalog'][2]['endpoints'][0]['publicURL']

            self.nova_server_url = re.search(regex, endpoint).group(1)
            self.nova_port = int(re.search(regex, endpoint).group(2))
            self.nova_dirs_url = re.search(regex, endpoint).group(3)

        except KeyError:
            raise InvalidCredentialsException(response)
        return True

    # Get a collection of images
    def get_images(self):
        server_url = self.nova_server_url
        return self._make_request(server_url, "GET",
            self.nova_dirs_url + "/images")['images']


class InvalidCredentialsException(Exception):
    pass

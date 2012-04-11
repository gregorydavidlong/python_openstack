import httplib, urllib
import json

class OpenstackRESTConnection(object):

    # Takes a username and password for authentication
    def __init__(self, username, password, keystone_url):
        self.token = ''
        self.username = username
        self.password = password
        self.keystone_url = keystone_url
        self.nova_url = ''

    def _make_json_request(self, server_url, request_method, dirs_url, json_request):
       conn = httplib.HTTPConnection(server_url)
       conn.request(request_method, dirs_url, json_request, {'Content-type': 'application/json'})
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
            self.nova_url = response['access']['serviceCatalog'][2]['endpoints'][0]['publicURL']
        except KeyError:
            raise InvalidCredentialsException(response)
        return response

    def list_images(self):
        server_url = self.nova_url
        conn = httplib.HTTPConnection(server_url)

        
        

class InvalidCredentialsException(Exception):
    pass

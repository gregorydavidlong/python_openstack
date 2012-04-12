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

    def _make_json_request_without_token(self, server_url, request_method, dirs_url, json_request):
       conn = httplib.HTTPConnection(server_url)
       conn.request(request_method, dirs_url, json_request, {'Content-type': 'application/json'})
       return json.loads(conn.getresponse().read())
    
    def _make_json_request(self, server_url, port, request_method, dirs_url, json_request):
       conn = httplib.HTTPConnection(server_url)
       conn.port = port
       conn.request(request_method, dirs_url, json_request, 
               {'X-Auth-Token': self.token, 
                   'Content-type': 'application/json',
                   'Accept': 'application/json'})
       return json.loads(conn.getresponse().read())

    def _make_request(self, server_url, port, request_method, dirs_url):
        conn = httplib.HTTPConnection(server_url)
        conn.port = port
        headers = {'X-Auth-Token': self.token, 
                'Content-type': 'application/json'} 
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
        response = self._make_json_request_without_token(
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
            raise InvalidRequestException(response)
        return True

    # Get a collection of images
    def get_images(self):
        server_url = self.nova_server_url
        return self._make_request(server_url, self.nova_port, "GET", self.nova_dirs_url + "/images")['images']

    # Get the currently running instances
    def get_instances(self):
        server_url = self.nova_server_url
        return self._make_request(server_url, self.nova_port, "GET", self.nova_dirs_url + "/servers")['servers']

    # Get detailed information about a running instance
    def get_instance_details(self, instance_id):
        return self._make_request(self.nova_server_url, self.nova_port, "GET",
                self.nova_dirs_url + "/servers/" + str(instance_id))['server']

    # Get the metadata associated with a currently running instance
    def get_instance_metadata(self, instance_id):
        return self._make_request(self.nova_server_url, self.nova_port, "GET",
                self.nova_dirs_url + "/servers/" + str(instance_id) +
                "/metadata")['metadata']

    def set_instance_metadata(self, instance_id, metadata):
        metadata_wrap = {'metadata': metadata}
        json_request = json.dumps(metadata_wrap)
        return self._make_json_request(
                self.nova_server_url, self.nova_port, "PUT", self.nova_dirs_url + "/servers/" + str(instance_id) + "/metadata",
                json_request)

    def set_instance_name(self, instance_id, name):
        json_request = json.dumps({'server': {'name': name}})
        return self._make_json_request(
                self.nova_server_url, self.nova_port, "PUT", self.nova_dirs_url + "/servers/" +
                str(instance_id), json_request)




class InvalidRequestException(Exception):
    pass

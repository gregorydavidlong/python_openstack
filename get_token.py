#!/usr/bin/env python
# Example Python code to get a token from the NeCTAR cloud

import httplib, urllib
import json
from credentials import USER, PASSWORD

json_string = json.dumps({
    'auth': {
        'passwordCredentials': {
            'username': USER,
            'password': PASSWORD
            }
        }
    })

conn = httplib.HTTPConnection("keystone.rc.nectar.org.au:35357")
conn.request("POST", "/v2.0/tokens", json_string, {'Content-type': 'application/json'})

response = json.loads(conn.getresponse().read())

print 'tenant id:{id}, name:{name}'.format(**response['access']['token']['tenant'])

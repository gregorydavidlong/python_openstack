#!/usr/bin/env python
# Example Python code to test a connection to the NeCTAR cloud

import httplib, urllib
from credentials import USER, PASSWORD

conn = httplib.HTTPConnection("keystone.rc.nectar.org.au:35357")

conn.request("GET", "")

response = conn.getresponse()
print response.status, response.reason

print response.read()

OpenStack Python API
====================

This light-weight OpenStack Python API merely wraps the REST API.

For an example of how to use the api see examples/api_usage.py

Credentials
-----------

You will need to create a credentials.py file with the following variables:

```python
  # Needed to use the API
  USER      = 'myuser@somedomain'     # Just your regular username.
  PASSWORD  = 'MYPASSWORD'      # From the Dashboard/credentials page (in the NeCTAR case it is NOT the password you use to login).
  KEYSTONE_URL = 'keystone.rc.nectar.org.au:5000' # The Keystone URL (this is the default NeCTAR URL)
  
  # These values are only needed if you're planning on running the unit tests. These are usually automatically determined by the API. Here are some examples.
  EXPECTED_NOVA_SERVER_URL = 'nova.rc.nectar.org.au'
  EXPECTED_NOVA_PORT = '8774'
  EXPECTED_NOVA_DIRS_URL = '/v1.1/YOUR_TENANT_ID'
```

Testing
-------

To run the unit tests use (you will need to have nose installed):

  nosetests tests/api_test.py

WARNING: Be aware that, at the moment, the unit tests run against OpenStack using your credentials. The tests do stuff like renaming instances and setting metadata.

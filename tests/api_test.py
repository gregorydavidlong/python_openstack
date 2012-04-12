import openstack_rest.api
import pytest
from nose.tools import with_setup
from openstack_rest.api import OpenstackRESTConnection
from openstack_rest.api import InvalidCredentialsException
from credentials import USER, PASSWORD, KEYSTONE_URL, EXPECTED_NOVA_SERVER_URL, EXPECTED_NOVA_DIRS_URL

class TestOpenstackRESTConnection(object):
    def setup(self):
        self.connection = OpenstackRESTConnection(
                USER, PASSWORD, KEYSTONE_URL) 

    def teardown(self):
        print "tear-down"

    @with_setup(setup, teardown)
    def test_init(self):
        assert self.connection != None
        assert self.connection.username == USER
        assert self.connection.password == PASSWORD
        assert self.connection.keystone_url == KEYSTONE_URL
    
    # Authenticate with correct credentials
    def testAuthenticate(self):
        assert self.connection.authenticate()
        assert self.connection.token != ''
        assert self.connection.nova_server_url == EXPECTED_NOVA_SERVER_URL
        assert self.connection.nova_dirs_url == EXPECTED_NOVA_DIRS_URL

    # Authenticate with incorrect credentials
    def testAuthenticateWithInvalidCredentials(self):
        connection = openstack_rest.api.OpenstackRESTConnection(
                'invalid_username', 'invalid_password', KEYSTONE_URL)
        assert connection != None
        with pytest.raises(InvalidCredentialsException):
            connection.authenticate()

    def testGetImages(self):
        self.connection.authenticate()
        images = self.connection.get_images() 
        assert images != None
        assert len(images) > 0


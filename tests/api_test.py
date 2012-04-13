import unittest
from nose.tools import with_setup, raises
from openstack_rest.api import OpenstackRESTConnection, InvalidRequestException
from credentials import USER, PASSWORD, KEYSTONE_URL, EXPECTED_NOVA_SERVER_URL, EXPECTED_NOVA_DIRS_URL

class TestOpenstackRESTConnection(unittest.TestCase):
    def setUp(self):
        self.connection = OpenstackRESTConnection(
                USER, PASSWORD, KEYSTONE_URL)
        self.connection.authenticate()

    def test_init(self):
        self.assertNotEqual(self.connection, None)
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
    @raises(InvalidRequestException)
    def testAuthenticateWithInvalidCredentials(self):
        connection = OpenstackRESTConnection(
                'invalid_username', 'invalid_password', KEYSTONE_URL)
        assert connection is not None
        connection.authenticate()

    def testGetImages(self):
        images = self.connection.get_images() 
        assert images is not None
        assert len(images) > 0

    def testGetInstances(self):
        instances = self.connection.get_instances()
        assert instances is not None
        assert len(instances) >= 0

    def testGetInstanceDetails(self):
        #relies on there being current instances running
        instance_id = self.connection.get_instances()[0]['id']
        details = self.connection.get_instance_details(instance_id)
        assert details is not None

    def testGetInstanceMetadata(self):
        #relies on there being current instances running
        instance_id = self.connection.get_instances()[0]['id']
        metadata = self.connection.get_instance_metadata(instance_id)
        assert metadata is not None

    def testSetAndGetInstanceMetadata(self):
        #relies on there being current instances running
        #WARNING: This will modify your running instances
        instance_id = self.connection.get_instances()[0]['id']
        metadata = {'unit_test_key': 'unit_test_value'}
        self.connection.set_instance_metadata(instance_id, metadata)
        metadata_retrieved = self.connection.get_instance_metadata(instance_id)
        assert metadata_retrieved['unit_test_key'] == 'unit_test_value'

    def testSetAndGetMultipleInstanceMetadata(self):
        #relies on there being current instances running
        #WARNING: This will modify your running instances
        instance_id = self.connection.get_instances()[0]['id']
        metadata = {'one': 'a',
                'two': 'b',
                'three': 'c'}
        self.connection.set_instance_metadata(instance_id, metadata)
        metadata_retrieved = self.connection.get_instance_metadata(instance_id)
        assert metadata_retrieved['one'] == 'a'
        assert metadata_retrieved['two'] == 'b'
        assert metadata_retrieved['three'] == 'c'
        

    def testRenameInstance(self):
        #relies on there being current instances running
        #WARNING: This will modify your running instances
        instance = self.connection.get_instances()[0]
        current_instance_name = instance['name']
        new_instance_name = 'New Instance Name'
        self.connection.set_instance_name(instance['id'], new_instance_name)
        actual_instance_name = self.connection.get_instance_details(instance['id'])['name']
        assert actual_instance_name == new_instance_name
        #Change the name back
        self.connection.set_instance_name(instance['id'], current_instance_name)
        actual_instance_name = self.connection.get_instance_details(instance['id'])['name']
        assert actual_instance_name == current_instance_name

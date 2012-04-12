from openstack_rest.api import OpenstackRESTConnection
from openstack_rest.api import InvalidCredentialsException
from credentials import USER, PASSWORD, KEYSTONE_URL, EXPECTED_NOVA_SERVER_URL, EXPECTED_NOVA_DIRS_URL

c = OpenstackRESTConnection(USER, PASSWORD, KEYSTONE_URL)
c.authenticate()
images = c.get_images()
instances = c.get_instances()
instance = c.get_instance_details(instances[0]['id'])

metadata = c.get_instance_metadata(instances[0]['id'])

metadata_to_set = {'some_key': 'some_value'}
c.set_instance_metadata(instances[0]['id'], metadata_to_set)


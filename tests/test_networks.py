# Copyright 2015 Hewlett-Packard Development Company, L.P
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import helpers
from pages import loginpage
from pages.compute import instancespage
from pages.network import networkspage
from pages.compute import volumespage

class TestNetworks(helpers.TestCase):
    """This is a basic network test:
    * checks that user is able to create a network
    * after successful network creation
    * checks that the user is able to delete the network without error
    """

    NETWORK_NAME = helpers.gen_random_resource_name("Network")
    SUBNET_NAME = helpers.gen_random_resource_name("Subnet")
    INSTANCE_NAME = helpers.gen_random_resource_name("Instance")
    VOLUME_NAME = helpers.gen_random_resource_name("Volume")

    def test_network_and_subnet_creation(self):
        network_pg = networkspage.NetworkPage(self.driver, self.CONFIG)
        network_pg.go_to_networks_page()
	network_pg.click_on_new_button()
        network_pg.create_network_and_subnet(self.NETWORK_NAME, self.SUBNET_NAME)
        volume_pg = volumespage.VolumePage(self.driver, self.CONFIG)
        volume_pg.go_to_volumes_page()
        volume_pg.click_on_new_button()
        volume_pg.create_volume_with_image_source(self.VOLUME_NAME)
        volume_pg.create_success_or_failure()
	instance_pg = instancespage.InstancePage(self.driver, self.CONFIG)
	instance_pg.go_to_instances_page()
	instance_pg.click_on_new_button()
	instance_pg.instance_details(self.VOLUME_NAME, self.INSTANCE_NAME)
	instance_pg.flavor_details()
	instance_pg.access_and_security()
	instance_pg.select_created_network()
	instance_pg.post_creation_and_advanced_options()
	instance_pg.launch_success_or_failure()
	instance_pg.associate_floating_ip(self.INSTANCE_NAME)
	instance_pg.delete_instance(self.INSTANCE_NAME)
        network_pg.go_to_networks_page()
	network_pg.delete_network(self.NETWORK_NAME)

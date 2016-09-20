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
from pages.compute import volumespage

class TestInstances(helpers.TestCase):
    """This is a basic instance test:
    * checks that user is able to create a instance 
    * using boot from volume
    * after successful instance creation
    * checks that the user is able to delete the instance without error
    """

    VOLUME_NAME = helpers.gen_random_resource_name("Volume")
    INSTANCE_NAME = helpers.gen_random_resource_name("Instance")

    def test_instance_creation(self):
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
	instance_pg.networking()
	instance_pg.post_creation_and_advanced_options()
	instance_pg.launch_success_or_failure()
	instance_pg.associate_floating_ip(self.INSTANCE_NAME)
	instance_pg.delete_instance(self.INSTANCE_NAME)

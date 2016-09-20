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
import time
from pages import loginpage
from pages.compute import volumespage

class TestVolumes(helpers.TestCase):
    """This is a basic volume test:
    * checks that user is able to create a volume
    * after successful volume creation
    * checks that the user is able to delete the volume without error
    """
    VOLUME_NAME = helpers.gen_random_resource_name("volume")
    VOLUME_NAME_ALT = helpers.gen_random_resource_name("volume-alt")

    def test_volume_with_no_source(self):
        volume_pg = volumespage.VolumePage(self.driver, self.CONFIG)
        volume_pg.go_to_volumes_page()
	volume_pg.click_on_new_button()
        volume_pg.create_volume_with_no_source(self.VOLUME_NAME)
	volume_pg.delete_volume(self.VOLUME_NAME)

    def test_volume_with_image_as_source(self):
        volume_pg = volumespage.VolumePage(self.driver, self.CONFIG)
        volume_pg.go_to_volumes_page()
	volume_pg.click_on_new_button()
        volume_pg.create_volume_with_image_source(self.VOLUME_NAME_ALT)
	volume_pg.delete_volume(self.VOLUME_NAME_ALT)

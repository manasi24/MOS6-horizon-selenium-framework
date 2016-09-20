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



import time
from selenium.webdriver.common import by
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from pages import pageobject

class VolumePage(pageobject.PageObject):
    _new_button_locator = (by.By.ID, 'volumes__action_create')
    _volume_name_field_locator = (by.By.ID, 'id_name')
    _volume_source_field_locator = (by.By.ID, 'id_volume_source_type')
    _image_source_field_locator = (by.By.ID, 'id_image_source')
    _volume_size_field_locator = (by.By.ID, 'id_size')
    _create_volume_button_locator = (by.By.CSS_SELECTOR,
                               "input[value='Create Volume'][type='submit']")
    _status_locator = (by.By.XPATH,
     "//body/div[1]/div[2]/div[3]/div[3]/div/div/form/table/tbody/tr[1]/td[5]")
    _delete_button_locator = (by.By.ID, "volumes__action_delete")
    _confirm_delete_locator = (by.By.CSS_SELECTOR, "a[href='#'].btn.btn-primary")
    _select_delete_item_locator = (by.By.XPATH, 
    "//body/div[1]/div[2]/div[3]/div[3]/div/div/form/table/tbody/tr[1]/td[1]/input")

    def __init__(self, driver, conf):
        super(VolumePage, self).__init__(driver, conf)
        self.volume_url = self.conf.volume.url
        self._page_title = "Volumes"

    @property
    def new_button(self):
        return self._get_element(*self._new_button_locator)

    @property
    def volume_name(self):
        return self._get_element(*self._volume_name_field_locator)

    @property
    def volume_source(self):
        return self._get_element(*self._volume_source_field_locator)

    @property
    def image_source(self):
	return self._get_element(*self._image_source_field_locator)

    @property
    def volume_size(self):
        return self._get_element(*self._volume_size_field_locator)
    
    @property
    def create_volume_button(self):
        return self._get_element(*self._create_volume_button_locator)

    @property
    def status(self):
        return self._get_element(*self._status_locator)

    @property
    def delete_button(self):
        return self._get_element(*self._delete_button_locator)

    @property
    def confirm_delete_button(self):
        return self._get_element(*self._confirm_delete_locator)

    @property
    def select_delete_item_field(self):
	return self._get_element(*self._select_delete_item_locator)

    def _click_on_volume_button(self):
        self.create_volume_button.click()

    def go_to_volumes_page(self):
        self.driver.get(self.volume_url)

    def click_on_new_button(self):
	self.new_button.click()

    def create_volume_with_no_source(self, random_volume_name):
	self._fill_field_element(random_volume_name, self.volume_name)
        self._select_dropdown_by_value("no_source_type", self.volume_source)
	self._fill_field_element("2", self.volume_size)
	self._click_on_volume_button()
	self._turn_on_implicit_wait()

    def create_volume_with_image_source(self, random_volume_name):
	os_image_name = self.conf.volume.image_name
	self._fill_field_element(random_volume_name, self.volume_name)
        self._select_dropdown_by_value("image_source", self.volume_source)
	self._select_dropdown(os_image_name, self.image_source)
        self._fill_field_element("10", self.volume_size)
	self._click_on_volume_button()
	self._turn_on_implicit_wait()

    def click_item_to_be_deleted(self):
	self.select_delete_item_field.click()

    def click_on_delete_button(self):
	self.delete_button.click()

    def click_on_confirm_delete_button(self):
	self.confirm_delete_button.click()

    def create_success_or_failure(self):
        self._wait_till_text_present_in_element(self.status, 'Available')
	time.sleep(3)

    def _select_item_to_be_deleted(self, random_volume_name):
        selector = "form > table > tbody > tr[data-display=" + random_volume_name + "] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()

    def delete_volume(self, random_volume_name):
	self.create_success_or_failure()
	self._wait_till_element_is_clickable(self.select_delete_item_field)
	self._select_item_to_be_deleted(random_volume_name)
	self.click_on_delete_button()
	self.click_on_confirm_delete_button()

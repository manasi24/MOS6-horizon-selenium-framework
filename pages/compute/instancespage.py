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
import selenium.webdriver.support.ui as Support
from selenium.common.exceptions import NoSuchElementException
from pages import pageobject

class InstancePage(pageobject.PageObject):
    _new_button_locator = (by.By.ID, 'instances__action_launch')
    _availability_zone_locator = (by.By.ID, 'id_availability_zone')
    _instance_name_field_locator = (by.By.ID, 'id_name')
    _source_type_field_locator = (by.By.ID, 'id_source_type')
    _volume_id_field_locator = (by.By.ID, 'id_volume_id')
    _delete_on_terminate_locator = (by.By.ID, 'id_delete_on_terminate')
    _next_button_locator = (by.By.CSS_SELECTOR, 
                         "button[type='button'].btn.btn-primary.button-next")
    _flavor_type_locator = (by.By.ID, 'id_flavor')
    _keypair_locator = (by.By.ID, 'id_keypair')
    _security_group_locator = (by.By.ID, "id_groups_1")
    _launch_button_locator = (by.By.CSS_SELECTOR,
                         "button[type='submit'].btn.btn-primary.button-final")
    _status_locator = (by.By.XPATH,
	"/html/body/div[1]/div[2]/div[3]/div[3]/form/table/tbody/tr[1]/td[9]")
    _delete_button_locator = (by.By.ID, "instances__action_terminate")
    _confirm_delete_locator = (by.By.CSS_SELECTOR, "a[href='#'].btn.btn-primary")
    _select_delete_item_locator = (by.By.XPATH,
    "/html/body/div[1]/div[2]/div[3]/div[3]/form/table/tbody/tr[1]/td[1]/input")

    def __init__(self, driver, conf):
        super(InstancePage, self).__init__(driver, conf)
        self.instance_url = self.conf.instance.url
	self.flavor_type = self.conf.instance.flavor_type
	self.availability_zone = self.conf.instance.availability_zone
	self.keypair = self.conf.instance.keypair
        self._page_title = "Instances"

    @property
    def new_button(self):
        return self._get_element(*self._new_button_locator)

    @property
    def instance_name(self):
        return self._get_element(*self._instance_name_field_locator)

    @property
    def availability_zone_field(self):
	return self._get_element(*self._availability_zone_locator)

    @property
    def source_type(self):
        return self._get_element(*self._source_type_field_locator)

    @property
    def volume_id(self):
	return self._get_element(*self._volume_id_field_locator)

    @property
    def delete_on_terminate(self):
	return self._get_element(*self._delete_on_terminate_locator)

    @property
    def flavor_field(self):
	return self._get_element(*self._flavor_type_locator)

    @property
    def keypair_field(self):
	return self._get_element(*self._keypair_locator)
 
    @property
    def next_button(self):
	return self._get_element(*self._next_button_locator)

    @property
    def launch_button(self):
        return self._get_element(*self._launch_button_locator)
    
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

    def _click_on_delete_on_terminate(self):
	self.delete_on_terminate.click()

    def _click_on_next_button(self):
	self.next_button.click()

    def _click_on_launch_button(self):
        self.launch_button.click()

    def _click_on_security_groups(self):
	self._get_element(*self._security_group_locator).click()

    def go_to_instances_page(self):
        self.driver.get(self.instance_url)

    def click_on_new_button(self):
	self.new_button.click()

    def instance_details(self, random_volume_name, random_instance_name):
	self._fill_field_element(random_instance_name, self.instance_name)
	self._select_dropdown_by_value(self.availability_zone, self.availability_zone_field)
	self._select_dropdown("Boot from volume", self.source_type)
	self._select_dropdown(random_volume_name + " - 10 GB (Volume)", self.volume_id)
	self._click_on_delete_on_terminate()
	self._click_on_next_button()

    def flavor_details(self):
	self._select_dropdown(self.flavor_type, self.flavor_field)
	self._click_on_next_button()

    def access_and_security(self):
	self._select_dropdown(self.keypair, self.keypair_field)
	self._click_on_security_groups()
	self._click_on_next_button()

    def networking(self):
        self._click_on_next_button()

    def select_created_network(self):
	net_list = self._get_element(by.By.XPATH,"//body/div[3]/div/form/div/div/div[2]/div/fieldset[4]/table[1]/tbody/tr/td[1]/ul[2]/li[1]/a")
	net_list.click()
	self._click_on_next_button()

    def post_creation_and_advanced_options(self):
	self._click_on_next_button()
	self._click_on_launch_button() 

    def launch_success_or_failure(self):
	self._wait_till_text_present_in_element(self.status, 'Active')
	time.sleep(3)

    def associate_floating_ip(self, random_instance_name):
	selector = "form > table > tbody > tr[data-display=" + random_instance_name + "] > td.actions_column > div > a:nth-child(2)"
        action_list = self._get_element(by.By.CSS_SELECTOR, selector)
        action_list.click()
	time.sleep(5)
	floating_ip = self._get_element(by.By.LINK_TEXT, "Associate Floating IP")
	floating_ip.click()

	instance_id = self._get_element(by.By.ID,"id_instance_id")
	select_instance_id = Support.Select(instance_id)
	select_instance_id.select_by_index(1)

    	#select floating ip
	element = self._get_element(by.By.ID, "id_ip_id")
        self._wait_till_element_is_clickable(element)
        select_floating_ip = Support.Select(element)
	for o in select_floating_ip.options:
            if o.text == "Select an IP address":
                select_floating_ip.select_by_index(1)
		#associate
		associate_button = self._get_element(by.By.CSS_SELECTOR, "input[type='submit'][value='Associate']")
                associate_button.click()
                break
            elif o.text == "No floating IP addresses allocated":
                select_floating_ip.select_by_index(0)
                add_floating_ip = self._get_element(by.By.XPATH, 
		    "//body/div[3]/div/form/div/div/div[2]/div/fieldset/table/tbody/tr/td[1]/div[1]/div/div/span/a")
                add_floating_ip.click()
		#allocate
                allocate_ip = self._get_element(by.By.CSS_SELECTOR, "input[type='submit'][value='Allocate IP']")
                allocate_ip.click()
		#associate
                associate_button = self._get_element(by.By.CSS_SELECTOR, "input[type='submit'][value='Associate']")
                associate_button.click()
	        break

    def click_item_to_be_deleted(self):
        self.select_delete_item_field.click()

    def click_on_delete_button(self):
        self.delete_button.click()

    def click_on_confirm_delete_button(self):
        self.confirm_delete_button.click()

    def _select_item_to_be_deleted(self, random_instance_name):
        selector = "form > table > tbody > tr[data-display='" + random_instance_name + "'] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()

    def delete_instance(self, random_instance_name):
        self._wait_till_element_is_clickable(self.select_delete_item_field)
	time.sleep(5)
        self._select_item_to_be_deleted(random_instance_name)
        self.click_on_delete_button()
        self.click_on_confirm_delete_button()

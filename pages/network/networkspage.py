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

class NetworkPage(pageobject.PageObject):
    _new_button_locator = (by.By.ID, 'networks__action_create')
    _network_name_field_locator = (by.By.ID, 'id_net_name')
    _admin_state_field_locator = (by.By.ID, 'id_admin_state')
    _subnet_name_field_locator = (by.By.ID, 'id_subnet_name')
    _network_address_locator = (by.By.ID, 'id_cidr')
    _next_button_locator = (by.By.CSS_SELECTOR, 
                         "button[type='button'].btn.btn-primary.button-next")
    _ip_version_field_locator = (by.By.ID, 'id_ip_version')
    _gateway_ip_field_locator = (by.By.ID, 'id_gateway_ip')
    _create_button_locator = (by.By.CSS_SELECTOR,
                         "button[type='submit'].btn.btn-primary.button-final")
    _delete_button_locator = (by.By.ID, "networks__action_delete")
    _confirm_delete_locator = (by.By.CSS_SELECTOR, "a[href='#'].btn.btn-primary")
    _select_delete_item_locator = (by.By.XPATH,
    "/html/body/div[1]/div[2]/div[3]/div[3]/form/table/tbody/tr[1]/td[1]/input")

    def __init__(self, driver, conf):
        super(NetworkPage, self).__init__(driver, conf)
        self.network_url = self.conf.network.url
        self.network_address = self.conf.network.network_address
        self.gateway_ip = self.conf.network.gateway_ip
        self.ip_version = self.conf.network.ip_version
        self._page_title = "Networks"

    @property
    def new_button(self):
        return self._get_element(*self._new_button_locator)

    @property
    def network_name(self):
        return self._get_element(*self._network_name_field_locator)

    @property
    def admin_state(self):
        return self._get_element(*self._admin_state_field_locator)

    @property
    def subnet_name(self):
	return self._get_element(*self._subnet_name_field_locator)

    @property
    def network_address_field(self):
	return self._get_element(*self._network_address_locator)

    @property
    def ip_version_field(self):
	return self._get_element(*self._ip_version_field_locator)

    @property
    def gateway_ip_field(self):
        return self._get_element(*self._gateway_ip_field_locator)

    @property
    def next_button(self):
	return self._get_element(*self._next_button_locator)

    @property
    def create_button(self):
        return self._get_element(*self._create_button_locator)
    
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

    def _click_on_create_button(self):
        self.create_button.click()

    def go_to_networks_page(self):
        self.driver.get(self.network_url)

    def click_on_new_button(self):
	self.new_button.click()

    def create_network_and_subnet(self, random_network_name, random_subnet_name):
        self._fill_field_element(random_network_name, self.network_name)
        self._select_dropdown_by_value("True", self.admin_state)
	self._click_on_next_button()
        self._fill_field_element(random_subnet_name, self.subnet_name)
        self._fill_field_element(self.network_address, self.network_address_field)
        self._select_dropdown(self.ip_version, self.ip_version_field)
        self._fill_field_element(self.gateway_ip, self.gateway_ip_field)
	self._click_on_next_button()
	self._click_on_create_button()

    def click_item_to_be_deleted(self):
        self.select_delete_item_field.click()

    def click_on_delete_button(self):
        self.delete_button.click()

    def click_on_confirm_delete_button(self):
        self.confirm_delete_button.click()

    def _select_item_to_be_deleted(self, random_network_name):
        selector = "form > table > tbody > tr[data-display='" + random_network_name + "'] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()

    def delete_network(self, random_network_name):
        self._wait_till_element_is_clickable(self.select_delete_item_field)
	time.sleep(5)
        self._select_item_to_be_deleted(random_network_name)
        self.click_on_delete_button()
        self.click_on_confirm_delete_button()

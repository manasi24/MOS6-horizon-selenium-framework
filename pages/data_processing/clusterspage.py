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

class ClusterPage(pageobject.PageObject):
    _new_button_locator = (by.By.ID, 'clusters__action_create')
    _plugin_field_locator = (by.By.ID,'id_plugin_name')
    _hadoop_version_field_locator = (by.By.ID,'id_vanilla_version')
    _cluster_name_locator = (by.By.ID,'id_cluster_name')
    _slave_count_locator = (by.By.ID, 'count_2')
    _cluster_template_field_locator = (by.By.ID, 'id_cluster_template')
    _base_image_locator = (by.By.ID, 'id_image')
    _keypair_field_locator = (by.By.ID, 'id_keypair')
    _network_field_locator = (by.By.ID, 'id_neutron_management_network')
    _create_button_locator = (by.By.CSS_SELECTOR,
                         "input[value='Create'][type='submit']")
    _status_locator = (by.By.XPATH,
	"/html/body/div[1]/div[2]/div[3]/div[3]/div/form/table/tbody/tr/td[3]")
    _delete_button_locator = (by.By.ID, "clusters__action_delete")
    _confirm_delete_locator = (by.By.CSS_SELECTOR, "a[href='#'].btn.btn-primary")
    _select_delete_item_locator = (by.By.XPATH,
    "//body/div[1]/div[2]/div[3]/div[3]/div/form/table/tbody/tr/td[1]/input")

    def __init__(self, driver, conf):
        super(ClusterPage, self).__init__(driver, conf)
        self.cluster_url = self.conf.cluster.cluster_url
	self.plugin_name = self.conf.cluster.plugin_name
	self.hadoop_version = self.conf.cluster.hadoop_version
	self.image_name = self.conf.cluster.base_image
	self.keypair = self.conf.instance.keypair
	self.network = self.conf.cluster.network
        self._page_title = "Data Processing"

    @property
    def new_button(self):
        return self._get_element(*self._new_button_locator)

    @property
    def plugin_field(self):
        return self._get_element(*self._plugin_field_locator)

    @property
    def hadoop_version_field(self):
        return self._get_element(*self._hadoop_version_field_locator)

    @property
    def cluster_name_field(self):
        return self._get_element(*self._cluster_name_locator)

    @property
    def cluster_template_field(self):
        return self._get_element(*self._cluster_template_field_locator)

    @property
    def image_field(self):
        return self._get_element(*self._base_image_locator)

    @property
    def keypair_field(self):
	return self._get_element(*self._keypair_field_locator)

    @property
    def network_field(self):
	return self._get_element(*self._network_field_locator)

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

    @property
    def create_button(self):
	return self._get_element(*self._create_button_locator)

    def _click_on_create_button(self):
	self._wait_till_element_visible(self.create_button, timeout=5)
	self.create_button.click()

    def go_to_clusters_page(self):
        self.driver.get(self.cluster_url)

    def click_on_new_button(self):
	self._wait_till_element_visible(self.new_button, timeout=5)
	self.new_button.click()

    def create_cluster(self, random_cluster_template_name, random_cluster_name):
        self._select_dropdown(self.plugin_name, self.plugin_field)
        self._select_dropdown(self.hadoop_version, self.hadoop_version_field)
        self._click_on_create_button()
	self._fill_field_element(random_cluster_name, self.cluster_name_field)
        self._select_dropdown(random_cluster_template_name, self.cluster_template_field)
        self._select_dropdown(self.image_name, self.image_field)
	self._select_dropdown(self.keypair, self.keypair_field)
	self._select_dropdown(self.network, self.network_field)
	self._click_on_create_button()


    def launch_success_or_failure(self):
        self._wait_till_text_present_in_element(self.status, 'Active')
	time.sleep(3)

    def click_item_to_be_deleted(self):
        self.select_delete_item_field.click()

    def click_on_delete_button(self):
        self.delete_button.click()

    def click_on_confirm_delete_button(self):
        self.confirm_delete_button.click()

    def _select_item_to_be_deleted(self, random_cluster_name):
        selector = "form > table > tbody > tr[data-display=" + random_cluster_name + "] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()

    def delete_cluster(self, random_cluster_name):
        self.launch_success_or_failure()
        self._wait_till_element_is_clickable(self.select_delete_item_field)
        self._select_item_to_be_deleted(random_cluster_name)
        self.click_on_delete_button()
        self.click_on_confirm_delete_button()

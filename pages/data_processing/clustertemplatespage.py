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

from selenium.webdriver.common import by
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from pages import pageobject

class ClusterTemplatePage(pageobject.PageObject):
    _new_button_locator = (by.By.ID, 'cluster_templates__action_create')
    _plugin_field_locator = (by.By.ID,'id_plugin_name')
    _hadoop_version_field_locator = (by.By.ID,'id_vanilla_version')
    _cluster_template_name_field_locator = (by.By.ID,'id_cluster_template_name')
    _slave_count_locator = (by.By.ID, 'count_2')
    _template_field_locator = (by.By.ID, 'template_id')
    _create_button_locator = (by.By.CSS_SELECTOR,
                         "input[value='Create'][type='submit']")
    _node_groups_button_locator = (by.By.CSS_SELECTOR,
     "a[data-target='#configure_cluster_template__configurenodegroupsaction']")
    _add_group_button_locator = (by.By.ID, "add_group_button")
    anti_affinity_list = []
    _delete_button_locator = (by.By.ID, 
	"cluster_templates__action_delete_cluster_template")
    _confirm_delete_locator = (by.By.CSS_SELECTOR, "a[href='#'].btn.btn-primary")
    _select_delete_item_locator = (by.By.XPATH,
    "/html/body/div[1]/div[2]/div[3]/div[3]/div/form/table/tbody/tr/td[1]/input")


    def __init__(self, driver, conf):
        super(ClusterTemplatePage, self).__init__(driver, conf)
        self.clustertemplate_url = self.conf.cluster.cluster_template_url
	self.plugin_name = self.conf.cluster.plugin_name
	self.hadoop_version = self.conf.cluster.hadoop_version
	self.slave_count = self.conf.cluster.slave_count
	self.anti_affinity_list = self.conf.cluster.anti_affinity_group.split(',')
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
    def cluster_template_name(self):
        return self._get_element(*self._cluster_template_name_field_locator)

    @property
    def node_groups_button(self):
	return self._get_element(*self._node_groups_button_locator)

    @property
    def add_group_button(self):
        return self._get_element(*self._add_group_button_locator)

    @property
    def template_field(self):
	return self._get_element(*self._template_field_locator)

    @property
    def slave_count_field(self):
	return self._get_element(*self._slave_count_locator)

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

    def _click_on_create_button(self):
	self._wait_till_element_visible(self.create_button, timeout=5)
	self.create_button.click()

    def _click_on_node_groups_button(self):
        self._wait_till_element_visible(self.node_groups_button, timeout=5)
        self.node_groups_button.click()

    def _click_on_add_group_button(self):
        self._wait_till_element_visible(self.add_group_button, timeout=5)
        self.add_group_button.click()

    def go_to_cluster_templates_page(self):
        self.driver.get(self.clustertemplate_url)

    def click_on_new_button(self):
	self._wait_till_element_visible(self.new_button, timeout=5)
	self.new_button.click()

    def _select_anti_affinity_groups(self, anti_affinity_group):
        for i in anti_affinity_group:
            selector = "input[value='" + i + "'][type='checkbox']"
            element = self._get_element(by.By.CSS_SELECTOR, selector)
            element.click()

    def select_node_group_templates(self, random_master1_name, random_master2_name, random_slave_name):
	self._click_on_node_groups_button()
	self._select_dropdown(random_master1_name, self.template_field)
	self._click_on_add_group_button()
	self._select_dropdown(random_master2_name, self.template_field)
	self._click_on_add_group_button()
	self._select_dropdown(random_slave_name, self.template_field)
	self._click_on_add_group_button()
	self._fill_field_element(self.slave_count, self.slave_count_field)
	self._click_on_create_button()

    def create_cluster_template_details(self, random_clustertemplate_name):
        self._select_dropdown(self.plugin_name, self.plugin_field)
        self._select_dropdown(self.hadoop_version, self.hadoop_version_field)
        self._click_on_create_button()
	self._fill_field_element(random_clustertemplate_name, self.cluster_template_name)
        self._select_anti_affinity_groups(self.anti_affinity_list)

    def click_item_to_be_deleted(self):
        self.select_delete_item_field.click()

    def click_on_delete_button(self):
        self.delete_button.click()

    def click_on_confirm_delete_button(self):
        self.confirm_delete_button.click()

    def _select_item_to_be_deleted(self, random_template_name):
        selector = "form > table > tbody > tr[data-display=" + random_template_name + "] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()

    def delete_cluster_template(self, random_template_name):
        self._wait_till_element_is_clickable(self.select_delete_item_field)
	self._select_item_to_be_deleted(random_template_name)
        self.click_on_delete_button()
        self.click_on_confirm_delete_button()

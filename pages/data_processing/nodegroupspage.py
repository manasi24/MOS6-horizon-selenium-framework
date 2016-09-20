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

class NodeGroupPage(pageobject.PageObject):
    _new_button_locator = (by.By.ID, 'nodegroup_templates__action_create')
    _plugin_field_locator = (by.By.ID,'id_plugin_name')
    _hadoop_version_field_locator = (by.By.ID,'id_vanilla_version')
    _nodegroup_name_field_locator = (by.By.ID, 'id_nodegroup_name')
    _flavor_type_locator = (by.By.ID, 'id_flavor')
    _availability_zone_locator = (by.By.ID, 'id_availability_zone')
    _storage_locator = (by.By.ID, 'id_storage')
    _volumes_per_node_locator = (by.By.ID, 'id_volumes_per_node')
    _volumes_size_field_locator = (by.By.ID, 'id_volumes_size')
    _floating_ip_pool_locator = (by.By.ID, 'id_floating_ip_pool')
    _security_group_locator = (by.By.XPATH, '//*[@id="id_groups"]')
    _process_list_locator = (by.By.XPATH, '//*[@id="id_processes"]')
    _create_button_locator = (by.By.CSS_SELECTOR,
                         "input[value='Create'][type='submit']")
    _delete_button_locator = (by.By.ID, 
	"nodegroup_templates__action_delete_nodegroup_template")
    _confirm_delete_locator = (by.By.CSS_SELECTOR, "a[href='#'].btn.btn-primary")
    _select_delete_item_locator = (by.By.XPATH,
    "//body/div[1]/div[2]/div[3]/div[3]/div/form/table/tbody/tr[1]/td[1]/input")

    filesystem = ["HDFS", "JobFlow", "YARN"]
    hdfs = ["namenode", "datanode", "secondarynamenode"]
    jobflow = ["oozie"]
    yarn = ["resourcemanager", "nodemanager", "historyserver"]

    slave_node_process_list = []
    master1_node_process_list = []
    master2_node_process_list = []

    def __init__(self, driver, conf):
        super(NodeGroupPage, self).__init__(driver, conf)
        self.nodegroup_url = self.conf.cluster.node_group_url
	self.plugin_name = self.conf.cluster.plugin_name
	self.hadoop_version = self.conf.cluster.hadoop_version
	self.flavor_type = self.conf.cluster.flavor
	self.availability_zone = self.conf.cluster.availability_zone
	self.storage = self.conf.cluster.storage
	self.volumes_per_node = self.conf.cluster.volumes_per_node
	self.volumes_size = self.conf.cluster.volumes_size
	self.floating_ip_pool = self.conf.cluster.floating_ip_pool
	self.slave_node_process_list = self.conf.cluster.slave_node_processes.split(',')
	self.master1_node_process_list = self.conf.cluster.master1_node_processes.split(',')
	self.master2_node_process_list = self.conf.cluster.master2_node_processes.split(',')
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
    def node_group_name(self):
        return self._get_element(*self._nodegroup_name_field_locator)

    @property
    def flavor_field(self):
	return self._get_element(*self._flavor_type_locator)

    @property
    def availability_zone_field(self):
	return self._get_element(*self._availability_zone_locator)

    @property
    def storage_field(self):
	return self._get_element(*self._storage_locator)

    @property
    def volumes_per_node_field(self):
        return self._get_element(*self._volumes_per_node_locator)

    @property
    def volumes_size_field(self):
        return self._get_element(*self._volumes_size_field_locator)

    @property
    def floating_ip_pool_field(self):
        return self._get_element(*self._floating_ip_pool_locator)

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

    def go_to_node_groups_page(self):
        self.driver.get(self.nodegroup_url)

    def click_on_new_button(self):
	self._wait_till_element_visible(self.new_button, timeout=5)
	self.new_button.click()

    def _select_node_processes(self, process_list):
        for i in process_list:
            if i in self.hdfs:
                process = "HDFS:" + i
            elif i in self.yarn:
                process = "YARN:" + i
            else:
                process = "JobFlow:" + i
            selector = "input[value='" + process + "'][type='checkbox']"
            element = self._get_element(by.By.CSS_SELECTOR, selector)
            element.click()

    def node_group_template_for_slave(self, random_ngt_slave_name):
	self._select_dropdown(self.plugin_name, self.plugin_field)
	self._select_dropdown(self.hadoop_version, self.hadoop_version_field)
	self._click_on_create_button()
	self._fill_field_element(random_ngt_slave_name, self.node_group_name)
	self._select_dropdown(self.flavor_type, self.flavor_field)
	self._select_dropdown(self.availability_zone, self.availability_zone_field)
	self._select_dropdown(self.storage, self.storage_field)
	self._fill_field_element(self.volumes_per_node, self.volumes_per_node_field)
	self._fill_field_element(self.volumes_size, self.volumes_size_field)
	self._select_dropdown(self.floating_ip_pool, self.floating_ip_pool_field)
	self._select_node_processes(self.slave_node_process_list)
	self._click_on_create_button()

    def node_group_template_for_master1(self, random_ngt_master1_name):
	self._select_dropdown(self.plugin_name, self.plugin_field)
	self._select_dropdown(self.hadoop_version, self.hadoop_version_field)
	self._click_on_create_button()
	self._fill_field_element(random_ngt_master1_name, self.node_group_name)
	self._select_dropdown(self.flavor_type, self.flavor_field)
	self._select_dropdown(self.availability_zone, self.availability_zone_field)
	self._select_dropdown(self.storage, self.storage_field)
	self._fill_field_element(self.volumes_per_node, self.volumes_per_node_field)
	self._fill_field_element(self.volumes_size, self.volumes_size_field)
	self._select_dropdown(self.floating_ip_pool, self.floating_ip_pool_field)
	self._select_node_processes(self.master1_node_process_list)
	self._click_on_create_button()

    def node_group_template_for_master2(self, random_ngt_master2_name):
	self._select_dropdown(self.plugin_name, self.plugin_field)
	self._select_dropdown(self.hadoop_version, self.hadoop_version_field)
	self._click_on_create_button()
	self._fill_field_element(random_ngt_master2_name, self.node_group_name)
	self._select_dropdown(self.flavor_type, self.flavor_field)
	self._select_dropdown(self.availability_zone, self.availability_zone_field)
	self._select_dropdown(self.storage, self.storage_field)
	self._fill_field_element(self.volumes_per_node, self.volumes_per_node_field)
	self._fill_field_element(self.volumes_size, self.volumes_size_field)
	self._select_dropdown(self.floating_ip_pool, self.floating_ip_pool_field)
	self._select_node_processes(self.master2_node_process_list)
	self._click_on_create_button()

    def click_item_to_be_deleted(self):
        self.select_delete_item_field.click()

    def click_on_delete_button(self):
        self.delete_button.click()

    def click_on_confirm_delete_button(self):
        self.confirm_delete_button.click()

    def _select_item_to_be_deleted(self, ngt_master1_name, ngt_master2_name, ngt_slave_name):
        selector = "form > table > tbody > tr[data-display=" + ngt_master1_name + "] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()
        selector = "form > table > tbody > tr[data-display=" + ngt_master2_name + "] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()
        selector = "form > table > tbody > tr[data-display=" + ngt_slave_name + "] > td.multi_select_column > input"
        element = self._get_element(by.By.CSS_SELECTOR, selector)
        element.click()

    def delete_nodegroup_template(self, master1_name, master2_name, slave_name):
        self._wait_till_element_is_clickable(self.select_delete_item_field)
        self._select_item_to_be_deleted(master1_name, master2_name, slave_name)
        self.click_on_delete_button()
        self.click_on_confirm_delete_button()

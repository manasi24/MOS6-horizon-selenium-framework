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
from pages.data_processing import nodegroupspage
from pages.data_processing import clustertemplatespage
from pages.data_processing import clusterspage

class TestClusters(helpers.TestCase):
    """This is a basic sahara test:
    * checks that user is able to create a cluster
    * after successful cluster creation
    * checks that the user is able to delete the cluster without error
    """

    NODEGROUP_SLAVE_NAME = helpers.gen_random_resource_name("slave-")
    NODEGROUP_MASTER1_NAME = helpers.gen_random_resource_name("master1-")
    NODEGROUP_MASTER2_NAME = helpers.gen_random_resource_name("master2-")
    CLUSTER_TEMPLATE_NAME = helpers.gen_random_resource_name("template-")
    CLUSTER_NAME = helpers.gen_random_resource_name("cluster-")

    def test_create_node_group_templates(self):
        nodegroup_pg = nodegroupspage.NodeGroupPage(self.driver, self.CONFIG)
        nodegroup_pg.go_to_node_groups_page()
	nodegroup_pg.click_on_new_button()
        nodegroup_pg.node_group_template_for_slave(self.NODEGROUP_SLAVE_NAME)
	time.sleep(5)
        nodegroup_pg.click_on_new_button()
        nodegroup_pg.node_group_template_for_master1(self.NODEGROUP_MASTER1_NAME)
	time.sleep(5)
        nodegroup_pg.click_on_new_button()
        nodegroup_pg.node_group_template_for_master2(self.NODEGROUP_MASTER2_NAME)
	time.sleep(5)
        
	# test_create_cluster_templates
	clustertemplate_pg = clustertemplatespage.ClusterTemplatePage(self.driver, self.CONFIG)
	clustertemplate_pg.go_to_cluster_templates_page()
	clustertemplate_pg.click_on_new_button()
	clustertemplate_pg.create_cluster_template_details(self.CLUSTER_TEMPLATE_NAME)
	clustertemplate_pg.select_node_group_templates(self.NODEGROUP_MASTER1_NAME, 
		self.NODEGROUP_MASTER2_NAME, self.NODEGROUP_SLAVE_NAME)
	time.sleep(5)

	# test_create_clusters
	cluster_pg = clusterspage.ClusterPage(self.driver, self.CONFIG)
	cluster_pg.go_to_clusters_page()
	cluster_pg.click_on_new_button()
	cluster_pg.create_cluster(self.CLUSTER_TEMPLATE_NAME, self.CLUSTER_NAME)
	time.sleep(5)
	#cluster_pg.launch_success_or_failure()

	#delete_cluster
	cluster_pg.delete_cluster(self.CLUSTER_NAME)

	#delete_cluster_template
	clustertemplate_pg.go_to_cluster_templates_page()
	clustertemplate_pg.delete_cluster_template(self.CLUSTER_TEMPLATE_NAME)

	#delete_nodegroup_template
	nodegroup_pg.go_to_node_groups_page()
	nodegroup_pg.delete_nodegroup_template(self.NODEGROUP_MASTER1_NAME,
                self.NODEGROUP_MASTER2_NAME, self.NODEGROUP_SLAVE_NAME)

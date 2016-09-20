# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from oslo_config import cfg


DashboardGroup = [
    cfg.StrOpt('dashboard_url',
               default='http://localhost/',
               help="Where the dashboard can be found"),
    cfg.StrOpt('login_url',
               default='http://localhost/auth/login/',
               help="Login page for the dashboard"),
    cfg.StrOpt('help_url',
               default='http://docs.openstack.org/',
               help="Dashboard help page url"),
    cfg.StrOpt('project',
               default='CLOUD QA',
               help="project for the dashboard"),

]

IdentityGroup = [
    cfg.StrOpt('username',
               default='demo',
               help="Username to use for non-admin API requests."),
    cfg.StrOpt('password',
               default='secretadmin',
               help="API key to use when authenticating.",
               secret=True),
    cfg.StrOpt('admin_username',
               default='admin',
               help="Administrative Username to use for admin API "
               "requests."),
    cfg.StrOpt('admin_password',
               default='secretadmin',
               help="API key to use when authenticating as admin.",
               secret=True),
]

ImageGroup = [
    cfg.StrOpt('http_image',
               default='http://download.cirros-cloud.net/0.3.1/'
                       'cirros-0.3.1-x86_64-uec.tar.gz',
               help='http accessible image'),
]

AvailableServiceGroup = [
    cfg.BoolOpt('sahara',
                default=True,
                help='Whether is Sahara expected to be available')
]

SeleniumGroup = [
    cfg.IntOpt('implicit_wait',
               default=10,
               help="Implicit wait timeout in seconds"),
    cfg.IntOpt('explicit_wait',
               default=300,
               help="Explicit wait timeout in seconds"),
    cfg.IntOpt('page_timeout',
               default=30,
               help="Page load timeout in seconds"),
]

ScenarioGroup = [
    cfg.StrOpt('ssh_user',
               default='cirros',
               help='ssh username for image file'),
]

InstanceGroup = [
    cfg.StrOpt('url',
	       default="https://xx.yyy.zzz.ww/horizon/project/instances/",
	       help="URL for creating Instances"),
    cfg.StrOpt('flavor_type',
	       default="m1.small",
	       help="Default flavor type for creating instances"),
    cfg.StrOpt('availability_zone',
               default="Mumbai_AZ1",
               help="Default availability zone for creating instances"),
    cfg.StrOpt('keypair',
               default="cloud-qa",
               help="Default keypair for creating instances"),
    cfg.StrOpt('security_group',
               default="Allow-All",
               help="Default security group for creating instances"),
]

NetworkGroup = [
    cfg.StrOpt('url',
               default="https://xx.yyy.zzz.ww/horizon/project/networks/",
               help="URL for creating Networks"),
    cfg.StrOpt('network_address',
               default="10.0.0.0/24",
               help="Default address for creating network"),
    cfg.StrOpt('gateway_ip',
               default="10.0.0.1",
               help="Default ip address for gateway"),
    cfg.StrOpt('ip_version',
               default="IPv4",
               help="Default ip version for network"),
]

VolumeGroup = [
    cfg.StrOpt('url',
	       default="https://xx.yyy.zzz.ww/horizon/project/volumes/",
	       help="URL for creating Volumes"),
    cfg.StrOpt('image_name',
	       default="Ubuntu14.04 (1.3 GB)",
	       help="Default image source for creating volumes"),
    cfg.StrOpt('availability_zone',
               default="Mumbai_AZ1",
               help="Default availability zone for creating volumes"),


ClusterGroup = [
    cfg.StrOpt('node_group_url',
               default="https://xx.yyy.zzz.ww/horizon/project/data_processing/nodegroup_templates/",
               help="URL for creating Node Group Templates"),
    cfg.StrOpt('cluster_template_url',
               default="https://xx.yyy.zzz.ww/horizon/project/data_processing/cluster_templates/",
               help="URL for creating Cluster Templates"),
    cfg.StrOpt('cluster_url',
               default="https://xx.yyy.zzz.ww/horizon/project/data_processing/clusters/",
               help="URL for creating Clusters"),
    cfg.StrOpt('plugin_name',
               default="Vanilla Apache Hadoop",
               help="Default plugin for creating clusters"),
    cfg.StrOpt('hadoop_version',
               default="2.4.1",
               help="Default hadoop version for creating clusters"),
    cfg.StrOpt('flavor',
               default="m1.medium",
               help="Default flavor type for creating clusters"),
    cfg.StrOpt('availability_zone',
               default="Mumbai_AZ1",
               help="Default availability zone for creating clusters"),
    cfg.StrOpt('floating_ip_pool',
               default = "RJILFloatingIPs",
               help="Default Floating IPs for creating clusters"),
    cfg.StrOpt('storage',
               default = "Cinder Volume",
               help="Default storage for creating clusters"),
    cfg.StrOpt('volumes_per_node',
               default = "1",
               help="Default volume per node for creating clusters"),
    cfg.StrOpt('volumes_size',
               default = "10",
               help="Default volume size node for creating clusters"),
    cfg.StrOpt('master1_node_processes',
               default = "10",
               help="Default volume size for creating clusters"),
    cfg.StrOpt('master2_node_processes',
               default = "10",
               help="Default volume size for creating clusters"),
    cfg.StrOpt('slave_node_processes',
               default = "10",
               help="Default volume size for creating clusters"),
    cfg.StrOpt('anti_affinity_group',
               default="10",
               help="Default anti-affinity for creating Cluster Templates"),
    cfg.StrOpt('slave_count',
               default="3",
               help="Default slave count for creating Cluster Templates"),
    cfg.StrOpt('base_image',
               default="Ubuntu-14.04-Sahara-Apache-Hadoop-2.4.1",
               help="Default image for creating Cluster"),
    cfg.StrOpt('network',
               default="network_name",
               help="Default network for creating Cluster"),

]


def _get_config_files():
    conf_dir = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        'overcast/conf')
    conf_file = os.environ.get('HORIZON_INTEGRATION_TESTS_CONFIG_FILE',
                               "%s/overcast.conf" % conf_dir)
    return [conf_file]


def get_config():
    cfg.CONF([], project='horizon', default_config_files=_get_config_files())

    cfg.CONF.register_opts(DashboardGroup, group="dashboard")
    cfg.CONF.register_opts(IdentityGroup, group="identity")
    cfg.CONF.register_opts(AvailableServiceGroup, group="service_available")
    cfg.CONF.register_opts(SeleniumGroup, group="selenium")
    cfg.CONF.register_opts(ImageGroup, group="image")
    cfg.CONF.register_opts(ScenarioGroup, group="scenario")
    cfg.CONF.register_opts(InstanceGroup, group="instance")
    cfg.CONF.register_opts(NetworkGroup, group="network")
    cfg.CONF.register_opts(VolumeGroup, group="volume")
    cfg.CONF.register_opts(ClusterGroup, group="cluster")
    return cfg.CONF

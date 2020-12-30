#!/usr/bin/env python
from resource_management import *
from resource_management.libraries.script.script import Script
import os, socket

script_dir = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(os.path.dirname(script_dir), 'files')

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_name = default("/hostLevelParams/stack_name", None)

master_env = config['configurations']['kudu-master-env']
tserver_env = config['configurations']['kudu-tserver-env']

current_host_name = socket.gethostname()
hdfs_host = default("/clusterHostInfo/namenode_hosts", [''])[0]

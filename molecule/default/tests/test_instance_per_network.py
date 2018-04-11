import os
import testinfra.utils.ansible_runner
import pytest
import json
import re

"""ASC-157: Perform Post Deploy System validations"""

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('infra1')


@pytest.mark.jira('asc-157')
def test_instance_per_network_per_hypervisor(host):
    """
    Per network, create instance, ping, tear-down.

    """

    os_pre = ("lxc-attach -n $(lxc-ls -1 | grep utility | head -n 1) "
              "-- bash -c '. /root/openrc ; openstack ")

    # create test security group
    cmd = "{} security group create rpc_support -f json'".format(os_pre)
    res = host.run(cmd)
    assert res.rc == 0
    security_group = json.loads(res.stdout)['id']

    # add ping rule to security group
    cmd = "{} security group rule create --proto icmp {} -f json'".format(os_pre,
    security_group)
    res = host.run(cmd)
    assert res.rc == 0

    vxlan = json.loads(res.stdout)['id']
    # create test vlan
    cmd = "{} network create TEST_VXLAN -f json'".format(os_pre)
    res = host.run(cmd)
    assert res.rc == 0
    vxlan = json.loads(res.stdout)['id']
    os_cmd = ' '.join(["subnet create",
                       "--allocation-pool",
                       "start=192.168.1.2,end=192.168.1.254",
                       "--host-route",
                       "destination=0.0.0.0/0,gateway=192.168.1.1",
                       "--subnet-range 192.168.1.0/24",
                       "--network",
                       vxlan,
                       "TEST-VXLAN-SUBNET"])
    res = host.run("{} {}'".format(os_pre, os_cmd))
    assert res.rc == 0

    # create flavor
    cmd = ' '.join(["flavor create",
                    "--ram 512",
                    "--disk 10",
                    "--vcpus 1",
                    "random_name"])
    host.run("{} {}'".format(os_pre, cmd))

    # get Ubuntu image
    img_cmd = "{} image list -f json '".format(os_pre)
    img_res = host.run(img_cmd)
    img_dicts = json.loads(img_res.stdout)
    img = (item for item in img_dicts if re.match(r'Ubuntu',
                                                  item["Name"])).next()

    # get network list
    net_cmd = "{} network list -f json '".format(os_pre)
    net_res = host.run(net_cmd)
    networks = json.loads(net_res.stdout)
    for network in networks:
        cmd = "{} network show \"{}\" -f json '".format(os_pre, network['ID'])
        res = host.run(cmd)
        net_dict = json.loads(res.stdout)
        if net_dict['router:external'] == 'External':
            continue
        # get compute list
        compute_cmd = ' '.join(["compute service list",
                                "--service nova-compute",
                                "-f json"])
        compute_res = host.run("{} {}'".format(os_pre, compute_cmd))
        computes = json.loads(compute_res.stdout)
        for compute in computes:
            server = '-'.join(["rpctest", compute['Host'], network['ID']])
            create_cmd = ' '.join(["server create",
                                   "--image", img['ID'],
                                   "--flavor random_name",
                                   "--security-group",
                                   security_group,
                                   "--nic net-id=" + network['ID'],
                                   "--availability-zone", compute['Zone'],
                                   server,
                                   "-f json"])
            cmd = "{} {}'".format(os_pre, create_cmd)
            create_res = host.run(cmd)
            assert create_res.rc == 0

            # ping server
            # How?
            # openstack router create router1
            # openstack router add subnet router1 VXLAN-subnet-v4
            # neutron router-gateway-set router1 provider1
            # ip netns
            # openstack floating ip create TEST_VXLAN
            # openstack server add floating ip servername <IP-returned-from-floating-create>
            # ping -c 1 <IP-returned-from-floating-create>

            # delete server
            cmd = "{} server delete {}'".format(os_pre, server)
            delete_res = host.run(cmd)
            assert delete_res.rc == 0

    # tear down test vlan
    host.run("{} network delete {}'".format(os_pre, vxlan))

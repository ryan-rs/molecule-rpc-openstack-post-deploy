import os
import testinfra.utils.ansible_runner
import pytest
import random
import json
import time

"""ASC-241: FIXME"""

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('os-infra_hosts')[:1]

os_pre = ("lxc-attach -n $(lxc-ls -1 | grep utility | head -n 1) "
          "-- bash -c '. /root/openrc ; openstack ")


@pytest.mark.test_id('c3002bde-59f1-11e8-be3b-6c96cfdb252f')
@pytest.mark.jira('jira-ticket')
def test_hypervisor_vms(host):
    """ASC-241: FIXME"""

    server_list = []
    # get image id
    cmd = "{} image list -f json'".format(os_pre)
    res = host.run(cmd)
    images = json.loads(res.stdout)
    filtered_images = list(filter(lambda d: 'buntu' in d['Name'], images))
    assert len(filtered_images) > 0
    image = filtered_images[-1]

    cmd = "lxc-ls -1 | egrep 'neutron(_|-)agents' | tail -1"
    res = host.run(cmd)
    container = res.stdout.strip()
    lxc_pre = "lxc-attach -n {} ".format(container)

    r = random.randint(1111, 9999)
    flavor = "rpctest-{}-flavor".format(r)
    flavor_cmd = "{} flavor create --ram 512 --disk 10 --vcpus 1 {}'".format(os_pre, flavor)
    host.run_expect([0], flavor_cmd)

    net_cmd = "{} network list -f json '".format(os_pre)
    net_res = host.run(net_cmd)
    # networks = net_res.stdout.split('\n')
    networks = json.loads(net_res.stdout)
    for network in networks:
        cmd = "{} network show {} -f json'".format(os_pre, network['ID'])
        res = host.run(cmd)
        network_detail = json.loads(res.stdout)
        if network_detail['router:external'] == 'External':
            continue
        # spin up instance per hypervisor
        cmd = "{} compute service list -f json'".format(os_pre)
        res = host.run(cmd)
        computes = json.loads(res.stdout)
        for compute in computes:
            if compute['Binary'] == 'nova-compute':
                instance_name = "rpctest-{}-{}-{}".format(r, compute['Host'],
                                                          network_detail['name'])
                cmd = "{} server create \
                       -f json \
                       --image {} \
                       --flavor {} \
                       --nic net-id={} \
                       --availability-zone {} \
                       {}'".format(os_pre, image['ID'], flavor,
                                   network['ID'], compute['Zone'], instance_name)
                res = host.run(cmd)
                server = json.loads(res.stdout)
                server_list.append(server)

    time.sleep(60)
    for server in server_list:
        cmd = "{} server show {} -f json'".format(os_pre, server['id'])
        res = host.run(cmd)
        s = json.loads(res.stdout)
        assert s['status'] == 'ACTIVE'

        # test ssh
        network_name, ip = s['addresses'].split('=')
        # get network detail (again)
        # Either fresh call to 'openstack network show' or bundle it above.
        # This will include network id and subnets.
        cmd = "{} network show {} -f json'".format(os_pre, network_name)
        res = host.run(cmd)
        network = json.loads(res.stdout)

        # confirm SSH port access
        cmd = "{} -- bash -c 'ip netns exec qdhcp-{} nc -w1 {} 22'".format(lxc_pre, network['id'], ip)
        res = host.run(cmd)
        assert 'SSH' in res.stdout

        # get gateway ip via subnet detail
        cmd = "{} subnet show {} -f json'".format(os_pre, network['subnets'])
        res = host.run(cmd)
        sub = json.loads(res.stdout)
        if sub['gateway_ip']:
            # ping out
            cmd = "{} -- bash -c 'ip netns exec qdhcp-{} \
                   ssh -o StrictHostKeyChecking=no rpc_support ubuntu@{} \
                   ping -c1 -w2 8.8.8.8'".format(lxc_pre, network['id'], ip)
            host.run_expect([0], cmd)

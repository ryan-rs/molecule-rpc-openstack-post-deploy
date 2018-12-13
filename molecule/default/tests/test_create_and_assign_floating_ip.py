import pytest_rpc.helpers as helpers
import os
import pytest
import testinfra.utils.ansible_runner
import utils as tmp_var

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('shared-infra_hosts')[:1]

utility_container = ("lxc-attach -n $(lxc-ls -1 | grep utility | head -n 1) "
                     "-- bash -c '. /root/openrc ; ")


@pytest.mark.test_id('ab24ffbd-798b-11e8-a2b2-6c96cfdb2e43')
@pytest.mark.jira('asc-254')
def test_assign_floating_ip_to_instance(os_props, host):
    """ Assign floating IP to an instance/server

    Args:
        os_props (dict): This fixture returns a dictionary of OpenStack facts
            and variables from Ansible which can be used to manipulate
            OpenStack objects.
        host(testinfra.host.Host): Testinfra host fixture.
    """

    # Creating an instance from image
    random_str = helpers.generate_random_string(6)
    data = {
        'instance_name': "test_instance_{}".format(random_str),
        'from_source': 'image',
        'source_name': os_props['test_resources']['image_name'],
        'flavor': os_props['test_resources']['flavor'],
        'network_name': os_props['private_network'],
    }

    instance_id = helpers.create_instance(data, host)

    assert tmp_var.get_expected_value('server',
                                      instance_id,
                                      'status',
                                      'ACTIVE',
                                      host,
                                      retries=40)
    assert tmp_var.get_expected_value('server',
                                      instance_id,
                                      'OS-EXT-STS:power_state',
                                      'Running',
                                      host,
                                      retries=20)
    assert tmp_var.get_expected_value('server',
                                      instance_id,
                                      'OS-EXT-STS:vm_state',
                                      'active', host,
                                      retries=20)

    # Creating a floating IP:
    floating_ip = helpers.create_floating_ip(
        os_props['gateway_network'],
        host
    )

    # Assigning floating ip to a server
    cmd = ("{} openstack server add "
           "floating ip {} {}'".format(utility_container,
                                       instance_id,
                                       floating_ip)
           )
    host.run_expect([0], cmd)

    # After being assigned, the floating IP status should be 'ACTIVE'
    assert (tmp_var.get_expected_value('floating ip',
                                       floating_ip,
                                       'status',
                                       'ACTIVE',
                                       host)
            )

    # Ensure the IP can be pinged from infra1
    cmd = "ping -c1 {}".format(floating_ip)
    assert (host.run_expect([0], cmd))

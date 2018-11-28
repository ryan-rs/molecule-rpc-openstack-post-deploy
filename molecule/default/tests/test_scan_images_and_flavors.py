# -*- coding: utf-8 -*-

"""ASC-240: Verify the requested glance images were uploaded

RPC 10+ manual test 10
"""

# ==============================================================================
# Imports
# ==============================================================================
import os
import pytest
import pytest_rpc.helpers as helpers
# noinspection PyPackageRequirements
import testinfra.utils.ansible_runner


# ==============================================================================
# Globals
# ==============================================================================
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('localhost')[:1]


# ==============================================================================
# Tests
# ==============================================================================
@pytest.mark.test_id('d7fc612b-432a-11e8-9a7a-6a00035510c0')
@pytest.mark.jira('asc-240')
def test_verify_glance_image(host):
    """Verify the glance images created by 'openstack-service-config.yml'."""

    # Expect
    exp_images = ['Ubuntu 14.04 LTS',
                  'Ubuntu 16.04',
                  'Fedora 27',
                  'CentOS 7',
                  'OpenSuse Leap 42.3',
                  'Debian 9 Latest',
                  'Debian TESTING',
                  'Cirros-0.3.5']

    # Test
    actual_images = [img['Name'] for img
                     in helpers.os_cli_json(host, 'image list')]

    assert actual_images == exp_images


@pytest.mark.test_id('d7fc62c7-432a-11e8-8102-6a00035510c0')
@pytest.mark.jira('asc-240')
def test_verify_vm_flavors(os_api_connection):
    """Verify the VM flavor created by 'openstack-service-config.yml'."""

    flavors = ['m1.micro',
               'm1.tiny',
               'm1.mini',
               'm1.small',
               'm1.medium',
               'm1.large',
               'm1.xlarge',
               'm1.heavy']

    for flavor in flavors:
        assert os_api_connection.get_flavor_name(flavor) == flavor

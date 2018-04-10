import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('non-existing-hosts')


class TestForRPC10PlusPostDeploymentQCProcessSwift(object):
    """This class define all test cases that need implemented for ticket:
     https://rpc-openstack.atlassian.net/browse/ASC-295
     """

    @pytest.mark.test_id('a717077c-4da2-44be-8f36-34e205ca2e82')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_swift_ring_has_data(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('c5558e17-d538-41d0-9f99-c71d744d5b7b')
    @pytest.mark.skip(reason='Need implementation')
    def test_object_ring_rebalanced(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('b354a4f9-0c9b-4727-bf41-37b2af5f375b')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_md5_and_mounted_drives(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('7f379758-faca-4bc3-820f-8d5eac6197a3')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_swift_stat(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('c2c9da61-3a63-4e4f-8789-c9ae7adf39ac')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_dispension_populate(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('6a4675b8-b8f4-4a43-8ece-a8b097166fc7')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_dispension_report(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

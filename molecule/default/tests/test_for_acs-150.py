import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('non-existing-hosts')


class TestForRPC10PlusPostDeploymentQCProcess(object):
    """This class define all test cases that need implemented for ticket:
     https://rpc-openstack.atlassian.net/browse/ASC-150
     """

    @pytest.mark.test_id('b67672ca-f3c5-4c0c-8016-75eba486234a')
    @pytest.mark.skip(reason='Need implementation')
    def test_reboot_physical_devices(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('ca14b131-9dc0-4151-a5a3-6da67eebfbca')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_galera_cluster(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('cac8933f-0d86-49a3-ad49-05a9494aeb79')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_rpc_version(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('d901e75f-5762-4a1e-a3b6-4da7c124e72f')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_ceph_deploy(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('c92b8f18-a168-4cbd-901f-b37cc95b43d0')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_configed_quotas(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('9b9aa60d-54a2-453d-889e-d1f098662906')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_configed_networks(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('9336f24f-4f16-4d72-94f2-c144fe92c872')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_updated_glance_image(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('f8d81763-ad9d-4c85-855d-178fe5cfa97a')
    @pytest.mark.skip(reason='Need implementation')
    def test_build_instances_on_compute_node(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('91b4fb8e-6251-4761-b4b1-873bf8c65019')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_floating_ip_nats(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('ea6a153d-a330-4e0d-b8de-56207285b9b9')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_correct_number_rabbitmq_per_connection(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('b5b7860c-f423-41c7-afa6-1ea4824f9ffa')
    @pytest.mark.skip(reason='Need implementation')
    def test_create_cinder_volume(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('2a01a1a3-1e37-4ac8-ac31-77670a63506e')
    @pytest.mark.skip(reason='Need implementation')
    def test_write_to_attached_volume_partition(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('5791a8e9-6ce8-47b5-a730-ec85247b1507')
    @pytest.mark.skip(reason='Need implementation')
    def test_create_volume_on_image_on_glance(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('fab13709-542a-4fbe-a067-f6db1d089edf')
    @pytest.mark.skip(reason='Need implementation')
    def test_create_snapshot_of_an_instance(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('4b3d21b5-e146-4d28-b368-990b0caac111')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_mbu_installation(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('9c485e7a-9e1c-4e55-9e9d-fc8ede31eec0')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_ssl_config_f5(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('9eed5eb3-b95f-4ce9-8245-17a08885dada')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_ansible_playbook(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('4b673f23-ba82-487d-a0d4-2e81eaa183ad')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_console_horizon(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

    @pytest.mark.test_id('63ffa675-58b6-4122-873f-1254f20d7446')
    @pytest.mark.skip(reason='Need implementation')
    def test_verify_kibana_horizon_access_with_no_ssh(self, host):
        """See RPC 10+ Post-Deployment QC process document"""

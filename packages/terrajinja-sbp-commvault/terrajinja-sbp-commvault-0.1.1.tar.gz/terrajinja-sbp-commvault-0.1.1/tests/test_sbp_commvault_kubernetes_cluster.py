import pytest
from cdktf import Testing, Token
from src.terrajinja.sbp.commvault.kubernetes_cluster import SbpCommvaultKubernetesCluster
from .helper import stack, has_resource, has_resource_path_value

class TestSbpCommvaultKubernetesCluster:

    def test_resource(self, stack):
        # Create an instance of the extended SbpCommvaultDataCommvaultPlan class
        cluster = SbpCommvaultKubernetesCluster(
            scope=stack,
            ns="test",
            name="cluster_name",
            id="5314"
        )

        synthesized = Testing.synth(stack)

        # Test synth output
        has_resource(synthesized, "commvault_kubernetes_cluster")
                        
        has_resource_path_value(synthesized, "commvault_kubernetes_cluster", "test", "name", "cluster_name")
        has_resource_path_value(synthesized, "commvault_kubernetes_cluster", "test", "id", "5314")
        
        # Test id if string is changed to number
        cluster.id == 5314

if __name__ == "__main__":
    pytest.main()

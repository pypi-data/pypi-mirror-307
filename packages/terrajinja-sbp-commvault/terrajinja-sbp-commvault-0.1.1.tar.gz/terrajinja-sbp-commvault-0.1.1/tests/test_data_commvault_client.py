import pytest
from cdktf import Testing, Token
from src.terrajinja.sbp.commvault.data_commvault_client import SbpCommvaultDataCommvaultClient
from .helper import stack, has_data_source, has_data_source_path_value

class TestSbpCommvaultDataCommvaultClient:

    def test_resource(self, stack):
        # Create an instance of the extended SbpCommvaultDataCommvaultClient class
        client = SbpCommvaultDataCommvaultClient(
            scope=stack,
            ns="test",
            name="client_name",
            id="1"
        )

        synthesized = Testing.synth(stack)

        # Test synth output
        has_data_source(synthesized, "commvault_client")
                        
        has_data_source_path_value(synthesized, "commvault_client", "test", "name", "client_name")
        has_data_source_path_value(synthesized, "commvault_client", "test", "id", "1")
        
        # Test id if string is changed to number
        client.id == 1

if __name__ == "__main__":
    pytest.main()

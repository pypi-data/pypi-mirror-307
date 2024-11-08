import pytest
from cdktf import Testing, Token
from src.terrajinja.sbp.commvault.data_commvault_plan import SbpCommvaultDataCommvaultPlan
from .helper import stack, has_data_source, has_data_source_path_value

class TestSbpCommvaultDataCommvaultPlan:

    def test_resource(self, stack):
        # Create an instance of the extended SbpCommvaultDataCommvaultPlan class
        plan = SbpCommvaultDataCommvaultPlan(
            scope=stack,
            ns="test",
            name="plan_name",
            id="1"
        )

        synthesized = Testing.synth(stack)

        # Test synth output
        has_data_source(synthesized, "commvault_plan")
                        
        has_data_source_path_value(synthesized, "commvault_plan", "test", "name", "plan_name")
        has_data_source_path_value(synthesized, "commvault_plan", "test", "id", "1")
        
        # Test id if string is changed to number
        plan.id == 1

if __name__ == "__main__":
    pytest.main()

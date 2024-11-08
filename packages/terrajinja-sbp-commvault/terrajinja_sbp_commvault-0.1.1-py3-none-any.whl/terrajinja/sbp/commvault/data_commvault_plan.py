from constructs import Construct
from terrajinja.imports.commvault.data_commvault_plan import DataCommvaultPlan
from cdktf import Token


class SbpCommvaultDataCommvaultPlan(DataCommvaultPlan):
    def __init__(self, scope: Construct, ns: str, **kwargs):

        super().__init__(
            scope=scope,
            id_=ns,
            **kwargs,
        )

    @property
    def id(self) -> str:
        return Token().as_number(super().id)

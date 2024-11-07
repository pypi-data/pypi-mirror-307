from constructs import Construct
from terrajinja.imports.commvault.data_commvault_client import DataCommvaultClient  # noqa: E501
from cdktf import Token


class SbpCommvaultDataCommvaultClient(DataCommvaultClient):
    def __init__(self, scope: Construct, ns: str, **kwargs):

        super().__init__(
            scope=scope,
            id_=ns,
            **kwargs,
        )

    @property
    def id(self) -> str:
        return Token().as_number(super().id)

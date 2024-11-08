from constructs import Construct
from terrajinja.imports.commvault.kubernetes_cluster import KubernetesCluster  # noqa: E501
from cdktf import Token


class SbpCommvaultKubernetesCluster(KubernetesCluster):
    def __init__(self, scope: Construct, ns: str, **kwargs):

        super().__init__(
            scope=scope,
            id_=ns,
            **kwargs,
        )

    @property
    def id(self) -> str:
        return Token().as_number(super().id)

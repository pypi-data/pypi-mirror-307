from typing import List, Optional

from databricks.agents.client.rest_client import (
    get_chain_deployments as rest_get_chain_deployments,
)
from databricks.agents.sdk_utils.entities import Deployment
from databricks.agents.sdk_utils.permissions_checker import (
    _check_view_permissions_on_deployment,
)
from databricks.sdk.errors.platform import (
    ResourceDoesNotExist,
)


def _get_deployments(
    model_name: str, model_version: Optional[int] = None
) -> List[Deployment]:
    deployments = rest_get_chain_deployments(model_name, model_version)
    return_deployments = []
    if len(deployments) > 0:
        for deployment in deployments:
            try:
                _check_view_permissions_on_deployment(deployment)
                return_deployments.append(deployment)
            except ResourceDoesNotExist:
                # If the corresponding endpoint does not exist because it was manually deleted, we should ignore it
                pass
    return return_deployments

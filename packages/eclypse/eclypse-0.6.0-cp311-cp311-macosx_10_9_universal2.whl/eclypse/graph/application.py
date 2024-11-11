"""Module for the Application class.

It extends the AssetGraph class to represent an application, with nodes representing
services and edges representing the interactions between them.
"""

from __future__ import annotations

from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
)

import networkx as nx

from eclypse.core.graph import AssetGraph
from eclypse.core.remote.service import ServiceEngine

if TYPE_CHECKING:
    from networkx.classes.reportviews import (
        EdgeView,
        NodeView,
    )

    from .assets import Asset
    from .node_group import NodeGroup


class Application(AssetGraph):
    """Class to represent a multi-service Application."""

    def __init__(
        self,
        application_id: str,
        node_update_policy: Optional[Callable[[NodeView], None]] = None,
        edge_update_policy: Optional[Callable[[EdgeView], None]] = None,
        node_assets: Optional[Dict[str, Asset]] = None,
        edge_assets: Optional[Dict[str, Asset]] = None,
        include_default_assets: bool = True,
        requirement_init: Literal["min", "max"] = "min",
        flows: Optional[List[List[str]]] = None,
        seed: Optional[int] = None,
    ):
        """Create a new Application.

        Args:
            application_id (str): The ID of the application.
            node_update_policy (Optional[Callable[[NodeView], None]]): A function to \
                update the nodes.
            edge_update_policy (Optional[Callable[[EdgeView], None]]): A function to \
                update the edges.
            node_assets (Optional[Dict[str, Asset]]): The assets of the nodes.
            edge_assets (Optional[Dict[str, Asset]]): The assets of the edges.
            include_default_assets (bool): Whether to include the default assets.
            requirement_init (Literal["min", "max"]): The initialization of the requirements.
            flows (Optional[List[List[str]]): The flows of the application.
            seed (Optional[int]): The seed for the random number generator.
        """

        if requirement_init == "min":
            _attr_init = "max"
        elif requirement_init == "max":
            _attr_init = "min"
        else:
            raise ValueError(f"Invalid value for attr_init: {requirement_init}")

        super().__init__(
            graph_id=application_id,
            node_update_policy=node_update_policy,
            edge_update_policy=edge_update_policy,
            node_assets=node_assets,
            edge_assets=edge_assets,
            include_default_assets=include_default_assets,
            attr_init=_attr_init,  # type: ignore[arg-type]
            flip_assets=True,
            seed=seed,
        )

        self.services: Dict[str, ServiceEngine] = {}
        self.flows = flows if flows is not None else []

    def add_service(self, service: ServiceEngine, **assets):
        """Add a service to the application.

        Args:
            service (Service): The service to add.
            **assets : The assets to add to the service.
        """
        if not isinstance(service, ServiceEngine):
            raise ValueError("The service must be an instance of Service.")
        service.application_id = self.id
        self.services[service.id] = service
        self.add_node(service.id, **assets)

    def add_service_by_group(self, group: NodeGroup, service: ServiceEngine, **assets):
        """Add a service with a specific group to the application.

        Args:
            group (NodeGroup): The group to add the service to.
            service (Service): The service to add.
            **assets: The assets to add to the service.
        """
        service.application_id = self.id
        self.services[service.id] = service
        self.add_node_by_group(group, service.id, **assets)

    def set_flows(self):
        """Set the flows of the application, using the following rules:

        - If the flows are already set, do nothing.
        - If the flows are not set, use the gateway as the source and all the other nodes as the target.
        - If there is no gateway, set the flows to an empty list.
        """
        if self.flows == []:
            gateway_name = next((s for s in self.nodes if "gateway" in s.lower()), None)
            if gateway_name is not None:
                self.flows = list(
                    nx.all_simple_paths(
                        self,
                        source=gateway_name,
                        target=[x for x in self.nodes if x != gateway_name],
                    )
                )

    @cached_property
    def has_logic(self) -> bool:
        """Check if the application has a logic for each service.

        This property requires to be True for the remote execution.
        """
        checks = [(x in self.services) for x in self.nodes]
        return checks != [] and all(checks)

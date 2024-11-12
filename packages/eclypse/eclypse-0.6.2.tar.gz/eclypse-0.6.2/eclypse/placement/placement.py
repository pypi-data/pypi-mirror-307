"""Module for the Placement class, which represents the mapping of application services
onto infrastructure nodes, according to a placement strategy."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

if TYPE_CHECKING:
    from eclypse.core.placement.view import PlacementView
    from eclypse.graph.application import Application
    from eclypse.graph.infrastructure import Infrastructure

    from .strategies import PlacementStrategy


class Placement:
    """A placement is a mapping of each service of an application to a node of an
    infrastructure, computed according to a placement strategy."""

    def __init__(
        self,
        infrastructure: Infrastructure,
        application: Application,
        strategy: Optional[PlacementStrategy] = None,
    ):
        """Initializes the Placement.

        Args:
            infrastructure (Infrastructure): The infrastructure to place the application onto.
            application (Application): The application to place onto the infrastructure.
            strategy (PlacementStrategy): The strategy to use for the placement.
        """
        self.strategy: Optional[PlacementStrategy] = strategy

        self.infrastructure: Infrastructure = infrastructure
        self.application: Application = application

        self._deployed: bool = False
        self.mapping: Dict[str, str] = {}

        self._to_reset = False

    def generate_mapping(
        self, placements: Dict[str, Placement], placement_view: PlacementView
    ):
        """Generate the mapping of the application services onto the infrastructure
        nodes, according to the placement strategy."""
        if self.strategy is None:
            raise ValueError("No placement strategy provided")
        self.mapping = self.strategy.place(
            self.infrastructure.available, self.application, placements, placement_view
        )

    def reset_mapping(self):
        """Reset the mapping of the placement."""
        self.mapping = {}
        self._to_reset = False

    def service_placement(self, service_id: str) -> str:
        """Return the node where a service is placed.

        Args:
            service_id (str): The name of the service.

        Returns:
            str: The name of the node where the service is placed.
        """
        return self.mapping[service_id]

    def services_on_node(self, node_name: str) -> List[str]:
        """Return all the services placed on a node.

        Args:
            node_name (str): The name of the node.

        Returns:
            List[str]: The names of the services placed on the node.
        """
        return [
            service_id for service_id, node in self.mapping.items() if node == node_name
        ]

    def interactions_on_link(self, source: str, target: str) -> List[Tuple[str, str]]:
        """Return all the services interactions crossing a link.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.

        Returns:
            List[Tuple[str, str]]: The names of the services interactions crossing the link.
        """
        return [
            (s, n)
            for s in self.services_on_node(source)
            for n in self.application.neighbors(s)
            if self.service_placement(n) == target
        ]

    def node_service_mapping(self) -> Dict[str, List[str]]:
        """Return a view of the placement as a mapping of nodes to the list of services
        placed on them."""
        return {node: self.services_on_node(node) for node in self.infrastructure.nodes}

    def link_interaction_mapping(self) -> Dict[Tuple[str, str], List[Tuple[str, str]]]:
        """Return a view of the placement as a mapping of links to the list of services
        interactions crossing them.

        Returns:
            Dict[Tuple[str, str], List[Tuple[str, str]]]: The mapping of links to the list \
                of services interactions crossing them.
        """
        return {
            (source, target): self.interactions_on_link(source, target)
            for source, target in self.infrastructure.edges
        }

    def node_requirements_mapping(self) -> Dict[str, Dict[str, Any]]:
        """Return a view of the placement as a mapping of nodes to the total
        requirements of the services placed on them.

        Returns:
            Dict[str, ServiceRequirements]: The mapping of nodes to the total requirements \
                of the services placed on them.
        """
        return {
            node: self.application.node_assets.aggregate(
                *(self.application.nodes[s] for s in services)
            )
            for node, services in self.node_service_mapping().items()
        }

    def link_requirements_mapping(self) -> Dict[Tuple[str, str], Dict[str, Any]]:
        """Return a view of the placement as a mapping of links to the total
        requirements of the services interactions crossing them.

        Returns:
            Dict[Tuple[str, str], S2SRequirements]: The mapping of links to the total \
                requirements of the services interactions crossing them.
        """
        return {
            (source, target): self.application.edge_assets.aggregate(
                *(self.application.edges[s][t] for s, t in services)
            )
            for (source, target), services in self.link_interaction_mapping().items()
        }

    def __str__(self) -> str:
        """Return a string representation of the placement, in the form: <service_id>
        -> <node_name>

        Returns:
            str: The string representation of the placement.
        """
        result = (
            "{"
            + "".join(
                [
                    f"{service_id} -> {node_name} | "
                    for service_id, node_name in self.mapping.items()
                ]
            )[:-3]
            + "}"
        )
        return result

    def __repr__(self) -> str:
        """Return a string representation of the placement, in the form: <service_id>
        -> <node_name>

        Returns:
            str: The string representation of the placement.
        """
        return self.__str__()

    @property
    def is_partial(self) -> List[str]:
        """Return whether the placement is partial or not.

        Returns:
            List[str]: The list of services that are not placed.
        """
        return list(
            service
            for service in self.application.nodes
            if service not in self.mapping or self.mapping[service] is None
        )

    @property
    def deployed(self) -> bool:
        """Return whether the placement is deployed or not.

        Returns:
            bool: True if the placement is deployed, False otherwise.
        """
        return self._deployed

    @deployed.setter
    def deployed(self, value: bool):
        """Set whether the placement is deployed or not.

        Args:
            value (bool): True if the placement is deployed, False otherwise.
        """
        self._deployed = value

    @property
    def to_reset(self) -> bool:
        """Return whether the placement needs to be reset or not.

        Returns:
            bool: True if the placement needs to be reset, False otherwise.
        """
        return self._to_reset

    @to_reset.setter
    def to_reset(self, value: bool):
        """Set whether the placement needs to be reset or not.

        Args:
            value (bool): True if the placement needs to be reset, False otherwise.
        """
        self._to_reset = value

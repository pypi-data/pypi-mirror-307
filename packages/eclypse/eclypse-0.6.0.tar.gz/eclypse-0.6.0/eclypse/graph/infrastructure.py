"""Module for the Infrastructure class, which extends the AssetGraph class to represent
a network, with nodes representing devices and edges representing (physical/virtual)
links between them.

The infrastructure also stores:
- A global placement strategy (optional).
- A set of path assets aggregators, one per edge asset.
- A path algorithm to compute the paths between nodes.
- A view of the available nodes and edges.
- A cache of the computed paths and their costs.
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
)

import networkx as nx
from networkx.classes.coreviews import (
    FilterAdjacency,
    FilterAtlas,
)
from networkx.classes.filters import no_filter

from eclypse.core.graph import AssetGraph

from .assets.defaults import get_default_path_aggregators

if TYPE_CHECKING:
    from networkx.classes.reportviews import (
        EdgeView,
        NodeView,
    )

    from eclypse.graph.assets.asset import Asset
    from eclypse.placement.strategies import PlacementStrategy


class Infrastructure(AssetGraph):
    """Class to represent a Cloud-Edge infrastructure."""

    def __init__(
        self,
        infrastructure_id: str = "Infrastructure",
        placement_strategy: Optional[PlacementStrategy] = None,
        node_update_policy: Optional[Callable[[NodeView], None]] = None,
        edge_update_policy: Optional[Callable[[EdgeView], None]] = None,
        node_assets: Optional[Dict[str, Asset]] = None,
        edge_assets: Optional[Dict[str, Asset]] = None,
        include_default_assets: bool = True,
        path_assets_aggregators: Optional[Dict[str, Callable[[List[Any]], Any]]] = None,
        path_algorithm: Optional[Callable[[nx.Graph, str, str], List[str]]] = None,
        resource_init: Literal["min", "max"] = "min",
        seed: Optional[int] = None,
    ):
        """Create a new Infrastructure.

        Args:
            infrastructure_id (str): The ID of the infrastructure.
            placement_strategy (Optional[PlacementStrategy]): The placement \
                strategy to use.
            node_update_policy (Optional[Callable[[NodeView], None]]): A function to \
                update the nodes.
            edge_update_policy (Optional[Callable[[EdgeView], None]]): A function to \
                update the edges.
            node_assets (Optional[Dict[str, Asset]]): The assets of the nodes.
            edge_assets (Optional[Dict[str, Asset]]): The assets of the edges.
            include_default_assets (bool): Whether to include the default assets.
            path_assets_aggregators (Optional[Dict[str, Callable[[List[Any]], Any]]]): \
                The aggregators to use for the path assets.
            path_algorithm (Optional[Callable[[nx.Graph, str, str], List[str]]]): \
                The algorithm to use to compute the paths.
            resource_init (Literal["min", "max"]): The initialization method for the resources.
            seed (Optional[int]): The seed for the random number generator.
        """
        self.strategy = placement_strategy

        super().__init__(
            graph_id=infrastructure_id,
            node_update_policy=node_update_policy,
            edge_update_policy=edge_update_policy,
            node_assets=node_assets,
            edge_assets=edge_assets,
            include_default_assets=include_default_assets,
            attr_init=resource_init,
            seed=seed,
        )

        if path_assets_aggregators is not None and not all(
            k in self.edge_assets for k in path_assets_aggregators
        ):
            raise ValueError(
                "The path_assets_aggregators must be a subset of the edge_assets"
            )

        default_path_aggregator = get_default_path_aggregators()
        _path_assets_aggregators = {}

        for k in self.edge_assets:
            if k not in _path_assets_aggregators:
                _path_assets_aggregators[k] = default_path_aggregator[k]

        self.path_assets_aggregators = _path_assets_aggregators

        self._path_algorithm: Callable[[nx.Graph, str, str], List[str]] = (
            path_algorithm
            if path_algorithm is not None
            else lambda G, source, target: nx.dijkstra_path(
                G, source, target, weight="latency"
            )
        )

        self._available: Optional[nx.DiGraph] = None

        self._paths: Dict[str, Dict[str, List[str]]] = {}
        self._costs: Dict[str, Dict[str, Tuple[List[Tuple[str, str, Any]], float]]] = {}

    def contains(self, other: nx.DiGraph) -> List[str]:
        """Compares the requirements of the nodes and edges in the PlacementView with
        the resources of the nodes and edges in the Infrastructure.

        Args:
            other (Infrastructure): The Infrastructure to compare with.

        Returns:
            List[str]: A list of nodes whose requirements are not respected or \
                whose connected links are not respected.
        """
        not_respected = set()
        for n, req in other.nodes(data=True):
            res = self.nodes[n]
            if not self.node_assets.satisfies(res, req):
                self.logger.log("ECLYPSE", f"Node {n} not respected")
                self.logger.log("ECLYPSE", f"Required: {req}")
                self.logger.log("ECLYPSE", f"Available: {res}")
                not_respected.add(n)

        for u, v, req in other.edges(data=True):
            res = self.path_resources(u, v)
            if not self.edge_assets.satisfies(res, req):
                self.logger.log("ECLYPSE", f"Link {u} -> {v} not respected")
                self.logger.log("ECLYPSE", f"Required: {req}")
                self.logger.log("ECLYPSE", f"Available: {res}")
                not_respected.add(u)
                not_respected.add(v)

        return list(not_respected)

    def path(
        self, source: str, target: str
    ) -> Optional[Tuple[List[Tuple[str, str, Dict[str, Any]]], float]]:
        """Retrieve the path between two nodes, if it exists. If the path does not
        exist, it is computed and cached, with costs for each hop. Both the path and the
        costs are recomputed if any of the hop costs has changed by more than 5%.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.

        Returns:
            Optional[List[Tuple[str, str, float]]]: The path between the two nodes in the \
                form (source, target, cost), or None if the path does not exist.
        """
        try:
            if source not in self._paths or target not in self._paths[source]:
                self._compute_path(source, target)
            if not all(n in self.available for n in self._paths[source][target]):
                self._compute_path(source, target)
            else:
                costs = [
                    c["latency"]
                    for _, _, c in self._path_costs(self._paths[source][target])[0]
                ]
                cached_costs = [
                    cc["latency"] for _, _, cc in self._costs[source][target][0]
                ]

                # check if any hop cost changed by more than 5%
                if any(
                    (abs(c - cc) / cc >= 0.05 if cc != 0 else 0)
                    for c, cc in zip(costs, cached_costs)
                ):
                    self._compute_path(source, target)

            return self._costs[source][target]
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def path_resources(self, source: str, target: str) -> Dict[str, Any]:
        """Retrieve the resources of the path between two nodes, if it exists. If the
        path does not exist, it is computed and cached.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.

        Returns:
            PathResources: The resources of the path between the two nodes, or None if \
                the path does not exist.
        """
        if source == target:
            return self.edge_assets.upper_bound

        path = self.path(source, target)

        if path is None:
            return self.edge_assets.lower_bound

        return {
            k: (aggr([c[k] for _, _, c in path[0]]))
            for k, aggr in self.path_assets_aggregators.items()
        }

    def _compute_path(self, source: str, target: str):
        """Compute the path between two nodes using Dijkstra's algorithm, and cache it.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.
        """
        self._paths.setdefault(source, {})[target] = self._path_algorithm(
            self.available, source, target
        )
        self._costs.setdefault(source, {})[target] = self._path_costs(
            self._paths[source][target]
        )

    def _path_costs(
        self, path: List[str]
    ) -> Tuple[List[Tuple[str, str, Dict[str, Any]]], float]:
        """Compute the costs of a path in the form (source, target, cost).

        Args:
            path (List[str]): The path as a list of node IDs.

        Returns:
            List[Tuple[str, str, float]]: The costs of the path in the form (source, target, cost).
        """
        costs = []
        total_processing_time = 0
        for s, t in nx.utils.pairwise(path):
            costs.append((s, t, self.edges[s, t]))
            total_processing_time += self.nodes[s]["processing_time"]

        total_processing_time += self.nodes[path[-1]]["processing_time"]
        return [
            (s, t, self.edges[s, t]) for s, t in nx.utils.pairwise(path)
        ], total_processing_time

    @property
    def available(self) -> Infrastructure:
        """Return the subgraph with only the available nodes.

        Returns:
            nx.DiGraph: A subgraph with only the available nodes.
        """
        if self._available is None:
            self._available = nx.freeze(
                self.__class__(
                    placement_strategy=self.strategy,
                    node_update_policy=self.node_update_policy,
                    edge_update_policy=self.edge_update_policy,
                    node_assets=self.node_assets,
                    edge_assets=self.edge_assets,
                    include_default_assets=False,
                    path_assets_aggregators=self.path_assets_aggregators,
                    path_algorithm=self._path_algorithm,
                )
            )
            filter_node = lambda n: self.nodes[n]["availability"] > 0
            filter_edge = no_filter
            self._available._NODE_OK = filter_node
            self._available._EDGE_OK = filter_edge

            # create view by assigning attributes from G
            self._available._graph = self
            self._available.graph = self.graph
            self._available._node = FilterAtlas(self._node, filter_node)

            def reverse_edge(u, v):
                return filter_edge(v, u)

            if self.is_directed():
                self._available._succ = FilterAdjacency(
                    self._succ, filter_node, filter_edge
                )
                self._available._pred = FilterAdjacency(
                    self._pred, filter_node, reverse_edge
                )

            else:
                self._available._adj = FilterAdjacency(
                    self._adj, filter_node, filter_edge
                )
        return self._available

    @property
    def has_strategy(self) -> bool:
        """Check if the infrastructure has a placement strategy.

        Returns:
            bool: True if the infrastructure has a placement strategy, False otherwise.
        """
        return self.strategy is not None

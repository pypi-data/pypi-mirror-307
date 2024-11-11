"""Package for the graph representation, used to model the infrastructure and the
applications in a simulation.

It also contains the node group class, which is used to assign a layer to application
services and infrastructure nodes.
"""

from .node_group import NodeGroup
from .application import Application
from .infrastructure import Infrastructure

from eclypse.core.graph import AssetGraph

__all__ = ["NodeGroup", "AssetGraph", "Application", "Infrastructure"]

"""Module for the Convex Asset class. It represents a numeric asset where the
aggregation is convex, i.e. the minimum value of the assets. It provides the interface
for the basic algebraic functions between assets:

- `aggregate`: Aggregate the assets into a single asset via the minimum value.
- `satisfies`: Check if the asset contains another asset.
- `is_consistent`: Check if the asset belongs to the interval [lower_bound, upper_bound].
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Tuple,
    Union,
)

from .asset import Asset

if TYPE_CHECKING:
    from eclypse.graph.node_group import NodeGroup

    from .space import AssetSpace


class Convex(Asset):
    """ConvexAsset represents a numeric asset where the aggregation is convex."""

    def __init__(
        self,
        lower_bound: float,
        upper_bound: float,
        init_spaces: Dict[
            Union[NodeGroup, Tuple[NodeGroup, NodeGroup]],
            Union[AssetSpace, Callable[[], Any]],
        ],
        functional: bool = True,
    ):
        """Create a new convex asset.

        Args:
            lower_bound (float): The lower bound of the asset.
            upper_bound (float): The upper bound of the asset.
            init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.

        Raises:
            ValueError: If $lower_bound < upper_bound$.
        """
        super().__init__(lower_bound, upper_bound, init_spaces, functional)

    def aggregate(self, *assets) -> float:
        """Aggregate the assets into a single asset by taking the minimum value. If no
        assets are provided, the upper bound is returned.

        Args:
            assets (Iterable[NumericAsset]): The assets to aggregate.

        Returns:
            NumericAsset: The aggregated asset.
        """
        return min(assets, default=self.upper_bound)

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check if asset1 contains asset2. In the ordering of a convex asset, the
        higher value contains the other.

        Args:
            asset1 (NumericAsset): The "container" asset.
            asset2 (NumericAsset): The "contained" asset.

        Returns:
            bool: True if asset1 >= asset2, False otherwise.
        """
        return asset >= constraint

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

        Args:
            asset (NumericAsset): The asset to check.

        Returns:
            bool: True if the asset is within the interval, False otherwise.
        """
        return self.lower_bound <= asset <= self.upper_bound

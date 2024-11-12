"""Module for the Concave Asset class. It represents a numeric asset where the
aggregation is concave, i.e. the maximum value of the assets. It provides the interface
for the basic algebraic functions between assets:

- `aggregate`: Aggregate the assets into a single asset via the maximum value.
- `satisfies`: Check if the asset is contained in another asset.
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
    from eclypse.graph import NodeGroup

    from .space import AssetSpace


class Concave(Asset):
    """ConcaveAsset represents a numeric asset where the aggregation is concave."""

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
        """Create a new concave asset.

        Args:
            lower_bound (TAdditive): The lower bound of the asset.
            upper_bound (TAdditive): The upper bound of the asset.
            init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.

        Raises:
            ValueError: If $lower_bound > upper_bound$.
        """
        super().__init__(lower_bound, upper_bound, init_spaces, functional)

    def aggregate(self, *assets) -> float:
        """Aggregate the assets into a single asset by taking the maximum value. If no
        assets are provided, the lower bound is returned.

        Args:
            assets (Iterable[TConcave]): The assets to aggregate.

        Returns:
            TConcave: The aggregated asset.
        """
        return max(assets, default=self.upper_bound)

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check if asset1 contains asset2. In the ordering of a concave asset, the
        lower value contains the other.

        Args:
            asset1 (TConcave): The "container" asset.
            asset2 (TConcave): The "contained" asset.

        Returns:
            bool: True if asset1 <= asset2, False otherwise.
        """
        return asset <= constraint

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound]."""
        return self.lower_bound >= asset >= self.upper_bound

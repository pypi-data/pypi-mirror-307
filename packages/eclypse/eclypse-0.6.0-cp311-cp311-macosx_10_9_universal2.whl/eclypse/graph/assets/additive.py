"""Module for the AdditiveAsset class. It represents a numeric asset where the
aggregation is the sum of the assets. It provides the interface for the basic algebraic
functions between assets:

- `aggregate`: Aggregate the assets into a single asset via summation.
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
    from eclypse.graph import NodeGroup

    from .space import AssetSpace


class Additive(Asset):
    """AdditiveAsset represents a numeric asset where the aggregation is additive."""

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
        """Create a new additive asset.

        Args:
            lower_bound (float): The lower bound of the asset.
            upper_bound (float): The upper bound of the asset.
            init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.

        Raises:
            ValueError: If $lower_bound > upper_bound$.
        """
        super().__init__(lower_bound, upper_bound, init_spaces, functional=functional)

    def aggregate(self, *assets: float) -> float:
        """Aggregate the assets into a single asset via summation.

        Args:
            assets (Iterable[float]): The assets to aggregate.

        Returns:
            float: The aggregated asset.
        """
        return sum(assets, start=self.lower_bound)

    def satisfies(self, asset: float, constraint: float) -> bool:
        """Check asset1 contains asset2. In an additive asset, the higher value contains
        the lower value.

        Args:
            asset1 (float): The "container" asset.
            asset2 (float): The "contained" asset.

        Returns:
            True if asset1 >= asset2, False otherwise.
        """
        return asset >= constraint

    def is_consistent(self, asset: float) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

        Args:
            asset (float): The asset to be checked.

        Returns:
            True if lower_bound <= asset <= upper_bound, False otherwise.
        """
        return self.lower_bound <= asset <= self.upper_bound

"""Module for the AssetBucket class.

It is a dictionary-like class that stores assets of nodes and service and provides
methods to aggregate, check consistency, and initialize them.
"""

from __future__ import annotations

import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Tuple,
    Union,
)

from eclypse.graph.assets import Additive

from .asset import Asset
from .concave import Concave
from .convex import Convex
from .multiplicative import Multiplicative

if TYPE_CHECKING:
    from random import Random

    from eclypse.graph.node_group import NodeGroup


class AssetBucket(Dict[str, Asset]):
    """Class to store a set of nodes/services assets."""

    def __init__(self, **assets):
        """Create a new asset bucket.

        Args:
            **assets (Dict[str, Asset]): The assets to store in the bucket.
        """
        super().__init__(assets)

    def __setitem__(self, key: str, value: Asset) -> None:
        """Set an asset in the bucket.

        Args:
            key (str): The key of the asset.
            value (Asset): The asset to store.
        """
        if not isinstance(value, Asset):
            raise ValueError(f"Asset {key} is not an instance of Asset.")
        super().__setitem__(key, value)

    def aggregate(self, *assets: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate the assets into a single asset.

        Args:
            assets (Iterable[Dict[str, Any]]): The assets to aggregate.

        Returns:
            Dict[str, Any]: The aggregated asset.
        """
        return {
            key: self[key].aggregate(*[asset[key] for asset in assets if key in asset])
            for key in self
        }

    def satisfies(self, asset: Dict[str, Any], constraint: Dict[str, Any]) -> bool:
        """Check if the assets of the other asset are contained in the assets of this
        asset.

        Args:
            asset1 (Dict[str, Any]): The "container" asset.
            asset2 (Dict[str, Any]): The "contained" asset.

        Returns:
            bool: True if the assets of asset2 are contained in asset1, False otherwise.
        """
        return all(
            self[key].satisfies(asset[key], constraint[key])
            for key in self
            if self[key].functional and key in constraint
        )

    def consume(self, asset: Dict[str, Any], amount: Dict[str, Any]) -> Dict[str, Any]:
        """Consume the `amount` of the asset from the `asset`.

        Args:
            asset (Dict[str, Any]): The asset to consume from.
            amount (Dict[str, Any]): The amount to consume.

        Returns:
            Dict[str, Any]: The remaining asset after the consumption.
        """

        return {
            key: (
                asset[key] - amount[key]
                if isinstance(self[key], Additive) and key in amount
                else asset[key]
            )
            for key in self
        }

    def is_consistent(self, asset: Dict[str, Any]) -> bool:
        """Check if the asset belongs to the interval [lower_bound, upper_bound].

        Args:
            asset (Dict[str, Any]): The asset to be checked.

        Returns:
            bool: True if the asset is within the interval, False otherwise.
        """
        return all(self[key].is_consistent(asset[key]) for key in asset)

    def init(
        self, key: Union[NodeGroup, Tuple[NodeGroup, NodeGroup]], random: Random
    ) -> Dict[str, Any]:
        """Initialize the asset for a particular `NodeGroup` in the case of the node,
        and for an ordered pair of `NodeGroup` for the link. This is strictly dependent
        on the asset implemented.

        Args:
            key (Union[NodeGroup, Tuple[NodeGroup, NodeGroup]]): The group for which to initialize the asset.

        Returns:
            Dict[str, Any]: The initialized asset.
        """
        return {k: self[k].init(key, random) for k in self}

    def flip(self):
        """Flip the assets of the bucket, thus moving from node capabilities to service.

        requirements:
        - Convex assets become Concave assets, and vice versa.
        - Multiplicative assets become Concave assets.

        N.B. Cannot be used more than once, since the flip is not reversible.
        """
        req_bucket = AssetBucket()
        for k, v in self.items():
            if isinstance(v, Concave):
                req_bucket[k] = Convex(
                    v.upper_bound, v.lower_bound, v.init_spaces, v.functional
                )
            elif isinstance(v, (Convex, Multiplicative)):
                req_bucket[k] = Concave(
                    v.upper_bound, v.lower_bound, v.init_spaces, v.functional
                )
            else:
                req_bucket[k] = copy.deepcopy(v)
        return req_bucket

    @property
    def lower_bound(self) -> Dict[str, Any]:
        """Return the lower bound of the asset bucket, i.e. the lower bound of each
        asset in the bucket.

        Returns:
            Dict[str, Any]: The lower bound of the asset bucket.
        """
        return {k: v.lower_bound for k, v in self.items()}

    @property
    def upper_bound(self) -> Dict[str, Any]:
        """Return the upper bound of the asset bucket, i.e. the upper bound of each
        asset in the bucket.

        Returns:
            Dict[str, Any]: The upper bound of the asset bucket.
        """
        return {k: v.upper_bound for k, v in self.items()}

"""Module for the Asset class. It represents a node resource or a service requirement,
such as CPU, GPU, RAM or node availability.

It provides the inteface for the basic algebraic functions between assets:
- aggregate: aggregate the assets into a single asset.
- satisfies: check if the asset satisfies a constraint based on the total ordering of the asset.
- is_consistent: check if the asset has a feasible value, i.e., it is within the bounds.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Tuple,
    Union,
)

from eclypse.graph.node_group import NodeGroup

from .space import AssetSpace

if TYPE_CHECKING:
    from random import Random


class Asset:
    """Asset represents a resource of the infrastructure, such as CPU, GPU, RAM or
    Availability.

    It provides the inteface for the basic algebraic functions between assets.
    """

    def __init__(
        self,
        lower_bound: Any,
        upper_bound: Any,
        init_spaces: Dict[
            Union[NodeGroup, Tuple[NodeGroup, NodeGroup]],
            Union[AssetSpace, Callable[[], Any]],
        ],
        functional: bool = True,
    ):
        """Initialize the asset with the lower and upper bounds.

        The lower and the upper bounds represent the element which is always contained in
        and the element the always contains the asset, respectively. Thus, they must
        respect the total ordering of the asset.

        The init_fns are the functions to initialize the asset. It must contain all the
        values of `NodeGroup` as keys for a node asset, and all the ordered combinations
        of `NodeGroup` as keys for a link asset.

        Args:
            lower_bound (Any): The lower bound of the asset.
            upper_bound (Any): The upper bound of the asset.
            group_init_fns (Dict[NodeGroup, Callable]): The functions to initialize the asset.
        """

        if not self.satisfies(upper_bound, lower_bound):
            raise ValueError(
                "The lower bound must be contained in the upper bound. See the ",
                f"behaviour of the `contains` method of {self.__class__.__name__}.",
            )
        self.init_spaces = init_spaces
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.functional = functional

    def init(
        self, key: Union[NodeGroup, Tuple[NodeGroup, NodeGroup]], random: Random
    ) -> Any:
        """Initialize the asset for a particular `NodeGroup` in the case of the node,
        and for an ordered pair of `NodeGroup` for the link.

        This is strictly dependent on the asset implemented.
        """
        if not key in self.init_spaces:
            raise ValueError(
                f"No initialization function for {key} present in the asset."
            )
        value = self.init_spaces[key]
        if value is None:
            raise ValueError(
                f"You must provide a return value in the initialization function for {key}."
            )

        if isinstance(value, AssetSpace):
            return self.init_spaces[key](random)  # type: ignore[call-arg]
        if callable(value):
            return self.init_spaces[key]()  # type: ignore[call-arg]

        raise ValueError(
            f"Initialization function for {key} must be "
            + "an AssetInitializer or a Callable with no arguments!"
        )

    @abstractmethod
    def aggregate(self, *assets) -> Any:
        """Aggregate the assets into a single asset.

        Args:
            assets (Any): The assets to aggregate.
        """

    @abstractmethod
    def satisfies(self, asset: Any, constraint: Any) -> bool:
        """Check if the asset satisfies the constraint.

        Args:
            asset (Any): The asset to check.
            constraint (Any): The constraint to check.

        Returns:
            bool: True if the asset satisfies the constraint, False otherwise.
        """

    @abstractmethod
    def is_consistent(self, asset: Any) -> bool:
        """Check if the asset has a feasible value."""

    def __str__(self):
        return "".join(
            [
                f"Type: {self.__class__.__name__}\n",
                f"Lower Bound: {self.lower_bound}\n",
                f"Upper Bound: {self.upper_bound}\n",
                f"Functional: {self.functional}\n",
            ]
        )

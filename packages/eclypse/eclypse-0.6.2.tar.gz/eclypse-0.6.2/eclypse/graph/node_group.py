"""Module for the NodeGroup enumeration, which represents the group/layer of a node in
the infrastructure."""

from enum import (
    Enum,
    auto,
)
from functools import total_ordering
from typing import (
    Any,
    Callable,
)


@total_ordering
class NodeGroup(Enum):
    """NodeGroup represents the group/layer of a node in the infrastructure. It is an enum
    with the following possible values:

    Attributes:
        UNSET: The node group is not set.
        IOT: The node group is an IoT device.
        EDGE: The node group is an edge device.
        CLOUD: The node group is a cloud server.
    """

    UNSET = auto()
    IOT = auto()
    NEAR_EDGE = auto()
    FAR_EDGE = auto()
    CLOUD = auto()

    @classmethod
    def _missing_(cls, _: object) -> Any:
        """Return the UNSET value if the value is not in the enum."""
        return cls.UNSET

    def _bool_op(self, fn: Callable, other: "NodeGroup"):
        """Perform a boolean operation between two NodeGroup objects.

        Args:
            fn (Callable): The boolean function to be performed.
            other (NodeGroup): The other NodeGroup object to be compared with.

        Returns:
            bool: The result of the boolean operation.
        """
        return fn(self.value, other.value)

    def __lt__(self, other: "NodeGroup"):
        """Return True if the value of the NodeGroup is less than the value of the other
        NodeGroup.

        Args:
            other (NodeGroup): The NodeGroup object to be compared with.

        Returns:
            bool: True if the current NodeGroup is less than the other, else False.
        """
        return self._bool_op(lambda x, y: x < y, other)

    def __eq__(self, other: object):
        """Return True if the value of the NodeGroup is equal to the value of the.

        Args:
            other (NodeGroup): The NodeGroup object to be compared with.

        Returns:
            bool: True if the current NodeGroup is equal to the other, else False.
        """
        if not isinstance(other, NodeGroup):
            raise TypeError("Can only compare NodeGroup with NodeGroup")
        return self._bool_op(lambda x, y: x == y, other)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash(self.value)

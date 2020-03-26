from collections import Counter
import numpy as np
from typing import Dict, List

import gym.spaces as spaces

from playtest.components import Component


class Resource(Component):
    """Constants for various types of resource
    """

    YELLOW = "yellow"
    RED = "red"
    GREEN = "green"
    BLACK = "black"

    value: str
    max_amount = 0xFFFF
    # Note this is order from least to most valuable
    all_resources = [YELLOW, RED, GREEN, BLACK]
    all_resources_short = "YRGB"

    str_lookup = {"R": RED, "G": GREEN, "B": BLACK, "Y": YELLOW}

    @property
    def stack(self) -> Dict[str, int]:
        """Convert value of resource into a structure
        """
        return self.value_to_struct(self.value)

    @classmethod
    def upgrade_char(cls, s: str) -> str:
        assert len(s) == 1, "Can only upgrade one at a time"
        token_name = cls.str_lookup[s]
        try:
            token_next = cls.all_resources[cls.all_resources.index(
                token_name) + 1]
        except IndexError:
            return s
        return cls.reverse_lookup(token_next)

    @classmethod
    def value_to_struct(cls, s: str):
        c = {r: 0 for r in cls.all_resources}
        for r in s:
            try:
                c[cls.str_lookup[r]] += 1
            except KeyError:
                raise KeyError(f"Invalid resource: {r} from {cls.value}")
        return c

    @classmethod
    def reverse_lookup(cls, s):
        rev_lookup = dict({v: k for k, v in cls.str_lookup.items()})
        return rev_lookup[s]

    @classmethod
    def struct_to_value(cls, stack: Dict[str, int]) -> str:
        return "".join(
            sorted(
                ["".join([cls.reverse_lookup(r)] * count)
                 for r, count in stack.items()]
            )
        )

    @classmethod
    def get_all_resources(cls) -> List[str]:
        return sorted(cls.all_resources)

    def __eq__(self, x) -> bool:
        return self.value == x.value

    def __len__(self) -> int:
        """Return number of resources"""
        return len(self.value)

    def __init__(self, data: str = ""):
        assert isinstance(data, str), "Resource only takes string"
        self.value = "".join(sorted(data))
        assert self.stack, "Can parse into valid stack"

    def __repr__(self):
        return self.value

    def reset(self):
        self.value = ""

    def to_data(self):
        return self.value

    def get_observation_space(self):
        return spaces.Box(
            low=0,
            high=self.max_amount,
            shape=(len(self.all_resources),),
            dtype=np.uint8,
        )

    def to_numpy_data(self) -> np.ndarray:
        return np.array(
            [self.stack[r] for r in self.get_all_resources()], dtype=np.uint8
        )

    def has_required(self, required: "Resource") -> bool:
        my = self.stack
        theirs = required.stack
        assert (
            sorted(my.keys()) == self.get_all_resources()
        ), "Not all resources are there"
        return all([theirs.get(res, 0) <= my_count for res, my_count in my.items()])

    def sub_resource(self, required: "Resource"):
        my = self.stack
        theirs = required.stack
        assert sorted(my.keys()) == self.get_all_resources()
        self.value = self.struct_to_value(
            {res: my_count - theirs.get(res, 0)
             for res, my_count in my.items()}
        )

    def sub_with_remainder(self, required: "Resource") -> "Resource":
        my = self.stack
        theirs = required.stack
        assert sorted(my.keys()) == self.get_all_resources()
        result = {res: my_count - theirs.get(res, 0)
                  for res, my_count in my.items()}
        new_my_value = {}
        remainder = {}
        for k, v in result.items():
            if result[k] < 0:
                remainder[k] = -v
                new_my_value[k] = 0
            else:
                new_my_value[k] = v
        self.value = self.struct_to_value(new_my_value)
        return Resource(self.struct_to_value(remainder))

    def add_resource(self, required: "Resource"):
        my = self.stack
        theirs = required.stack
        assert sorted(my.keys()) == self.get_all_resources()
        self.value = self.struct_to_value(
            {res: my_count + theirs.get(res, 0)
             for res, my_count in my.items()}
        )

    def pop_lower(self, amount) -> "Resource":
        """Pop number of cheapest resources"""
        assert len(self) >= amount, f"Must have {amount} resources"
        data = self.stack
        popped_data: Dict[str, int] = {}
        for c in self.all_resources:
            if data[c] > 0 and sum(popped_data.values()) <= amount:
                to_discard = min(amount, data[c])
                data[c] -= to_discard
                popped_data[c] = to_discard
                amount -= to_discard
        self.value = self.struct_to_value(data)
        return self.__class__(self.struct_to_value(popped_data))


class Caravan(Resource):
    """A set of resources, with a 10 item limit."""

    def discard_to(self, down_to: int = 10):
        if len(self) >= down_to:
            self.pop_lower(len(self) - down_to)

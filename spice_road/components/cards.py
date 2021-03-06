import os
import re
import yaml
from copy import copy
from typing import Dict

import gym.spaces as spaces

from playtest.components import BaseCard, Deck as BaseDeck
from .resources import Resource


def read_yaml(file_name):
    return filter(lambda r: bool(r), yaml.load_all(open(file_name, "r")))


class TraderCard(BaseCard):
    re_value = re.compile(r"([RGBY]*)\s*->\s*([RGBY]*)")

    total_unique_cards: int = 52

    @classmethod
    def value_to_struct(cls, value) -> Dict:
        """Get structured data from string"""
        m = cls.re_value.match(value)
        assert m, f"Value should be in valid format: {value}"
        return {
            "src": Resource(m.group(1)),
            "dst": Resource(m.group(2)),
        }

    @classmethod
    def struct_to_value(cls, struct: Dict) -> str:
        return f"{struct['src']} -> {struct['dst']}"

    @property
    def src(self) -> Resource:
        return self.value_to_struct(self.value)["src"]

    @property
    def dst(self) -> Resource:
        return self.value_to_struct(self.value)["dst"]

    @classmethod
    def get_all_cards(cls):
        data = read_yaml(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "trader.yml")
        )
        return [cls(f"{d['src']} -> {d['dst']}", uid=i) for i, d in enumerate(data)]

    def can_trade(self, r: Resource) -> bool:
        return r.has_required(self.src)

    def trade(self, r: Resource) -> Resource:
        r2 = copy(r)
        r2.sub_resource(self.src)
        r2.add_resource(self.dst)
        return r2


class ConversionCard(TraderCard):
    re_value = re.compile(r"Convert\((\d+)\)")

    total_unique_cards: int = 52

    @classmethod
    def value_to_struct(cls, value) -> Dict:
        """Get structured data from string"""
        m = cls.re_value.match(value)
        assert m, f"Value should be in valid format: {value}"
        return {
            "c": int(m.group(1)),
        }

    @classmethod
    def struct_to_value(cls, struct: Dict) -> str:
        return f"Convert({struct['c']})"

    @property
    def c(self) -> int:
        """Number of resource you can convert"""
        return self.value_to_struct(self.value)["c"]

    @property
    def src(self) -> Resource:
        raise KeyError()

    @property
    def dst(self) -> Resource:
        raise KeyError()

    @classmethod
    def get_all_cards(cls):
        return [cls("Convert(2)") * 2]

    def can_trade(self, r: Resource) -> bool:
        return len(r) >= self.c

    def trade(self, r: Resource) -> Resource:
        assert len(r) == self.c, f"Must provide exact count of resource ({r})"
        r2 = Resource("")
        for val in r.value:
            # Upgrade the resource
            r2.add_resource(Resource(Resource.upgrade_char(val)))
        return r2

    def get_observation_space(self) -> spaces.Space:
        raise NotImplementedError(f"{self.__class__}")


class TraderDeck(BaseDeck[TraderCard]):
    generic_card = TraderCard


class ScoringCard(BaseCard):
    regex_parse = re.compile(r"([RGBY]+) \((\d+)\)")

    total_unique_cards: int = 52

    @classmethod
    def get_all_cards(cls):
        data = read_yaml(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "scoring.yml")
        )
        return [cls(f"{d['target']} ({d['vp']})", uid=i) for i, d in enumerate(data)]

    # ----------------
    # Get structured property
    # -----------------

    @classmethod
    def value_to_struct(cls, value):
        m = cls.regex_parse.match(value)
        assert m, f"Must be of right format {value}"
        return {
            "target": Resource(m.group(1)),
            "victory_point": int(m.group(2)),
        }

    @classmethod
    def struct_to_value(cls, struct):
        target: Resource = struct["target"]
        return f"{target.value} ({struct['victory_point']})"

    @property
    def target(self) -> Resource:
        return self.value_to_struct(self.value)["target"]

    @property
    def victory_point(self) -> int:
        return self.value_to_struct(self.value)["victory_point"]

    def __init__(self, value, uid=0, test_watermark=None):
        assert self.regex_parse.match(
            value
        ), f"Input string should be of right format {value}"
        super().__init__(value, uid=uid, test_watermark=test_watermark)

    def check_enough(self, r: Resource) -> bool:
        """Check if the resource is sufficient for the cards
        """
        return r.has_required(self.target)

    def get_observation_space(self) -> spaces.Space:
        raise NotImplementedError(f"{self.__class__}")


class ScoringDeck(BaseDeck[ScoringCard]):
    generic_card = ScoringCard

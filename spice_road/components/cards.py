import re
from copy import copy
from typing import Dict

from playtest.components import Card, Deck as BaseDeck
from .resources import Resource


class TraderCard(Card):
    re_value = re.compile(r"([RGBY]*)\s*->\s*([RGBY]*)")

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

    @staticmethod
    def get_all_cards():
        data = read_yaml(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "trader.yml")
        )
        return [
            SpellCard(f"{d['src']} -> {d['dst']}", uid=i) for i, d in enumerate(data)
        ]

    def can_trade(self, r: Resource) -> bool:
        return r.has_required(self.src)

    def trade(self, r: Resource) -> Resource:
        r2 = copy(r)
        r2.sub_resource(self.src)
        r2.add_resource(self.dst)
        return r2


class ConversionCard(TraderCard):
    re_value = re.compile(r"Convert\((\d+)\)")

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

    @staticmethod
    def get_all_cards():
        return [ConversionCard("Convert(2)") * 2]

    def can_trade(self, r: Resource) -> bool:
        return len(r) >= self.c

    def trade(self, r: Resource) -> Resource:
        assert len(r) == self.c, f"Must provide exact count of resource ({r})"
        r2 = Resource("")
        for val in r.value:
            # Upgrade the resource
            r2.add_resource(Resource(Resource.upgrade_char(val)))
        return r2


class TraderDeck(BaseDeck[Card]):
    generic_card = Card


class ScoringCard(Card):
    def check_enough(self, r: Resource) -> bool:
        """Check if the resource is sufficient for the cards
        """
        raise NotImplementedError()


class ScoringDeck(BaseDeck[ScoringCard]):
    generic_card = ScoringCard

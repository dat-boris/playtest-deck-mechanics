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
            os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "trader.yml")
        )
        return [
            SpellCard(f"{d['src']} -> {d['dst']}", uid=i) for i, d in enumerate(data)
        ]

    def can_trade(self, r: Resource) -> bool:
        return r.has_required(self.src)

    def trade_in_place(self, r: Resource) -> None:
        assert self.can_trade(r)
        r.sub_resource(self.src)
        r.add_resource(self.dst)

    def trade(self, r: Resource) -> Resource:
        r2 = copy(r)
        self.trade_in_place(r2)
        return r2


class ConversionCard(TraderCard):
    def can_trade(self, r: Resource) -> bool:
        raise NotImplementedError()

    def trade(self, r: Resource) -> Resource:
        raise NotImplementedError()


class TraderDeck(BaseDeck[Card]):
    generic_card = Card


class ScoringCard(Card):
    def check_enough(self, r: Resource) -> bool:
        """Check if the resource is sufficient for the cards
        """
        raise NotImplementedError()


class ScoringDeck(BaseDeck[ScoringCard]):
    generic_card = ScoringCard

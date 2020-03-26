from typing import List, Dict, TypeVar, Sequence, Generic, Type, Tuple

from playtest.components import Card, Deck

from .resources import Resource
from .cards import ScoringCard, TraderCard
from .coins import Coin


C = TypeVar("C", bound=Card)
R = TypeVar("R", bound=Resource)


class BaseRiver(Deck, Generic[C, R]):
    # Note: generic_card is still not implemented
    # generic_card = None
    generic_resource: Type[R]
    resources: List[R]

    def __init__(self, cards=[], resources=None, **kwargs):
        super().__init__(cards, **kwargs)
        self.resources = resources
        if resources is None:
            self.resources = [self.generic_resource("") for _ in self.cards]
        assert len(self.resources) == len(self.cards)
        assert all([isinstance(r, self.generic_resource) for r in self.resources])

    def add_resource(self, pos: int, resource: R):
        assert len(self.resources) >= pos, f"No resource found at position {pos}"
        self.resources[pos].add_resource(resource)

    def __getitem__(self, i: int):
        assert isinstance(i, int)
        return {
            "card": self.cards[i],
            "resources": self.resources[i],
        }

    def add(self, card: C):
        self.resources.append(self.generic_resource(""))
        self.cards.append(card)

    def remove(self, card: C):
        self.cards.remove(card)
        # TODO: remove token
        raise NotImplementedError()

    def pop_at(self, pos:int) -> Tuple[C, R]:
        card = self.cards.pop(pos)
        resource = self.resources.pop(pos)
        return card, resource


class ScoringRiver(BaseRiver[ScoringCard, Coin]):
    generic_card = ScoringCard
    generic_resource = Coin


class TraderRiver(BaseRiver[TraderCard, Resource]):
    generic_card = TraderCard
    generic_resource = Resource

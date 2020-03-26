import logging
from copy import copy
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
    init_resources: List[R]

    def __init__(self, cards=[], resources=None, **kwargs):
        self.resources = resources
        if resources is None:
            self.resources = [self.generic_resource("") for _ in cards]
        self.init_resources = copy(self.resources)

        super().__init__(cards, **kwargs)

        assert len(self.resources) == len(
            self.cards
        ), f"We have {len(self.cards)} cards vs {len(self.resources)} resources"
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

    def add(self, card: C, resource=None):
        if resource is None:
            resource = self.generic_resource("")
        self.resources.append(resource)
        self.cards.append(card)
        assert len(self.cards) == len(
            self.resources
        ), f"We have {len(self.cards)} cards vs {len(self.resources)} resources"

    def remove(self, card: C):
        self.cards.remove(card)
        # TODO: remove token
        raise NotImplementedError()

    def replace_from(self, deck: Deck):
        if len(deck) > 0:
            deck.deal(self, count=1)
        else:
            logging.warn(f"No more cards in deck {deck.__class__}")

    def pop(self, index: int = -1) -> Tuple[C, R]:  # type: ignore
        card = self.cards.pop(index)
        resource = self.resources.pop(index)
        return card, resource

    def reset(self):
        self.cards = copy(self.init_cards)
        self.resources = copy(self.init_resources)


class TraderRiver(BaseRiver[TraderCard, Resource]):
    generic_card = TraderCard
    generic_resource = Resource


class ScoringRiver(BaseRiver[ScoringCard, Coin]):
    generic_card = ScoringCard
    generic_resource = Coin

    def pop(self, index: int = -1) -> Tuple[ScoringCard, Coin]:  # type: ignore
        """We only pop one coin from the list"""
        card: ScoringCard = self.cards.pop(index)
        resource: Coin = self.resources[index].pop_lowest(1)
        # pop last resource
        self.resources.pop()
        assert len(self.cards) == len(self.resources)
        return card, resource

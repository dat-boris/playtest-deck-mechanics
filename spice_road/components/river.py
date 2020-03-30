import logging
import numpy as np
from copy import copy
from typing import List, Dict, TypeVar, Sequence, Generic, Type, Tuple

import gym.spaces as spaces

from playtest.components import BaseCard, Deck

from .resources import Resource
from .cards import ScoringCard, TraderCard
from .coins import Coin


C = TypeVar("C", bound=BaseCard)
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

    def to_data(self):
        return [
            {"card": c.to_data(), "resources": r.to_data(),}
            for c, r in zip(self.cards, self.resources)
        ]

    def get_observation_space(self) -> spaces.Space:
        # TODO: need to show resources also!
        return spaces.Box(
            low=0,
            high=self.generic_card.total_unique_cards,
            shape=(self.max_size,),
            dtype=np.uint8,
        )

    def to_numpy_data(self) -> np.ndarray:
        # TODO: need to show resources also!
        value_array = [c.to_numpy_data() for c in self.cards]
        assert len(value_array) <= self.max_size
        return np.array(
            value_array + [0] * (self.max_size - len(value_array)), dtype=np.uint8
        )


class TraderRiver(BaseRiver[TraderCard, Resource]):
    generic_card = TraderCard
    generic_resource = Resource


class ScoringRiver(BaseRiver[ScoringCard, Coin]):
    generic_card = ScoringCard
    generic_resource = Coin

    def pop(self, index: int = -1) -> Tuple[ScoringCard, Coin]:  # type: ignore
        """We only pop one coin from the list"""
        card: ScoringCard = self.cards.pop(index)
        if len(self.resources[index]) > 0:
            resource: Coin = self.resources[index].pop_lowest(1)
        else:
            resource = Coin("")
        # pop last resource - so we keep number of resource same
        self.resources.pop()
        assert len(self.cards) == len(self.resources)
        return card, resource

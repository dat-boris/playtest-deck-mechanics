

from playtest.components import Card, Deck as BaseDeck
from .resources import Resource


class TraderCard(Card):
    def can_trade(self, r: Resource) -> bool:
        raise NotImplementedError()

    def trade(self, r: Resource) -> Resource:
        raise NotImplementedError()


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

from playtest.components import Card, Deck as BaseDeck


class TraderDeck(BaseDeck[Card]):
    generic_card = Card


class ScoringDeck(BaseDeck[Card]):
    generic_card = Card

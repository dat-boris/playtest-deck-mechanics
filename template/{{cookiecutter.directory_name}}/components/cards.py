from playtest.components import Card, Deck as BaseDeck


class Deck(BaseDeck[Card]):
    generic_card = Card

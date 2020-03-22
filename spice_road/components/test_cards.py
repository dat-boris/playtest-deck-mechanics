from playtest.components import Card

from .cards import Deck


def test_deck():
    """## Deck

    The deck consists of 52 cards.  Just standard deck of cards.
    """
    d = Deck(all_cards=True)
    assert len(d) == 52
    assert Card("Ad") in d, "Ace of diamond is in the deck"

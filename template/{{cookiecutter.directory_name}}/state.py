from typing import Dict, Type


from playtest import Param, SubState, FullState, Visibility
from playtest.components import Component, Counter


from .components.cards import Deck


class PlayerState(SubState):
    visibility = {
        "hand": Visibility.ALL,
    }

    hand: Deck

    def __init__(self, param=None):
        self.hand = Deck([])


class State(FullState[PlayerState]):
    player_state_class = PlayerState

    visibility = {
        # Deck is face down and nobody can see it
        "deck": Visibility.NONE,
    }

    deck: Deck

    def __init__(self, param=None):
        self.deck = Deck(all_cards=True)
        super().__init__(param=param)

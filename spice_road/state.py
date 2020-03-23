from typing import Dict, Type


from playtest import Param, SubState, FullState, Visibility
from playtest.components import Component, Counter


from .components.cards import TraderDeck, ScoringDeck
from .components.river import ScoringRiver, TraderRiver
from .components.resources import Caravan
from .components.coins import Coin


class PlayerState(SubState):
    visibility = {
        "hand": Visibility.SELF,
        "used_hand": Visibility.ALL,
        "caravan": Visibility.ALL,
        "scored": Visibility.ALL,
        "coins": Visibility.ALL,
    }

    hand: TraderDeck
    used_hand: TraderDeck
    caravan: Caravan
    scored: ScoringDeck
    coins: Coin

    def __init__(self, param=None):
        self.hand = TraderDeck([])
        self.used_hand = TraderDeck([])
        self.scored = ScoringDeck([])
        self.coins = Coin({})
        self.caravan = Caravan({})


class State(FullState[PlayerState]):
    player_state_class = PlayerState

    visibility = {
        # Deck is face down and nobody can see it
        "trader_deck": Visibility.NONE,
        "scoring_deck": Visibility.NONE,
        "scoring_river": Visibility.ALL,
        "trader_river": Visibility.ALL,
    }

    trader_deck: TraderDeck
    scoring_deck: ScoringDeck
    scoring_river: ScoringRiver
    trader_river: TraderRiver

    def __init__(self, param=None):
        self.trader_deck = TraderDeck(all_cards=True)
        self.scoring_deck = ScoringDeck(all_cards=True)
        self.scoring_river = ScoringRiver([])
        self.trader_river = TraderRiver([])
        super().__init__(param=param)

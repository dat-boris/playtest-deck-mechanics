import pytest
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
        self.coins = Coin("")
        self.caravan = Caravan("")


@pytest.mark.xfail
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

        self.reset()

    def reset(self):
        super().reset()
        # Deal tokens to players
        number_of_players = len(self.players)
        assert 2 <= number_of_players <= 5
        # According to rules, number of players th
        player_assets = ["YYY", "YYYY", "YYYY", "YYYR", "YYYR"]
        for i, p in enumerate(self.players):
            p.caravan = Caravan(player_assets[i])

        # Setting up the river
        self.scoring_deck.deal(self.scoring_river, count=5)
        self.scoring_river.add_resource(0, Coin("G" * number_of_players))
        self.scoring_river.add_resource(1, Coin("S" * number_of_players))

        self.trader_deck.deal(self.trader_river, count=6)

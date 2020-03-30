import re
from itertools import combinations_with_replacement
import numpy as np
from typing import Set, Optional, List


import gym.spaces as spaces

from playtest.action import (
    ActionSingleValue,
    ActionSingleValueRange,
    ActionSingleValue,
    ActionValueInSet,
    ActionValueInSetRange,
    ActionBoolean,
    ActionBooleanRange,
    ActionWaitRange,
    ActionInstance,
    ActionRange,
    ActionFactory as BaseAF,
    InvalidActionError,
)

from .constants import Param
from .state import State, PlayerState
from .components.resources import Resource
from .components.coins import Coin
from .components.cards import TraderCard, ScoringCard, ConversionCard


class ActionTrade(ActionValueInSet[State, int]):
    key = "trade"

    value_set_mapping = list(range(Param.max_card_in_hand))
    unique_value_count = Param.max_card_in_hand
    coerce_int = True

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        ps: PlayerState = s.get_player_state(player_id)
        card = ps.hand[self.value]
        if a:
            a.say(f"Player {player_id+1} playing card {card}")
        if card.__class__ == TraderCard:
            ps.hand.remove(card)
            ps.caravan = card.trade(ps.caravan)
            ps.used_hand.add(card)
            return None
        elif card.__class__ == ConversionCard:
            assert isinstance(card, ConversionCard)
            ps.hand.remove(card)
            ps.used_hand.add(card)
            # Now given the conversion action, let's setup the action
            return ActionConvertRange(s, player_id=player_id, trade_count=card.c)
        else:
            raise NotImplementedError(f"Unknown card: {card}")


class ActionTradeRange(ActionValueInSetRange[ActionTrade, State, int]):
    instance_class = ActionTrade

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        self.possible_values = set()
        if len(ps.hand) == 0:
            self.actionable = False
            return
        self.possible_values = set(
            [i for i, s in enumerate(ps.hand) if s.can_trade(ps.caravan)]
        )
        self.actionable = bool(self.possible_values)


class ActionConvert(ActionValueInSet[State, str]):
    key = "convert"
    value_set_mapping: List[str] = (
        list(
            map(
                lambda s: "".join(s),
                combinations_with_replacement(Resource.all_resources_short, r=1),
            )
        )
        + list(
            map(
                lambda s: "".join(s),
                combinations_with_replacement(Resource.all_resources_short, r=2),
            )
        )
        + list(
            map(
                lambda s: "".join(s),
                combinations_with_replacement(Resource.all_resources_short, r=3),
            )
        )
    )
    unique_value_count = len(value_set_mapping)

    value: str

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        # Converting given values
        ps = s.get_player_state(player_id)
        resource_to_trade = Resource(self.value)
        conversion_card = ps.used_hand[-1]
        assert isinstance(
            conversion_card, ConversionCard
        ), f"Top used card {conversion_card} must be a conversion card"

        ps.caravan.sub_resource(resource_to_trade)
        ps.caravan.add_resource(conversion_card.trade(resource_to_trade))
        return None


class ActionConvertRange(ActionValueInSetRange[ActionConvert, State, str]):
    instance_class = ActionConvert

    def __init__(self, state: State, player_id: int, trade_count: Optional[int] = None):
        ps = state.get_player_state(player_id)
        if trade_count is None:
            self.actionable = False
            self.possible_values = set()
            return
        self.actionable = True
        assert (
            len(ps.caravan) >= trade_count
        ), f"Player {player_id+1} must have enough resource {ps.caravan}"
        self.possible_values = set(
            [
                r
                for r in ActionConvert.value_set_mapping
                if len(r) == trade_count and ps.caravan.has_required(Resource(r))
            ]
        )
        assert self.possible_values, f"No trade possible with {ps.caravan}"


class ActionAcquire(ActionValueInSet[State, int]):
    key = "acquire"

    value_set_mapping = list(range(Param.number_of_trader_slots))
    unique_value_count = Param.number_of_trader_slots
    coerce_int = True

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        # Now leave the resources you need
        river = s.trader_river
        ps = s.get_player_state(player_id)
        for i in range(self.value):
            river.add_resource(i, ps.caravan.pop_lowest(1))

        # Get the card from trader slot + resources
        card, resource = river.pop(index=self.value)
        if a:
            a.say(f"Player {player_id+1} acquired {card} (r={resource})")
        ps.hand.add(card)
        ps.caravan.add_resource(resource)
        s.trader_river.replace_from(s.trader_deck)
        return None


class ActionAcquireRange(ActionValueInSetRange[ActionAcquire, State, int]):
    instance_class = ActionAcquire

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        number_of_resources = len(ps.caravan)
        self.possible_values = set(
            [i for i, s in enumerate(state.trader_river) if i <= number_of_resources]
        )
        self.actionable = bool(self.possible_values)


class ActionRest(ActionBoolean[State]):
    key = "rest"

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        ps = s.get_player_state(player_id)
        ps.used_hand.deal(ps.hand, all=True)
        return None


class ActionRestRange(ActionBooleanRange[ActionRest, State]):
    instance_class = ActionRest


class ActionScore(ActionValueInSet[State, int]):
    key = "score"

    value_set_mapping = list(range(Param.number_of_scoring_slots))
    unique_value_count = Param.number_of_scoring_slots
    coerce_int = True

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        ps = s.get_player_state(player_id)
        card, resource = s.scoring_river.pop(self.value)
        assert isinstance(resource, Coin)
        ps.caravan.sub_resource(card.target)
        ps.scored.add(card)
        ps.coins.add_resource(resource)
        s.scoring_river.replace_from(s.scoring_deck)
        return None


class ActionScoreRange(ActionValueInSetRange[ActionScore, State, int]):
    instance_class = ActionScore

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        self.possible_values = set(
            [
                i
                for i, s in enumerate(state.scoring_river)
                if ps.caravan.has_required(s.target)
            ]
        )
        self.actionable = bool(self.possible_values)


class ActionFactory(BaseAF):
    range_classes = [
        ActionTradeRange,
        ActionConvertRange,
        ActionAcquireRange,
        ActionRestRange,
        ActionScoreRange,
        ActionWaitRange,
    ]

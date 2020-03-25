import re
from itertools import combinations_with_replacement
import numpy as np
from typing import Set, Optional, List


import gym.spaces as spaces

from playtest.action import (
    ActionSingleValue,
    ActionSingleValueRange,
    ActionSingleValue,
    ActionValueInSetRange,
    ActionBoolean,
    ActionBooleanRange,
    ActionWaitRange,
    ActionInstance,
    ActionRange,
    ActionFactory as BaseAF,
    InvalidActionError,
)

from .state import State, PlayerState
from .components.resources import Resource
from .components.cards import TraderCard, ScoringCard, ConversionCard


class ActionTrade(ActionSingleValue[State]):
    key = "trade"
    minimum_value: int = 0
    maximum_value: int = TraderCard.total_unique_cards + ScoringCard.total_unique_cards

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        ps: PlayerState = s.get_player_state(player_id)
        card = [s for s in ps.hand if s.uid == self.value][0]
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


class ActionTradeRange(ActionValueInSetRange[ActionTrade, State]):
    instance_class = ActionTrade
    max_values_in_set = TraderCard.total_unique_cards

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        if len(ps.hand) == 0:
            self.actionable = False
            return
        self.actionable = True
        self.values_set = set([s.uid for s in ps.hand if s.can_trade(ps.caravan)])

    def value_to_position(self, value) -> int:
        return value

    def position_to_value(self, pos: int):
        return pos


class ActionConvert(ActionSingleValue[State]):
    key = "convert"
    all_possible_set_value: List[str] = (
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
    minimum_value: int = 0
    maximum_value: int = len(all_possible_set_value)

    value: str  # type: ignore

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


class ActionConvertRange(ActionValueInSetRange[ActionConvert, State]):
    instance_class = ActionConvert
    max_values_in_set = ActionConvert.maximum_value

    values_set: Set[str]  # type: ignore

    def __init__(self, state: State, player_id: int, trade_count: int):
        self.actionable = True
        ps = state.get_player_state(player_id)
        self.values_set = set(
            [
                r
                for r in ActionConvert.all_possible_set_value
                if len(r) == trade_count and ps.caravan.has_required(Resource(r))
            ]
        )
        assert self.values_set, f"Cannot trade for player resource {ps.caravan}"

    def value_to_position(self, value: str) -> int:
        return ActionConvert.all_possible_set_value.index(value)

    def position_to_value(self, pos: int) -> str:
        return ActionConvert.all_possible_set_value[pos]


class ActionAcquire(ActionSingleValue[State]):
    key = "acquire"


class ActionAcquireRange(ActionValueInSetRange[ActionAcquire, State]):
    instance_class = ActionAcquire


class ActionRest(ActionBoolean[State]):
    key = "rest"


class ActionRestRange(ActionBooleanRange[ActionRest, State]):
    instance_class = ActionRest


class ActionScore(ActionSingleValue[State]):
    key = "score"


class ActionScoreRange(ActionValueInSetRange[ActionScore, State]):
    instance_class = ActionScore


class ActionFactory(BaseAF):
    range_classes = [
        ActionTradeRange,
        ActionConvertRange,
        ActionAcquireRange,
        ActionRestRange,
        ActionScoreRange,
        ActionWaitRange,
    ]

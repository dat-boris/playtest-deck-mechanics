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

from .constants import Param
from .state import State, PlayerState
from .components.resources import Resource
from .components.coins import Coin
from .components.cards import TraderCard, ScoringCard, ConversionCard


class ActionTrade(ActionSingleValue[State]):
    key = "trade"
    minimum_value: int = 0
    maximum_value: int = TraderCard.total_unique_cards + ScoringCard.total_unique_cards

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


class ActionTradeRange(ActionValueInSetRange[ActionTrade, State]):
    instance_class = ActionTrade
    max_values_in_set = TraderCard.total_unique_cards

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        self.values_set = set()
        if len(ps.hand) == 0:
            self.actionable = False
            return
        self.values_set = set(
            [i for i, s in enumerate(ps.hand) if s.can_trade(ps.caravan)]
        )
        self.actionable = bool(self.values_set)


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

    # Note that we use this as a str value
    def __init__(self, value: str):
        super().__init__(value)  # type: ignore

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

    def __init__(self, state: State, player_id: int, trade_count: Optional[int] = None):
        ps = state.get_player_state(player_id)
        self.values_set = set()
        if trade_count is None:
            self.actionable = False
            return
        self.actionable = True
        assert (
            len(ps.caravan) >= trade_count
        ), f"Player {player_id+1} must have enough resource {ps.caravan}"
        self.values_set = set(
            [
                r
                for r in ActionConvert.all_possible_set_value
                if len(r) == trade_count and ps.caravan.has_required(Resource(r))
            ]
        )
        assert self.values_set, f"No trade possible with {ps.caravan}"

    def value_to_position(self, value: str) -> int:
        return ActionConvert.all_possible_set_value.index(value)

    def position_to_value(self, pos: int) -> str:
        return ActionConvert.all_possible_set_value[pos]


class ActionAcquire(ActionSingleValue[State]):
    key = "acquire"

    minimum_value: int = 0
    maximum_value: int = Param.number_of_trader_slots

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
        s.trader_river.replace_from(s.trader_deck)
        return None


class ActionAcquireRange(ActionValueInSetRange[ActionAcquire, State]):
    instance_class = ActionAcquire
    max_values_in_set = Param.number_of_trader_slots

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        number_of_resources = len(ps.caravan)
        self.values_set = set(
            [i for i, s in enumerate(state.trader_deck) if i <= number_of_resources]
        )
        self.actionable = bool(self.values_set)


class ActionRest(ActionBoolean[State]):
    key = "rest"

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        ps = s.get_player_state(player_id)
        ps.used_hand.deal(ps.hand, all=True)
        return None


class ActionRestRange(ActionBooleanRange[ActionRest, State]):
    instance_class = ActionRest


class ActionScore(ActionSingleValue[State]):
    key = "score"

    def resolve(self, s: State, player_id: int, a=None) -> Optional[ActionRange]:
        ps = s.get_player_state(player_id)
        card, resource = s.scoring_river.pop(self.value)
        assert isinstance(resource, Coin)
        ps.caravan.sub_resource(card.target)
        ps.scored.add(card)
        ps.coins.add_resource(resource)
        s.scoring_river.replace_from(s.scoring_deck)
        return None


class ActionScoreRange(ActionValueInSetRange[ActionScore, State]):
    instance_class = ActionScore
    max_values_in_set = Param.number_of_scoring_slots

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        self.values_set = set(
            [
                i
                for i, s in enumerate(state.scoring_river)
                if ps.caravan.has_required(s.target)
            ]
        )
        self.actionable = bool(self.values_set)


class ActionFactory(BaseAF):
    range_classes = [
        ActionTradeRange,
        ActionConvertRange,
        ActionAcquireRange,
        ActionRestRange,
        ActionScoreRange,
    ]

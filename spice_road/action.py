from playtest.action import (
    ActionSingleValue,
    ActionSingleValueRange,
    ActionSingleValue,
    ActionValueInSetRange,
    ActionBoolean,
    ActionBooleanRange,
    ActionWaitRange,
    ActionFactory as BaseAF,
)

from .state import State, PlayerState
from .components.cards import TraderCard, ScoringCard


class ActionTrade(ActionSingleValue[State]):
    key = "trade"
    minimum_value: int = 0
    maximum_value: int = TraderCard.total_unique_cards + ScoringCard.total_unique_cards

    def resolve(self, s: State, player_id: int, a=None):
        ps: PlayerState = s.get_player_state(player_id)
        card = [s for s in ps.hand if s.uid == self.value][0]
        if a:
            a.say(f"Player {player_id+1} playing card {card}")
        ps.hand.remove(card)
        ps.caravan = card.trade(ps.caravan)
        ps.used_hand.add(card)


class ActionTradeRange(ActionValueInSetRange[ActionTrade, State]):
    instance_class = ActionTrade
    max_values_in_set = TraderCard.total_unique_cards + ScoringCard.total_unique_cards

    def __init__(self, state: State, player_id: int):
        ps: PlayerState = state.get_player_state(player_id)
        if len(ps.hand) == 0:
            self.actionable = False
            return
        self.actionable = True
        self.values_set = set(
            [s.uid for s in ps.hand if s.can_trade(ps.caravan)])

    def value_to_position(self, value) -> int:
        return value

    def position_to_value(self, pos: int):
        return pos


class ActionConvert(ActionSingleValue[State]):
    key = "exchange"


class ActionConvertRange(ActionValueInSetRange[ActionConvert, State]):
    instance_class = ActionConvert


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

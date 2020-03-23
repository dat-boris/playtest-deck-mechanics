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

from .state import State


class ActionTrade(ActionSingleValue[State]):
    key = "trade"

    def resolve(self, s: State, player_id: int, a=None):  # type: ignore
        if a:
            a.say("Do nothing!")
        pass


class ActionTradeRange(ActionSingleValueRange[ActionTrade, State]):
    instance_class = ActionTrade


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

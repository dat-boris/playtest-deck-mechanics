from playtest.action import (
    ActionBoolean,
    ActionBooleanRange,
    ActionWaitRange,
    ActionFactory as BaseAF,
)

from .state import State


class ActionSkip(ActionBoolean[State]):
    key = "skip"

    def resolve(self, s: State, player_id: int, a=None):  # type: ignore
        if a:
            a.say("Do nothing!")
        pass


class ActionSkipRange(ActionBooleanRange[ActionSkip, State]):
    instance_class = ActionSkip


class ActionHit(ActionBoolean[State]):
    key = "hit"

    def resolve(self, s: State, player_id: int, a=None):  # type: ignore
        if a:
            a.say(f"Give 1 card to player {player_id}!")

        s.deck.deal(s.players[player_id].hand)


class ActionHitRange(ActionBooleanRange[ActionHit, State]):
    instance_class = ActionHit


class ActionFactory(BaseAF):
    range_classes = [
        ActionHitRange,
        ActionSkipRange,
        ActionWaitRange,
    ]

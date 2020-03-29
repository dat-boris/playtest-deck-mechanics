#!/usr/bin/env python
"""Run interactive agent for argparse
"""
import argparse
from pprint import pprint
from importlib import import_module

import gym

from playtest.env import GameWrapperEnvironment, EnvironmentInteration
from playtest.agents import HumanAgent

AGENT_COUNT = 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive Agent for ma-gym")
    parser.add_argument("game", help="Game ID (folder name) to play")
    parser.add_argument(
        "--players", type=int, default=4, help="episodes (default: %(default)s)"
    )
    parser.add_argument(
        "--ai", action="store_true", help="Play against AI"
    )
    args = parser.parse_args()

    game_module = import_module(args.game + ".game")
    game_class = getattr(game_module, "Game", None)
    assert game_class, f"Cannot find {args.game}.game.Game class"
    param_class = getattr(game_module, "Param", None)
    assert param_class, f"Cannot find {args.game}.game.Param class"

    __game = game_class(param_class(number_of_players=args.players))
    env: GameWrapperEnvironment = GameWrapperEnvironment(__game)

    assert not args.ai, "AI should be implemented"
    agents = [HumanAgent(env) for i in range(env.n_agents)]

    game = EnvironmentInteration(env, agents, episodes=1)
    game.play()

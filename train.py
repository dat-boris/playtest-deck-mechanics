#!/usr/bin/env python
"""Run interactive agent for argparse
"""
import argparse
from pprint import pprint
from importlib import import_module

import gym

from playtest.env import GameWrapperEnvironment
from playtest.agents import KerasDQNAgent, train_agents

AGENT_COUNT = 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive Agent for ma-gym")
    parser.add_argument(
        "--episodes", type=int, default=100000, help="episodes (default: %(default)s)"
    )
    parser.add_argument(
        "--players",
        type=int,
        default=4,
        help="Number of players (default: %(default)s)",
    )
    parser.add_argument("--pdb", action="store_true", help="Add debugger on error")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print verbose message"
    )
    parser.add_argument(
        "--output", type=str, help="Output agent file (default: %(default)s)",
    )
    parser.add_argument("game", help="Game ID (folder name) to play")
    args = parser.parse_args()

    game_module = import_module(args.game + ".game")
    game_class = getattr(game_module, "Game", None)
    assert game_class, f"Cannot find {args.game}.game.Game class"
    param_class = getattr(game_module, "Param", None)
    assert param_class, f"Cannot find {args.game}.game.Param class"

    filename = args.output
    if not filename:
        filename = f"agent_{args.game}.h5f"

    __game = game_class(
        param_class(number_of_players=args.players), verbose=args.verbose
    )
    env: GameWrapperEnvironment = GameWrapperEnvironment(__game, verbose=args.verbose)

    agents = [KerasDQNAgent(env) for _ in range(env.n_agents)]

    train_agents(
        env, agents, save_filenames=[filename], nb_steps=args.episodes, is_pdb=True,
    )

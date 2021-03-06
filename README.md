# Playtest deck mechanics

[![Build Status](https://travis-ci.com/dat-boris/playtest-deck-mechanics.svg?branch=master)](https://travis-ci.com/dat-boris/playtest-deck-mechanics)

This is a repository that is my collection of game mechanics that I simplify
into a 52 card deck, and a few tokens and dices.

This makes use of the [PyPlaytest](https://github.com/dat-boris/py-playtest)
framework.

# Getting start

To run any of the game, run:

```
PYTHONPATH=. ./play.py <game_name>
```

## Generating the rules

The rules are extracted from various docstring from the test cases.
If you are interesting in reading and extending the mechanics of
the game,  it is recommended to follow the order of `<game module>.RULE_TESTS`
array.

To regenerate the rules, please run:
```
./mk_rules.py <game_name>
```


## Creating a new game

To create a new game, you can use the cookie cutter template

```
$ pipenv install --dev
$ pipenv run cookiecutter template/
# Following questions will be asked....
directory_name [example_game]:
designer [John Doe]:
game_name [Example Game]:
buy_url [http://original_publisher_link.com/]:
bgg_url [https://www.boardgamegeek.com/boardgame/...]:
```

Which will then create a scaffold for your game.  Then you can start creating
the game as expected.


## Disclaimer

All games referenced is in reference to the original game, and are
derivative work under *fair use*, as a mean to model and study of
and critique of the original game.

Original link and purchase are referenced in the game, and interested
parties are encouraged to buy the original version of the game.

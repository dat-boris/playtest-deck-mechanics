# Century: Spice Road

*Game designer*: Emerson Matsuuchi

*Boardgame geek URL*: https://boardgamegeek.com/boardgame/209685/century-spice-road

*Purchase link*: https://www.planbgames.com/en/all-our-games/8-century-spice-road.html

Century: Spice Road is a engine builder game, focus on the timing of how you
trying to achieve your victory card mechanics.  This is a great game to study,
with it's elegant mechanism for building tension within the game.


## Disclaimer

This simulation is meant to be a tool for studying the game mechanics of the
original game. This is derivative work under *fair use*, as a mean to model and
study of and critique of the original game.

Any questions, please do reach out to the author of the repository.

Original link and purchase are referenced in the game, and interested
parties are encouraged to buy the original version of the game.


## Resources

* [Homemade Rule book](https://www.fgbradleys.com/rules/rules5/Century-Spice_Road_EN_Rules.pdf)
* [Reference card list](https://boardgamegeek.com/thread/1896169/list-all-cards-merchants-points-and-analysis-their)
* [Jamey Stegmaier's comments](https://www.youtube.com/watch?v=FBL3nxNtbik)


## To play

See root folder's README

```
./play.py spice_road
```


# Steps to create this game

We encourage a [Docs driven development](https://gist.github.com/zsup/9434452) approach -
and in this case, create the rules first.

If you run

```
./mk_rules.py spice_road
```

You will see the [spice_road/RULES.md](RULES.md) being
generated.  We encourage filling out his rulebook before getting started
with the development.

### 1. Filling in the rules

1. From `spice_road/__init__.py` fill in the list of tests.
2. For each tests, you can describe the behaviour, and match in with the
   behaviour that the test is trying to satisfy.
3. Rerun `mk_rules.py` to review the tests.

### 2. Writing the tests

Once satisfy, you can start writing the tests!


### 3. Writing the code

Well, this is the part where you actually write the implementation of the game.

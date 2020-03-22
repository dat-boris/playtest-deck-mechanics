# Century: Spice Road


*Boardgame geek URL*: https://boardgamegeek.com/boardgame/209685/century-spice-road

> TODO: Add brief description of the game.

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

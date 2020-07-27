## Description
pseu is a command line tool that provides several pseudorandom utilities:

* shuffling.
* dice rolling.
* number generation.
* choice from a list.

## Commands
#### roll (DONE)

```
pseu roll # rolls 1d6 by default
pseu roll 1d3
pseu roll 2d3
pseu roll 2d3 5d7
pseu roll 2d3 --stats
pseu roll 2d3 --seed abc
```

#### rand (DONE)

```
pseu rand # [0, 2^16)
pseu rand 5 # 0-4
pseu rand 1-3
pseu rand 1-3x5 # repeat 5 times
pseu rand 1-3x5 --stats
pseu rand 1-3 --seed abc
```

#### shuffle

```
pseu shuffle bob alice pete # output: alice pete bob
pseu shuffle --sep ';' 1;2;pizza;3
pseu shuffle --lines # shuffles around the lines
echo '[1, 2, 3]' | pseu shuffle --json
```

#### pick

```
pseu pick --lines  # pick a line
pseu pick --sep ';' 1;2;pizza;3
pseu pick bob alice judy
pseu pick --n 2 bob alice judy
echo '[1, 2, 3]' | pseu pick --json --n 2
```

#### MORE IDEAS
* Output in different bases.
* String (e.g. random hex string of 16 chars, random base64).
* Date/time (specific day of the week: random Monday in 2006, for example).
* An image/bitmap of some description.
* Random colour.
* But, come on. Reign it in. 1) Only implement things that are useful for me, otherwise I'll never use them and they won't be well-tested. 2) More commands and options -> more docs to maintain, more complexity, etc. And more difficult to grasp the tool in its entirety. 3) There should be only 1 way to do things.

## Installation
TODO

## TODO
* Input through stdin or arglist.
* json input (shuffle, pick).
* Linewise vs whole input.
* Maybe number gen and dice rolling don't need such flexible options, they just search & replace. Then you could use them to replace stuff in a document.
* Ask D&D types for their opinions, what would be useful? Maybe the ability to identify a crit?

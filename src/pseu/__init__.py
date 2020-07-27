#!/usr/bin/env python3

import argparse
import re
import random as rd

BASE64_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

ROLL_REG = re.compile("^([1-9][0-9]*)d([1-9][0-9]*)$")

JUST_NUM_RAND_REG = re.compile("^[1-9][0-9]*$")
DASH_RAND_REG = re.compile("^([0-9]+)-([0-9]+)(x([1-9][0-9]*))?$")

def out(msg, *fmt_args):
    print(msg.format(*fmt_args))

def roll(rnd, raw_dices, stats):
    do_rand(
        rnd,
        [Range(1, 1, 6)]
            if not raw_dices
            else [parse_dice(s) for s in raw_dices],
        stats)

def parse_dice(s):
    match = ROLL_REG.match(s)
    if not match:
        raise ValueError("Invalid dice format: " + s)
    return Range(
        int(match.group(1)),
        1,
        int(match.group(2)))

class Range:
    def __init__(self, times, lb, ub):
        self.times = times
        self.lb = lb
        self.ub = ub

    def get_nums(self, rnd):
        return [rnd.randint(self.lb, self.ub) for _ in range(self.times)]

def parse_range(s):
    m = JUST_NUM_RAND_REG.match(s)
    if m:
        return Range(1, 0, int(s)-1)
    m = DASH_RAND_REG.match(s)
    if m:
        lb = int(m.group(1))
        ub = int(m.group(2))
        if lb > ub:
            raise ValueError("Lower bound must be <= upper bound: " + s)
        return Range(int(m.group(4)) if m.group(4) else 1, lb, ub)
    raise ValueError("Invalid range: " + s)

def rand(rnd, raw_ranges, stats):
    do_rand(
        rnd,
        [Range(1, 0, 2**16-1)]
            if not raw_ranges
            else [parse_range(s) for s in raw_ranges],
        stats)

def do_rand(rnd, ranges, stats):
    results = []
    for r in ranges:
        for n in r.get_nums(rnd):
            results.append(n)
    out(" ".join(map(str, results)))
    if stats:
        out("sum: {}", sum(results))
        out("max: {}", max(results))
        out("min: {}", min(results))

def pick(rnd, js, n, lines, sep, words):
    # TODO other variations
    if words:
        # they haven't been separated for us by argparse
        if sep != " ":
            words = (" ".join(words)).split(sep)
        if n > len(words):
            raise ValueError(
                "n ({}) must be less than the number of words ({}).".format(
                n,
                len(words)))
        for word in rnd.sample(words, n):
            # TODO better output handling
            print(word)

class Arg:
    def __init__(self, name, *args, **kwargs):
        self.name = name.lstrip("-")
        self.raw_name = name
        self.args = args
        self.kwargs = kwargs

def add_subparser(subparsers, name, description, f, args):
    parser = subparsers.add_parser(name, help=description)
    for arg in args:
        parser.add_argument(arg.raw_name, *arg.args, **arg.kwargs)
    parser.add_argument(
        "--seed",
        required=False,
        help="base-64 seed.")
    def wrapped_func(cli_args):
        try:
            if cli_args.seed:
                r = rd.Random(parse_base64_seed(cli_args.seed))
            else:
                r = rd.Random()
            f(r, *[getattr(cli_args, arg.name) for arg in args])
        except Exception as e:
            # TODO show message, exit with failure.
            raise e
    parser.set_defaults(func=wrapped_func)

def parse_base64_seed(s):
    result = 0
    for i, c in enumerate(reversed(s)):
        try:
            result += BASE64_CHARS.index(c) * (64**i)
        except ValueError as e:
            # TODO raise a nicer exception
            raise e
    return result

STATS_ARG = Arg(
    "--stats",
    default=False,
    action="store_true",
    help="whether to print stats (sum, max, min)")
JSON_ARG = Arg(
    "--json",
    default=False,
    action="store_true",
    help="indicates whether input is in JSON format")

SUBCOMMANDS = [
    ("roll",
     "roll dice",
     roll,
     [Arg("dice", nargs="*", help="dice rolls, in the form {n}d{m}; 1d6 by default"),
      STATS_ARG]),
    ("rand",
     "generate random number",
     rand,
     [Arg(
        "range",
        nargs="*",
        help="number range, either {n}-{m} (inclusive bounds) or {n} (for [0, n)); [0, 2^16 - 1) by default"),
      STATS_ARG]),
    ("pick",
     "pick from a selection of words or lines",
     pick,
     [JSON_ARG,
      Arg(
        "--n",
        default=1,
        required=False,
        type=int,
        help="number of words/lines to pick"),
      Arg(
        "--lines",
        default=False,
        action="store_true",
        help="pick lines from the input instead of words"),
      Arg(
        "--sep",
        default=" ",
        required=False,
        help="how words are separated"),
      Arg(
        "words",
        nargs="*",
        help="the words to pick from; alternatively, input can be passed through stdin")])
]

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Functions")
    for name, description, f, args in SUBCOMMANDS:
        add_subparser(subparsers, name, description, f, args)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

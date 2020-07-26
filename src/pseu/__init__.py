#!/usr/bin/env python3

import argparse
import re
import random as rd

BASE64_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

ROLL_REG = re.compile("^([1-9][0-9]*)d([1-9][0-9]*)$")
RAND_REG = re.compile("([0-9]+)-([0-9]+)")

def out(msg, *fmt_args):
    print(msg.format(*fmt_args))

def roll(rnd, raw_dices, stats):
    if not raw_dices:
        dices = [Dice(1, 6)]
    else:
        dices = [Dice.parse(s) for s in raw_dices]
    results = []
    for dice in dices:
        for s in dice.get_rolls(rnd):
            results.append(s)
    out(" ".join(map(str, results)))
    if stats:
        out("sum: {}", sum(results))
        out("avg: {}", sum(results)/len(results))
        out("max: {}", max(results))
        out("min: {}", min(results))

class Dice:
    def __init__(self, times, sides):
        self.times = times
        self.sides = sides

    def get_rolls(self, rnd):
        return [rnd.randint(1, self.sides) for _ in range(self.times)]
    
    @classmethod
    def parse(cls, s):
        match = ROLL_REG.match(s)
        if not match:
            raise ValueError("Invalid dice format: " + s)
        return Dice(
            int(match.group(1)),
            int(match.group(2)))
        
def pick(args):
    out(rd.choice(args.options))

def shuffle(args):
    options = args.options[:]
    rd.shuffle(options)
    out(", ".join(options))

def rand(args):
    parsed_ranges = []
    for r in args.ranges:
        m = RAND_REG.match(r)
        if not m:
            raise ValueError("Invalid rand format, should be <n>-<m>")
        parsed_ranges.append((
            int(m.group(1)),
            int(m.group(2))))
    results = []
    for n, m in parsed_ranges:
        results.append(rd.randint(n, m))
    for x in results:
        out(x)
    out("sum: {}".format(sum(results)))
    out("max: {}".format(max(results)))
    out("min: {}".format(min(results)))

def add_pick_subparser(subparsers):
    parser = subparsers.add_parser("pick", help="pick from several options.")
    parser.add_argument(
        "options",
        nargs="+",
        help="options, aka strings.")
    parser.set_defaults(func=pick)

def add_shuffle_subparser(subparsers):
    parser = subparsers.add_parser("shuffle", help="shuffle options.")
    parser.add_argument(
        "options",
        nargs="+",
        help="options, aka strings.")
    parser.set_defaults(func=shuffle)

def add_rand_subparser(subparsers):
    parser = subparsers.add_parser("rand", help="generate random integers.")
    parser.add_argument(
        "ranges",
        nargs="+",
        help="ranges in which to generate the integers, in the form <n>-<m>.")
    parser.set_defaults(func=rand)

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

SUBCOMMANDS = [
    ("roll",
     "roll dice",
     roll,
     [Arg("dice", nargs="*", help="dice rolls, in the form {n}d{m}"),
      Arg("--stats",
          default=False,
          action="store_true",
          help="whether to print stats (sum, max, min, avg)")])
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

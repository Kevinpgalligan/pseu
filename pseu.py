import argparse
import re
import random as rd

ROLL_REG = re.compile("([1-9][0-9]*)d([1-9][0-9]*)")
RAND_REG = re.compile("([0-9]+)-([0-9]+)")

def out(msg):
    print(msg)

def roll(args):
    parsed_rolls = []
    for dice in args.dice:
        m = ROLL_REG.match(dice)
        if not m:
            raise ValueError("Invalid roll format, should be <n>d<m>")
        parsed_rolls.append((
            int(m.group(1)),
            int(m.group(2))))
    results = []
    for n, m in parsed_rolls:
        for _ in range(n):
            results.append(rd.randint(1, m))
    for x in results:
        out(x)
    out("sum: {}".format(sum(results)))
    out("max: {}".format(max(results)))
    out("min: {}".format(min(results)))

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

def add_roll_subparser(subparsers):
    parser = subparsers.add_parser(
        "roll",
        help="roll dice.")
    parser.add_argument(
        "dice",
        nargs="+",
        help="dice rolls, in the form <n>d<m>.")
    parser.set_defaults(func=roll)

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

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Functions")
    add_roll_subparser(subparsers)
    add_pick_subparser(subparsers)
    add_shuffle_subparser(subparsers)
    add_rand_subparser(subparsers)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

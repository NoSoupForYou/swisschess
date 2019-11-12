# -*- coding: utf-8 -*-
"""Swiss-style Pairings for Chess Tournaments

An implementation of the official USCF rules for Swiss System Tournaments,
published at https://new.uschess.org/home/
"""


from argparse import ArgumentParser
from csv import reader as csv_reader
import logging
from math import ceil
from math import log
from random import random
import sys


def pair_field(filename):
    """Pair the participants in the CSV pointed to by filename"""

    with open(filename) as f:
        field = tuple(tuple(l) for l in csv_reader(f))

    min_rounds = ceil(log(len(field), 2))
    logging.info((
        f"Read {len(field)} participants from {filename}. Will run at least "
        f"{min_rounds} rounds"))

    pairing = list(zip(field[:len(field) // 2], field[len(field) // 2:]))
    print(pairing)
    print(random())


def main(argv=None):
    """Parse CLI input and begin pairing"""

    if argv is None:
        argv = sys.argv[1:]

    parser = ArgumentParser(
        description="Swiss-style Pairings for Chess Tournaments")
    parser.add_argument(
        "field", help="CSV filename containing tournament participants")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG)

    pair_field(args.field)

    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

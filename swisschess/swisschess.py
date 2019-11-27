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
from random import sample
import sys


def assign_colors(pairing):
    """Assign colors to each pair of players

    28J. Flip a coin to select who will play White on the first board. Then,
        colors alternate down the pairing list between higher and lower-seeded
        players in each pair"""

    top_player_plays_white = random() < 0.5
    flip_index = 0 if top_player_plays_white else 1
    logging.info(
        "Top-rated player is {}playing white".format(
            "" if top_player_plays_white else "not "))

    for i, pair in enumerate(pairing):
        if i % 2 == flip_index:
            a, b = pair
            this_pair = b, a
        else:
            this_pair = pair

        logging.info((
            f"Pair: {this_pair[0]} plays White against {this_pair[1]} playing"
            " Black"))
        yield this_pair


def pair_field(filename):
    """Pair the participants in the CSV pointed to by filename

    For now, we're assuming the field hasn't been properly ranked, and that no
    player yet has ratings, so we'll randomize their order upon read. However,
    from this point on, we'll assume each player's pairing number has been
    assigned according to rank."""

    with open(filename) as f:
        field = list(map(tuple, csv_reader(f)))
    random_field = sample(field, len(field))
    logging.info(f"Shuffled field: {random_field}")

    min_rounds = ceil(log(len(random_field), 2))
    logging.info((
        f"Read {len(random_field)} participants from {filename}. Will run at "
        f"least {min_rounds} rounds"))

    first_half = random_field[:len(random_field) // 2]
    second_half = random_field[len(random_field) // 2:]
    pairing = list(zip(first_half, second_half))

    if len(random_field) % 2 != 0:
        # In an odd-sized field, the last player got left out
        left_out = random_field[-1]
        logging.info(f"Initial pairing: {pairing} with {left_out} left out")
    else:
        logging.info(f"Initial pairing: {pairing}")

    return list(assign_colors(pairing))


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

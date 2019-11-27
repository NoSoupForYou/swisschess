from os.path import dirname
from os.path import join
from unittest.mock import call
from unittest.mock import patch

from swisschess.swisschess import main
from swisschess.swisschess import pair_field


TEST_DATA = "./data/test_field.csv"


@patch("swisschess.swisschess.pair_field")
def test_main(mock_pair):
    """Runs pair_field with the first arg as a filename"""

    main(["arg"])
    mock_pair.assert_called_once_with("arg")


@patch("swisschess.swisschess.random", lambda: 0.1)
@patch("swisschess.swisschess.sample", lambda list_, _: list_)
@patch("swisschess.swisschess.logging")
def test_pairing(mock_logging):
    """Tests pairing, mocking the RNG"""

    data_file = join(dirname(__file__), TEST_DATA)
    assert pair_field(data_file) == [
        (('d', '4'), ('a', '1')),
        (('b', '2'), ('e', '5')),
        (('f', '6'), ('c', '3'))
    ]
    assert mock_logging.info.call_args_list == [
        call((
            "Shuffled field: [('a', '1'), ('b', '2'), ('c', '3'), ('d', '4'), "
            "('e', '5'), ('f', '6'), ('g', '7')]")),
        call((
            "Read 7 participants from /home/los/code/swisschess/tests/./data/t"
            "est_field.csv. Will run at least 3 rounds")),
        call((
            "Initial pairing: [(('a', '1'), ('d', '4')), (('b', '2'), ('e', '5"
            "')), (('c', '3'), ('f', '6'))] with ('g', '7') left out")),
        call('Top-rated player is playing white'),
        call("Pair: ('d', '4') plays White against ('a', '1') playing Black"),
        call("Pair: ('b', '2') plays White against ('e', '5') playing Black"),
        call("Pair: ('f', '6') plays White against ('c', '3') playing Black")
    ]

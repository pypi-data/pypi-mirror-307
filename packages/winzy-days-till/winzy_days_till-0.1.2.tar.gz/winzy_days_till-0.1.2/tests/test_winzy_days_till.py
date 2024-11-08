import winzy_days_till as w
import pytest
from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_known_args(["2022-01-01", "--say", "hello"])[0]
    assert result.say == "hello"
    assert result.datetext == ["2022-01-01"]


def test_plugin(capsys):
    w.days_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out

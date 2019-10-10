import pytest
import exgrex.cli as cli


def test_parse_raises_key_error_when_key_not_exist():
    with pytest.raises(KeyError):
        cli.parse('partId')


def test_parse_return_params():
    pass


def test_load_executor_module():
    pass

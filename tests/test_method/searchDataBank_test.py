from unittest.mock import *

import pytest

import bot
import classes


@pytest.fixture
def mock_bank():
    with patch(
        "bot.bancoDdados", {"1": {"name": "Alice"}, "2": {"name": "Bob"}}
    ), patch("bot.userData", {"3": {"name": "Charlie"}, "4": {"name": "Diana"}}):
        yield


def teste_searchDataBankIfUserNotInBank(mock_bank):
    result = bot.searchDataBank("5")
    assert result is False


def teste_searchDataBankIfUserInBank(mock_bank):
    result = bot.searchDataBank("1")
    assert result == {"name": "Alice"}


def teste_searchDataBankIfUserInUserData(mock_bank):
    result = bot.searchDataBank("3")
    assert result == {"name": "Charlie"}

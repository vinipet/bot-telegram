from unittest.mock import *

import pytest

import bot
import classes


@pytest.fixture
def mockBank():
    with patch(
        "bot.bancoDdados", {"1": classes.Usertest(), "2": {"name": "Bob"}}
    ), patch(
        "bot.userData",
        {
            "3": {"name": "Charlie"},
            "4": classes.Usertest(),
            "5": classes.User(123, infos="1"),
            "6": classes.User(9090, ["quero boquete parafuso", "name", "email"]),
        },
    ):
        yield bot

@pytest.fixture
def mock_bot(mocker):
    mock_send_message = mocker.patch("bot.bot.send_message")
    return mock_send_message


@pytest.fixture
def mock_message():
    mock_message = MagicMock()
    mock_message.chat.id = 12345
    return mock_message

def test_try_to_register_user (mockBank,mock_message):
   chatId = mock_message.chat.id
   infos = ["email", "firstName", "lastName", "identification"]
   bot.startCatchUserData(chatId, infos)

   assert bot.userData[chatId]
   assert bot.userData[chatId].steps == infos

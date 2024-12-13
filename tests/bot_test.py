import pytest
import bot
import classes
from unittest.mock import *


@pytest.fixture
def mock_bot(mocker):
    mock_bot_instance = MagicMock()
    mocker.patch("bot.bot.reply_to", mock_bot_instance.reply_to)
    return mock_bot_instance


@pytest.fixture
def mock_message():
    class MockMessage:
        chat = type("Chat", (), {"id": 12345})
        message_id = 67890
        text = "Olá, este é um teste!"

    return MockMessage()


def test_bot_initialization():
    assert callable(bot.start_bot)

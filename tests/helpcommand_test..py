import pytest
from unittest.mock import MagicMock, patch
from telebot import types
import bot

@pytest.fixture
def mock_message():
    mock_message = MagicMock()
    mock_message.chat.id = 12345
    return mock_message

@pytest.fixture
def mock_bot(mocker):
    mock_reply_to = mocker.patch("bot.bot.reply_to")
    mock_send_message = mocker.patch("bot.bot.send_message")
    mock_get_my_commands = mocker.patch("bot.bot.get_my_commands", return_value=[
        types.BotCommand("start", "Inicia o bot"),
        types.BotCommand("help", "Mostra os comandos disponíveis")
    ])
    return {
        "reply_to": mock_reply_to,
        "send_message": mock_send_message,
        "get_my_commands": mock_get_my_commands
    }

def test_help_command(mock_message, mock_bot):
    bot.helpcommand(mock_message)

    mock_bot["reply_to"].assert_called_once_with(mock_message, "Aqui está tudo o que você pode fazer comigo!")

    mock_bot["get_my_commands"].assert_called_once()

    expected_calls = [
        ((mock_message.chat.id, "/start -   Inicia o bot "),),
        ((mock_message.chat.id, "/help -   Mostra os comandos disponíveis"),),
        ((mock_message.chat.id, "Para executar qualquer comando, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃"),)
    ]
    mock_bot["send_message"].assert_has_calls(expected_calls, any_order=False)

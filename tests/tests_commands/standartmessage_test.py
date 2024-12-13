from unittest.mock import MagicMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot():
    with patch("bot.bot") as mock_bot_instance:
        yield mock_bot_instance


@pytest.fixture
def mock_verify():
    with patch("bot.verify") as mock_verify_func:
        yield mock_verify_func


def test_StandartMensage(mock_bot, mock_verify):
    mock_verify.return_value = True
    mock_msg = MagicMock()
    mock_msg.chat.id = 12345
    mock_msg.from_user.id = 67890
    mock_msg.from_user.first_name = "TestUser"
    mock_bot.get_my_commands.return_value = [
        MagicMock(
            command="help", description="Veja uma lista completa dos meus comandos"
        ),
        MagicMock(command="start", description="Comece pelo início :)"),
    ]
    bot.StandartMensage(mock_msg)
    mock_bot.send_message.assert_called_with(
        12345,
        "Não entendi oque você quis dizer, aqui estão alguns comandos que podem te ajudar \n \n 📄 /help - Veja uma lista completa dos meus comandos \n 🚀 /start - comece pelo inicio :) ",
    )
    with patch("builtins.print") as mock_print:
        bot.StandartMensage(mock_msg)
        mock_print.assert_any_call("id de usuario >>>", 67890)
        mock_print.assert_any_call("nome de usuario >>>>", "TestUser")

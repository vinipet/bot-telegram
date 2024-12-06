import pytest
from unittest.mock import MagicMock, patch, call
import bot

@pytest.fixture
def mock_bot():
    with patch("bot.bot") as mock_bot_instance:
        yield mock_bot_instance

def test_helpcommand(mock_bot):
    mock_msg = MagicMock()
    mock_msg.chat.id = 12345  # ID fictício do chat

    commands = [
        MagicMock(command="start", description="Inicia o bot"),
        MagicMock(command="help", description="Mostra ajuda"),
        MagicMock(command="settings", description="Configurações do bot"),
    ]
    mock_bot.get_my_commands.return_value = commands
    bot.helpcommand(mock_msg)
    mock_bot.reply_to.assert_called_once_with(mock_msg, 'Aqui está tudo o que você pode fazer comigo!')
    expected_calls = [
        call(mock_msg.chat.id, '/start -   Inicia o bot'),
        call(mock_msg.chat.id, '/help -   Mostra ajuda'),
        call(mock_msg.chat.id, '/settings -   Configurações do bot'),
        call(
            mock_msg.chat.id,
            'Para executar qualquer comando, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃'
        )
    ]
    mock_bot.send_message.assert_has_calls(expected_calls, any_order=False)
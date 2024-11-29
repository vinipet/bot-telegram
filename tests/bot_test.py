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
        chat = type('Chat', (), {'id': 12345})
        message_id = 67890
        text = "Olá, este é um teste!"
    return MockMessage()


def test_bot_initialization():
    assert (callable(bot.start_bot))

def test_start_command(mock_bot, mock_message):
    bot.startCommand(mock_message)
    mock_bot.reply_to.assert_called_once_with(
        mock_message,
        'Olá! 👋 Bem-vindo! \n \n  Estou aqui para ajudar você a entrar no canal privado [sla que nome c vai dar pedro]. Aqui estão algumas coisas que você pode fazer comigo: \n \n 📄 /help - Veja uma lista completa dos meus comandos \n ℹ️ /info - Saiba mais sobre o que eu posso fazer \n 🆘 /support - Fale com o suporte para mais ajuda \n \n Se precisar de algo específico, é só digitar o comando ou enviar uma mensagem. Vamos começar! 🚀'
    )

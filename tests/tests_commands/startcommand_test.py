import pytest
from unittest.mock import MagicMock
import bot


@pytest.fixture
def mock_message():
    mock_message = MagicMock()
    mock_message.chat.id = 12345
    return mock_message


@pytest.fixture
def mock_reply_to(mocker):
    return mocker.patch("bot.bot.reply_to")


def test_start_command(mock_message, mock_reply_to):
    bot.startCommand(mock_message)

    expected_text = (
        "Olá! 👋 Bem-vindo! \n \n  Estou aqui para ajudar você a entrar no canal privado [sla que nome c vai dar pedro]. "
        "Aqui estão algumas coisas que você pode fazer comigo: \n \n "
        "📄 /help - Veja uma lista completa dos meus comandos \n ℹ️ /info - Saiba mais sobre o que eu posso fazer \n "
        "🆘 /support - Fale com o suporte para mais ajuda \n \n "
        "Se precisar de algo específico, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃 Vamos começar! 🚀"
    )

    mock_reply_to.assert_called_once_with(mock_message, expected_text)

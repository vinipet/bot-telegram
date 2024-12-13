import pytest
from unittest.mock import MagicMock, patch, call
import bot


@pytest.fixture
def mock_bot():
    with patch("bot.bot") as mock_bot_instance:
        mock_bot_instance.get_my_commands.return_value = []
        yield mock_bot_instance


def test_infosCommand(mock_bot):
    mock_msg = MagicMock()
    mock_msg.chat.id = 12345
    mock_msg.json = {"from": {"id": 12345, "first_name": "TestUser"}}
    bot.infosCommand(mock_msg)
    mock_bot.reply_to.assert_called_once_with(mock_msg, "ℹ️ Sobre o Adm (ele é top):")
    expected_calls = [
        call(
            mock_msg.chat.id,
            "Eu sou um bot criado para te ajudar a entrar no canal privado da Prototips. Fui desenvolvido para oferecer a você uma experiência simples, rápida e eficiente.",
        ),
        call(
            mock_msg.chat.id,
            "Principais funções: \n \n # ADM - Eu administro o canal \n # Pagamentos - posso te ajudar a pagar (tem descontos as vezes) \n # [3 funções fica mais bonito falta 1] - [descrição da função] \n \n # Estou sempre por aqui! Se precisar de algo específico, use /help para ver todos os comandos. Vamos trabalhar juntos! 🤝",
        ),
    ]
    mock_bot.send_message.assert_has_calls(expected_calls, any_order=False)

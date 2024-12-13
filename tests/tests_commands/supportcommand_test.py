from unittest.mock import MagicMock, call, patch

import pytest

import bot


@pytest.fixture
def mock_bot():
    with patch("bot.bot") as mock_bot_instance:
        yield mock_bot_instance


def test_supportCommand(mock_bot):
    mock_msg = MagicMock()
    mock_msg.chat.id = 12345  # ID fictício do chat
    bot.supportCommand(mock_msg)
    mock_bot.reply_to.assert_called_once_with(
        mock_msg,
        "Estamos aqui para ajudar você com qualquer dúvida ou problema! Para entrar em contato:",
    )
    expected_call = call(
        mock_msg.chat.id,
        "Email: suporte100%real@todosEles.com \n "
        "FAQ: Consulte nossas Perguntas Frequentes em (link para o site que vai ter) \n "
        "Chat: (Link para um canal de suporte, se houver, ou pro seu chat) \n "
        "Fique à vontade para nos contatar, e faremos o possível para ajudar! 😄",
    )
    mock_bot.send_message.assert_has_calls([expected_call])

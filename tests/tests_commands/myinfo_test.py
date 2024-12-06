import pytest
from unittest.mock import MagicMock, patch
import bot

@pytest.fixture
def mock_bot():
    with patch("bot.bot") as mock_bot_instance:
        yield mock_bot_instance

def test_myinfosCommand(mock_bot):
    mock_msg = MagicMock()
    mock_msg.json = {
        'from': {
            'id': 12345,
            'first_name': 'TestUser'
        }
    }
    bot.myinfosCommand(mock_msg)
    mock_bot.reply_to.assert_called_once_with(
        mock_msg,
        "claro, aqui estão algumas info suas \n seu id 12345 \n seu primeiro nome TestUser \n"
    )
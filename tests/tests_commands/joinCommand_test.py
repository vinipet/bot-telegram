import pytest
from unittest.mock import MagicMock
from telebot import types
import bot

@pytest.fixture
def mock_bot(mocker):
    mock_send_message = mocker.patch("bot.bot.send_message")
    return mock_send_message

@pytest.fixture
def mock_message():
    mock_message = MagicMock()
    mock_message.chat.id = 12345
    return mock_message

def test_join_command(mock_bot, mock_message):
    bot.joinCommand(mock_message)

    expected_text = 'Pra entrar no nosso canal, primeiro deve ser pago uma pequena taxa, você esta bem com isso também?'

    expected_markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Sim", callback_data="startPayment")
    btn2 = types.InlineKeyboardButton("Não", callback_data="no")
    expected_markup.add(btn1, btn2)

    mock_bot.assert_called_once()
    actual_chat_id, actual_text = mock_bot.call_args[0]
    actual_markup = mock_bot.call_args[1]["reply_markup"]

    assert actual_chat_id == mock_message.chat.id
    assert actual_text == expected_text

    for actual_row, expected_row in zip(actual_markup.keyboard, expected_markup.keyboard):
        assert len(actual_row) == len(expected_row)  
        for actual_btn, expected_btn in zip(actual_row, expected_row):
            assert actual_btn.text == expected_btn.text  
            assert actual_btn.callback_data == expected_btn.callback_data 

def test_join_command_keyboard_size(mock_bot, mock_message):
    bot.joinCommand(mock_message)

    _, kwargs = mock_bot.call_args
    keyboard = kwargs["reply_markup"]

    assert len(keyboard.keyboard) == 1
    assert len(keyboard.keyboard[0]) == 2


from unittest.mock import MagicMock, patch

import pytest
from telebot import types

import bot


@pytest.fixture
def mock_call():
    call = MagicMock()
    call.data = "no"
    call.message.chat.id = 12345
    call.message.message_id = 67890
    call.message.text = "Mensagem original"
    call.message.reply_markup = types.InlineKeyboardMarkup()
    return call


@pytest.fixture
def mock_bot(mocker):
    mock_edit_message = mocker.patch("bot.bot.edit_message_text")
    mock_send_message = mocker.patch("bot.bot.send_message")
    mock_answer_callback = mocker.patch("bot.bot.answer_callback_query")
    return {
        "edit_message_text": mock_edit_message,
        "send_message": mock_send_message,
        "answer_callback_query": mock_answer_callback,
    }


@pytest.fixture
def mock_nullify_btn(mocker):
    return mocker.patch("bot.nullifyBtn", return_value=types.InlineKeyboardMarkup())


def test_callback_no_query(mock_call, mock_bot, mock_nullify_btn):
    bot.callback_no_query(mock_call)

    mock_bot["edit_message_text"].assert_called_once_with(
        "Mensagem original", 12345, 67890, reply_markup=mock_nullify_btn.return_value
    )
    mock_bot["send_message"].assert_called_once_with(
        12345,
        "Que pena que você não quer continuar conosco :( \n se mudar de ideia estou aqui por você.",
    )
    mock_bot["answer_callback_query"].assert_called_once_with(mock_call.id)
    mock_nullify_btn.assert_called_once_with(mock_call.message.reply_markup.keyboard)


def test_callback_no_query_missing_attributes(mock_call, mock_bot):
    del mock_call.message.chat.id
    with pytest.raises(AttributeError):
        bot.callback_no_query(mock_call)

import pytest
from unittest.mock import MagicMock, patch
from telebot import types
import bot


@pytest.fixture
def mock_call():
    call = MagicMock()
    call.data = "startPayment"
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


def test_callback_startPayment_query(mock_call, mock_bot, mock_nullify_btn):
    bot.callback_startPayment_query(mock_call)

    mock_bot["edit_message_text"].assert_called_once_with(
        "Mensagem original",  # Texto original
        12345,  # ID do chat
        67890,  # ID da mensagem
        reply_markup=mock_nullify_btn.return_value,  # Teclado nullificado
    )
    mock_bot["send_message"].assert_called_once()
    _, kwargs = mock_bot["send_message"].call_args
    assert kwargs["reply_markup"]  # Teclado deve estar presente
    keyboard = kwargs["reply_markup"].keyboard
    assert len(keyboard) == 3  # Três botões no teclado
    assert keyboard[0][0].text == "🔥 Pix 🔥"
    assert keyboard[0][0].callback_data == "pix"
    assert keyboard[1][0].text == "💳 Cartão 💳"
    assert keyboard[1][0].callback_data == "cartão"
    assert keyboard[2][0].text == "📃 Boleto 📃"
    assert keyboard[2][0].callback_data == "boleto"

    mock_bot["answer_callback_query"].assert_called_once_with(mock_call.id)

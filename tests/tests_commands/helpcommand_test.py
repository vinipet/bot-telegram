# import pytest
# from unittest.mock import MagicMock, patch
# from telebot import types
# import bot

# @pytest.fixture
# def mock_message():
#     mock_message = MagicMock()
#     mock_message.chat.id = 12345
#     return mock_message

# @pytest.fixture
# def mock_botTwo():
#     with patch("bot.bot") as mock_bot_instance:
#         yield mock_bot_instance

# @pytest.fixture
# def mock_bot():
#     with patch("bot.bot") as mock_bot_instance:
#         yield mock_bot_instance

# @pytest.fixture
# def mock_bot(mocker):
#     mock_reply_to = mocker.patch("bot.bot.reply_to")
#     mock_send_message = mocker.patch("bot.bot.send_message")
#     mock_get_my_commands = mocker.patch("bot.bot.get_my_commands", return_value=[
#         types.BotCommand("start", "Inicia o bot"),
#         types.BotCommand("help", "Mostra os comandos disponíveis")
#     ])
#     return {
#         "reply_to": mock_reply_to,
#         "send_message": mock_send_message,
#         "get_my_commands": mock_get_my_commands
#     }

# def test_help_command(mock_message, mock_bot):
#     bot.helpcommand(mock_message)

#     mock_bot["reply_to"].assert_called_once_with(mock_message, "Aqui está tudo o que você pode fazer comigo!")

#     mock_bot["get_my_commands"].assert_called_once()

#     expected_calls = [
#         ((mock_message.chat.id, "/start -   Inicia o bot "), {"reply_markup": None}),  
#         ((mock_message.chat.id, "/help -   Mostra os comandos disponíveis"), {"reply_markup": None}),
#         ((mock_message.chat.id, "Para executar qualquer comando, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃"), {"reply_markup": None})
#     ]
#     mock_bot["send_message"].assert_has_calls(expected_calls, any_order=False)

# def test_help_command_no_commands(mock_message, mock_bot):
#     # Mocka get_my_commands para retornar uma lista vazia
#     mock_bot["get_my_commands"].return_value = []

#     bot.helpcommand(mock_message)

#     # Verifica que apenas a mensagem inicial e final foram enviadas
#     expected_calls = [
#         ((mock_message.chat.id, "Aqui está tudo o que você pode fazer comigo!"), {}),
#         ((mock_message.chat.id, "Para executar qualquer comando, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃"), {})
#     ]
#     mock_bot["send_message"].assert_has_calls(expected_calls, any_order=False)

# def test_help_command_args(mock_message, mock_bot):
#     bot.helpcommand(mock_message)
#     print(mock_bot["send_message"].call_args_list) 
    
#     assert mock_bot["send_message"].call_count > 0, "send_message não foi chamado!"

# def test_help_command_print(mock_message, mock_bot):
#     bot.helpcommand(mock_message)

#     calls = mock_bot["send_message"].call_args_list
#     assert calls, f"Depuração: {calls}"



# def test_helpcommand(mock_botTwo):
#     mock_message = MagicMock()
#     mock_message.chat.id = 12345

#     mock_botTwo.get_my_commands.return_value = [
#         MagicMock(command="start", description="Iniciar o bot"),
#         MagicMock(command="help", description="Obter ajuda"),
#     ]

#     bot.helpcommand(mock_message)

#     mock_botTwo.reply_to.assert_called_once_with(mock_message, 'Aqui está tudo o que você pode fazer comigo!')

#     mock_botTwo.send_message.assert_any_call(12345, '/start -   Iniciar o bot ')
#     mock_botTwo.send_message.assert_any_call(12345, '/help -   Obter ajuda')
#     mock_botTwo.send_message.assert_any_call(12345, 'Para executar qualquer comando, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃')

#     assert mock_botTwo.send_message.call_count == 3

#  # Substitua pelo caminho correto para importar seu método



# def test_helpcommandd(mock_botTwo):
#     mock_message = MagicMock()
#     mock_message.chat.id = 12345

#     mock_botTwo.get_my_commands.return_value = [
#         MagicMock(command="start", description="Iniciar o bot"),
#         MagicMock(command="help", description="Obter ajuda"),
#         MagicMock(command="help", description="Obter ajuda"),
#     ]

#     bot.helpcommand(mock_message)

#     mock_botTwo.reply_to.assert_called_once_with(mock_message, 'Aqui está tudo o que você pode fazer comigo!')
#     mock_botTwo.send_message.assert_any_call(12345, '/start -   Iniciar o bot ')
#     mock_botTwo.send_message.assert_any_call(12345, '/help -   Obter ajuda')
#     mock_botTwo.send_message.assert_any_call(12345, 'Para executar qualquer comando, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃')
#     assert mock_botTwo.send_message.call_count == 3

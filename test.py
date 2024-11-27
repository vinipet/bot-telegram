import unittest
import bot
from bot import start_bot
from unittest.mock import *
from bot import  startCommand
import classes

class TestBot(unittest.TestCase):
   def test_bot_initialization(self):
      self.assertTrue(callable(start_bot))

   def test_start_command(self):
         mock_message = MagicMock()
         mock_message.chat.id = 12345
         bot.bot.reply_to = MagicMock()
         bot.startCommand(mock_message)
         bot.bot.reply_to.assert_called_once_with(mock_message, 'Olá! 👋 Bem-vindo! \n \n  Estou aqui para ajudar você a entrar no canal privado [sla que nome c vai dar pedro]. Aqui estão algumas coisas que você pode fazer comigo: \n \n 📄 /help - Veja uma lista completa dos meus comandos \n ℹ️ /info - Saiba mais sobre o que eu posso fazer \n 🆘 /support - Fale com o suporte para mais ajuda \n \n Se precisar de algo específico, é só digitar o comando ou enviar uma mensagem. Vamos começar! 🚀')
   

@patch("bot.bancoDdados" , {"1": {"name": "Alice"}, "2": {"name": "Bob"}})
@patch("bot.userData", {"3": {"name": "Charlie"}, "4": {"name": "Diana"}})
class testsearchDataBank(unittest.TestCase):
      
   def teste_searchDataBankIfUserNotInBank(self):
      result = bot.searchDataBank("5")  # ID não está em nenhum dicionário
      self.assertFalse(result)

   def teste_searchDataBankIfUserInBank(self):
      result = bot.searchDataBank("1")  # ID não está em nenhum dicionário
      self.assertEqual(result, {"name": "Alice"})

   def teste_searchDataBankIfUserInUserData(self):
      result = bot.searchDataBank("3")  # ID não está em nenhum dicionário
      self.assertEqual(result, {"name": "Charlie"})

class testSearchUserInfoWhoIsNone(unittest.TestCase):
    def test_user_as_dict_all_values_present(self):
        user = {
            "email": "user@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "identification": "123456789"
        }
        result = bot.SearchUserInfoWhoIsNone(user)
        self.assertEqual(result, [])  # nothing are missing

    def test_user_as_dict_some_values_missing(self):
        user = {
            "email": "user@example.com",
            "firstName": "John"
        }
        result = bot.SearchUserInfoWhoIsNone(user)
        self.assertEqual(result, ["lastName", "identification"])  # value missing

    def test_user_as_dict_all_values_missing(self):
        user = {}
        result = bot.SearchUserInfoWhoIsNone(user)
        self.assertEqual(result, ['email', 'firstName', 'lastName', 'identification'])  # value missing

    def test_user_as_object_all_values_present(self):
      class User:
         email = "user@example.com"
         firstName = "John"
         lastName = "Doe"
         identification = "123456789"

      user = User()
      result = bot.SearchUserInfoWhoIsNone(user)
      self.assertEqual(result, [])  # nothing are missing

    def test_user_as_object_some_values_missing(self):
      class User:
         email = "user@example.com"
         lastName = "Doe"

      user = User()
      result = bot.SearchUserInfoWhoIsNone(user)
      self.assertEqual(result, ["firstName", "identification"])  # missing value

    def test_user_as_object_all_values_missing(self):
      class User:
         email = None
         firstName = None
         lastName = None
         identification = None

      user = User()
      result = bot.SearchUserInfoWhoIsNone(user)
      self.assertEqual(result, ['email', 'firstName', 'lastName', 'identification'])  # missing value

    def test_user_with_empty_searching_info(self):
      user = {
         "email": "user@example.com",
         "firstName": "John"
      }
      result = bot.SearchUserInfoWhoIsNone(user, [])
      self.assertEqual(result, [])  # nothing information to verify

    def test_user_as_dict_no_matching_values(self):
        user = {}
        result = bot.SearchUserInfoWhoIsNone(user)
        self.assertEqual(result, ["email", "firstName", "lastName", "identification"])  # all are missing

    def test_user_as_obj_with_not_atribute(self):
      class user():
         id = self
      user = user()
      result = bot.SearchUserInfoWhoIsNone(user)
      self.assertEqual(result, ["email", "firstName", "lastName", "identification"])  # all are missing

    def test_user_as_obj_search_random_value(self):
      class User:
         def __init__(self):
            self.email = None
            self.firstName = None
            self.lastName = None
            self.identification = None
      user = User()
      result = bot.SearchUserInfoWhoIsNone(user, ['cu', 'bct', 'penisGordo'])
      self.assertEqual(result, ['cu', 'bct', 'penisGordo'])  # all are missing

    def test_user_is_none(self):
        with self.assertRaises(TypeError):
            bot.SearchUserInfoWhoIsNone(None)

    def test_user_is_string(self):
        with self.assertRaises(TypeError):
            bot.SearchUserInfoWhoIsNone("invalid_string")

    def test_user_is_list(self):
        with self.assertRaises(TypeError):
           bot.SearchUserInfoWhoIsNone(["invalid", "list"])

    def test_user_is_number(self):
        with self.assertRaises(TypeError):
           bot.SearchUserInfoWhoIsNone(123)

class TestNullifyBtn(unittest.TestCase):
    def test_nullify_btn(self):
        btns = [
            [
                bot.types.InlineKeyboardButton("Button 1", callback_data="data1"),
                bot.types.InlineKeyboardButton("Button 2", callback_data="data2"),
            ],
            [
                bot.types.InlineKeyboardButton("Button 3", callback_data="data3"),
            ]
        ]
        result = bot.nullifyBtn(btns)
        self.assertIsInstance(result, bot.types.InlineKeyboardMarkup)
        rows = result.keyboard  
        self.assertEqual(len(rows), len(btns)) 

        for row_result, row_expected in zip(rows, btns):
            self.assertEqual(len(row_result), len(row_expected))  
            for btn_result, btn_expected in zip(row_result, row_expected):
                self.assertEqual(btn_result.text, btn_expected.text) 
                self.assertEqual(btn_result.callback_data, "None")  

class testAddCommand(unittest.TestCase):
   class TestBotCommands(unittest.TestCase):
    def setUp(self):
        # Cria um bot simulado
        self.bot = MagicMock(spec=TeleBot)

    def test_add_command(self):
        mock_commands = [types.BotCommand("start", "Iniciar o bot")]
        self.bot.get_my_commands.return_value = mock_commands  # Simula get_my_commands
        bot.add_command(self.bot, "help", "Mostrar ajuda")
        args, _ = self.bot.set_my_commands.call_args
        actual_commands = args[0]  # Argumento passado para set_my_commands
        expected_commands = [
            bot.types.BotCommand("start", "Iniciar o bot"),
            bot.types.BotCommand("help", "Mostrar ajuda"),
        ]
        self.assertEqual(len(actual_commands), len(expected_commands))
        for actual, expected in zip(actual_commands, expected_commands):
            self.assertEqual(actual.command, expected.command)
            self.assertEqual(actual.description, expected.description)


class joinCommand(unittest.TestCase):
    True

if __name__ == "__main__":
   unittest.main()
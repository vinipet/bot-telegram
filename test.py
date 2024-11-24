import unittest
import bot
from bot import start_bot
from unittest.mock import *
from bot import  startCommand


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


if __name__ == "__main__":
   unittest.main()

















# class testeBotMethod(unittest.TestCase):
#    def test_user_in_bancoDdados(self):
#       result = start_bot.searchDataBank(1)
#       self.assertEqual(result, bancoDdados[1]) 
#    def test_user_in_userData(self):
#       result = start_bot.searchDataBank(3)
#       self.assertEqual(result, userData[3]) 

#    def test_user_not_found(self):
#       result = start_bot.searchDataBank(99)
#       self.assertFalse(result) 

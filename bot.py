import telebot
Chave_api = "7352283955:AAE2KNW-GlifnPKwy82F0iytRP2uDFPlJSA"

bot = telebot.TeleBot(Chave_api)
def verify(msg):
   return True
@bot.message_handler(func=verify)
def StandartMensage(msg):
   bot.reply_to(msg, "Mensagem padrão!")

bot.polling()
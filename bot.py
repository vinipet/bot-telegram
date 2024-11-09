import telebot 
from telebot import TeleBot, types
import json

Chave_api = "7352283955:AAE2KNW-GlifnPKwy82F0iytRP2uDFPlJSA"
bot = telebot.TeleBot(Chave_api)

bot.delete_my_commands()


def add_command(commandName, commandDescription):
    currentCommands = bot.get_my_commands()
    newCommand = types.BotCommand(commandName, commandDescription)
    currentCommands.append(newCommand)
    bot.set_my_commands(currentCommands)

# @bot.message_handler(func = lambda msg: msg.text == 'me add')

add_command('start', ' 🚀 inicia o bot')
@bot.message_handler(commands=['start'])
def startCommand(msg):
   bot.reply_to(msg, " Olá! 👋 Bem-vindo! \n \n  Estou aqui para ajudar você a entrar no canal privado [sla que nome c vai dar pedro]. Aqui estão algumas coisas que você pode fazer comigo: \n \n 📄 /help - Veja uma lista completa dos meus comandos \n ℹ️ /info - Saiba mais sobre o que eu posso fazer \n 🆘 /support - Fale com o suporte para mais ajuda \n \n Se precisar de algo específico, é só digitar o comando ou enviar uma mensagem. Vamos começar! 🚀")

add_command('help', ' 🔍 Exibe lista completa de Comandos')
@bot.message_handler(commands=['help'])
def helpcommand(msg):
   bot.reply_to(msg, 'Aqui está tudo o que você pode fazer comigo!')
   for command in bot.get_my_commands():
      bot.send_message(msg.chat.id, '/{} -   {} '.format(command.command ,command.description))
   bot.send_message(msg.chat.id, 'Para executar qualquer um, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃') 

add_command('myinfo',' 📄 exibe as informações do usuario')
@bot.message_handler(commands=['myinfo'])
def infosCommand(msg):
   bot.reply_to(msg, "claro, aqui estão algumas info suas \n seu id {} \n seu primeiro nome {} \n".format(msg.json['from']['id'], msg.json['from']['first_name']))

add_command('logs', '\U0001FAB5 exibe alguns logs da programação')
@bot.message_handler(commands=['logs'])
def sendLogsCommand(msg):
   bot.reply_to(msg, ('os dados da msg são >>>>>>>> ' + json.dumps(msg.json, indent=4)))
   bot.send_message(msg.chat.id, 'o tipo da msg tratado pelo jasonpickle é  >>>>>>>> {} '.format(type( json.dumps(msg.json, indent=4))))
   bot.send_message(msg.chat.id, 'o tipo da msg não tratada é   >>>>>>>> {}'.format(type(msg)))

def verify(msg):
   print('A mensagem recebida é  >>>>> ',  msg.text)
   return True
@bot.message_handler(func=verify)
def StandartMensage(msg):
   commands = bot.get_my_commands()
   bot.send_message(msg.chat.id, 'Não entendi oque você quis dizer, aqui estão alguns comandos que podem te ajudar \n \n 📄 /help - Veja uma lista completa dos meus comandos \n 🚀 /start - comece pelo inicio :) ' )
   print('id de usuario >>>', msg.from_user.id)
   print('nome de usuario >>>>', msg.from_user.first_name)

bot.infinity_polling()
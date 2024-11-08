import telebot 
from telebot import TeleBot, types
import json

Chave_api = "7352283955:AAE2KNW-GlifnPKwy82F0iytRP2uDFPlJSA"
bot = telebot.TeleBot(Chave_api)

# start help info
bot.delete_my_commands()

def add_command(commandName, commandDescription):
    currentCommands = bot.get_my_commands()
    newCommand = types.BotCommand(commandName, commandDescription)
    currentCommands.append(newCommand)
    bot.set_my_commands(currentCommands)

add_command('myinfo','exibe as informações do usuario')
@bot.message_handler(commands=['myinfo'])
def infosCommand(msg):
   bot.reply_to(msg, "claro, aqui estão algumas info suas \n seu id {} \n seu primeiro nome {} \n".format(msg.json['from']['id'], msg.json['from']['first_name']))

add_command('logs', 'exibe alguns logs da programação')
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
   bot.reply_to(msg, "Recebi sua mensagem.")
   bot.send_message(msg.chat.id, 'não entendi oque voce quer, aqui estao alguns comandos que podem vir a ser uteis.' )
   for command in commands:
    bot.send_message(msg.chat.id, '/{} , {}'.format(command.command, command.description))
   print(msg.from_user.id)
   print(msg.from_user.first_name)


bot.infinity_polling()
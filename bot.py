import telebot 
from telebot import TeleBot, types
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv('API_KEY')
bot = telebot.TeleBot(API_key)


# bot.delete_my_commands()


def add_command(commandName, commandDescription):
    currentCommands = bot.get_my_commands()
    newCommand = types.BotCommand(commandName, commandDescription)
    currentCommands.append(newCommand)
    bot.set_my_commands(currentCommands)

def nullifyBtn(btns):
   newBtns = types.InlineKeyboardMarkup()
   for row in btns:
      newRow = [types.InlineKeyboardButton(btn.text, callback_data='None') for btn in row]
      newBtns.row(*newRow)
   return newBtns



# add_command('join', '🎁 iniciar o processo para entrar no canal privado')
@bot.message_handler(commands=['join'])
def joinCommand(msg):
   keyboard = types.InlineKeyboardMarkup()
   btn1 = types.InlineKeyboardButton("Sim", callback_data="sim")
   btn2 = types.InlineKeyboardButton("Não", callback_data="no")
   keyboard.add(btn1,btn2)

   bot.reply_to(msg, 'Entendido!!! então você quer começar a acompanhar o nosso super canal. Mas antes eu preciso de algumas informções suas ')
   bot.send_message(msg.chat.id, 'você esta bem com isso?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "no")
def callback_no_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    message = call.message
    bot.edit_message_text(message.text, chat_id, message_id, reply_markup=nullifyBtn(message.reply_markup.keyboard))
    bot.send_message(chat_id, 'Que pena que você não quer continuar conosco :( \n se mudar de ideia estou aqui por você   ')
    bot.answer_callback_query(call.id)
    
@bot.callback_query_handler(func=lambda call: call.data == "sim")
def callback_sim_query(call):
   chat_id = call.message.chat.id
   message_id = call.message.message_id
   message = call.message
   bot.edit_message_text(message.text, chat_id, message_id, reply_markup=nullifyBtn(message.reply_markup.keyboard))
   keyboard = types.InlineKeyboardMarkup()
   btn1 = types.InlineKeyboardButton("Sim", callback_data="startPayment")
   btn2 = types.InlineKeyboardButton("Não", callback_data="no")
   keyboard.add(btn1,btn2)
   bot.send_message(chat_id, 'Pra entrar no nosso canal, primeiro deve ser pago uma pequena taxa, você esta bem com isso também?', reply_markup=keyboard)
   bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "startPayment")
def callback_startPayment_query(call):
   chat_id = call.message.chat.id
   message_id = call.message.message_id
   message = call.message
   bot.edit_message_text(message.text, chat_id, message_id, reply_markup=nullifyBtn(message.reply_markup.keyboard))

   keyboard = types.InlineKeyboardMarkup()
   Pix = types.InlineKeyboardButton("🔥 Pix 🔥", callback_data="pix")
   card = types.InlineKeyboardButton("💳 Cartão 💳", callback_data="cartão")
   boleto = types.InlineKeyboardButton("📃 Boleto 📃" , callback_data="boleto")
   keyboard.add(Pix)
   keyboard.add(card)
   keyboard.add(boleto)

   bot.send_message(chat_id, 'Como você deseja pagar?', reply_markup=keyboard)
   bot.answer_callback_query(call.id)

# add_command('start', ' 🚀 iniciar o bot')
@bot.message_handler(commands=['start'])
def startCommand(msg):
   bot.reply_to(msg, " Olá! 👋 Bem-vindo! \n \n  Estou aqui para ajudar você a entrar no canal privado [sla que nome c vai dar pedro]. Aqui estão algumas coisas que você pode fazer comigo: \n \n 📄 /help - Veja uma lista completa dos meus comandos \n ℹ️ /info - Saiba mais sobre o que eu posso fazer \n 🆘 /support - Fale com o suporte para mais ajuda \n \n Se precisar de algo específico, é só digitar o comando ou enviar uma mensagem. Vamos começar! 🚀")

# add_command('help', ' 🔍 Exibir lista completa de Comandos')
@bot.message_handler(commands=['help'])
def helpcommand(msg):
   bot.reply_to(msg, 'Aqui está tudo o que você pode fazer comigo!')
   for command in bot.get_my_commands():
      bot.send_message(msg.chat.id, '/{} -   {} '.format(command.command ,command.description))
   bot.send_message(msg.chat.id, 'Para executar qualquer um, basta digitar o nome do comando ou clicar nele. Qualquer dúvida, estou aqui para ajudar! 😃') 

# add_command('info',' ℹ️  exibir algumas informações sobre mim')
@bot.message_handler(commands=['info'])
def infosCommand(msg):
   bot.reply_to(msg, 'ℹ️ Sobre o Adm (ele é top):')
   bot.send_message(msg.chat.id, 'Eu sou um bot criado para te ajudar a entrar no canal privado da Prototips. Fui desenvolvido para oferecer a você uma experiência simples, rápida e eficiente.')
   bot.send_message(msg.chat.id, 'Principais funções: \n \n # ADM - Eu administro o canal \n # Pagamentos - posso te ajudar a pagar (tem descontos as vezes) \n # [3 funções fica mais bonito falta 1] - [descrição da função] \n \n # Estou sempre por aqui! Se precisar de algo específico, use /help para ver todos os comandos. Vamos trabalhar juntos! 🤝')

# add_command('support', '🆘 mostrar os contatos para melhor suporte')
@bot.message_handler(commands=['support'])
def supportCommand(msg):
   bot.reply_to(msg, 'Estamos aqui para ajudar você com qualquer dúvida ou problema! Para entrar em contato:')
   bot.send_message(msg.chat.id, 'Email: suporte100%real@todosEles.com \n FAQ: Consulte nossas Perguntas Frequentes em (link para o site que vai ter) \n Chat: (Link para um canal de suporte, se houver, ou pro seu chat) \n Fique à vontade para nos contatar, e faremos o possível para ajudar! 😄')

# add_command('myinfo',' 📄 exibir as informações do usuario')
@bot.message_handler(commands=['myinfo'])
def infosCommand(msg):
   bot.reply_to(msg, "claro, aqui estão algumas info suas \n seu id {} \n seu primeiro nome {} \n".format(msg.json['from']['id'], msg.json['from']['first_name']))

# add_command('logs', '\U0001FAB5 exibir alguns logs da programação')
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

print('LIGADO!!!!!!')
bot.infinity_polling()
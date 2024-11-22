import telebot 
from telebot import TeleBot, types
import json
from dotenv import load_dotenv
import os
import classes
from typing import Optional
import fetch
import qrcode
from PIL import Image
import io

load_dotenv()
API_key = os.getenv('API_KEY')
bot = telebot.TeleBot(API_key)

bancoDdados = {}
userData = {}
# bot.delete_my_commands()

def makeQRimage(code):
   qr = qrcode.QRCode(
   version=2,  # Tamanho do QR Code (1 = menor, 40 = maior)
   error_correction=qrcode.constants.ERROR_CORRECT_L,  # Tolerância a erros
   box_size=10,  # Tamanho de cada "quadradinho"
   border=4,  # Tamanho da borda
   )
   qr.add_data(code)
   qr.make(fit=True)

   qr_image = qr.make_image(fill_color="black", back_color="white")
   buffer = io.BytesIO()
   qr_image.save(buffer, format="PNG")
   qr_bytes = buffer.getvalue()
   
   return qr_bytes
   # # Salvando a imagem em um arquivo
   # qr_image.save("qr_code.png")

   # # Exibindo a imagem (opcional, para visualização)
   # qr_image.show()

def searchDataBank(userId):
   if userId in bancoDdados:
         user_object = bancoDdados[userId]  
         return user_object
   elif userId in userData:
      user_object = userData[userId]  
      return user_object
   else:
      return False

def SearchUserInfoWhoIsNone(user = object, SearchingInfo: Optional[list] = None):
   """
   Busca informações que estão como 'None' em um usuário.

   Args:
      user: O objeto ou dicionário do usuário.
      SearchingInfo: Uma lista opcional de informações a serem verificadas.
                     Se não for fornecida, será usada a lista padrão.

   Returns:
      list: Uma lista contendo os nomes das informações que estão como 'None'.
   """
   if SearchingInfo is None:
      SearchingInfo = ['email', 'firstName', 'lastName', 'identification']
      datas = []
      for info in SearchingInfo:
         if isinstance(user, dict):
            value = user.get(info, None)  
         else:  
            value = getattr(user, info, None) 
         if value is None:
            datas.append(info)
      return datas

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

def tryRegisterUser(userId):
   if len(userData[userId].steps) == 0 :
      del userData[userId].steps
      bancoDdados[userId] = userData[userId]
      del userData[userId]
      print('banco de dados ofc >>>>', bancoDdados)
      print('banco de dados fal >>>>', userData)
      return True 
   else:
      return False   

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

@bot.callback_query_handler(func=lambda call: call.data =="pix")
def callback_pix_query(call):
   chat_id = call.message.chat.id
   message_id = call.message.message_id
   message = call.message
   
   keyboard = types.InlineKeyboardMarkup()
   keyboard.add(types.InlineKeyboardButton("🔥 Pix 🔥", callback_data="none"))
   bot.edit_message_text(message.text, chat_id, message_id, reply_markup=keyboard)

   bot.send_message(chat_id, 'estamos verificando algumas informações')   
   isInBank = searchDataBank(chat_id)
   infos = ['email', 'firstName', 'lastName', 'identification']
   print(SearchUserInfoWhoIsNone(chat_id, infos))
   if isInBank and not SearchUserInfoWhoIsNone(isInBank, infos):
      result = fetch.fetch(isInBank)
      print(result)
      if result['status'] == 'denied':
         bot.send_message(chat_id,'Algo deu errado')
         bot.send_message(chat_id, result['msg'])
      if result['status'] == 'aproved':
         bot.send_message(chat_id, 'Vejo que você já tem cadastro conosco.')
         qr = makeQRimage(result['QRCode'])
         bot.send_photo(chat_id, qr )
         bot.send_message(chat_id, result['link'])


   else:
      userData[chat_id] = classes.Usertemp(chat_id, infos) 
      bot.send_message(chat_id, 'Vejo que você ainda não possui um cadastro conosco. Vamos primeiro fazer o seu cadastro depos você volta aqui pra realizar o seu pagamento')
      bot.send_message(chat_id, 'Vamos começar com {}, por favor digite as informações pra eu terminar o seu cadastro'.format(userData[chat_id].steps[0]) )
      
@bot.message_handler(func=lambda msg:  msg.chat.id in userData and userData[msg.chat.id].steps[0] == 'email')
def captureEmail(msg):
   chat_id = msg.chat.id
   email = msg.text

   if "@" in email and "." in email:
      print('capturando e-mail')
      userData[chat_id].email = email
      bot.send_message(chat_id, f"E-mail registrado com sucesso: {email}")
      print(f"Salvando no banco de dados: {chat_id} - {email}")
      userData[chat_id].steps.remove('email')
      bot.send_message(chat_id, 'ainda falta {} pra finalizar o cadastro, por favor digite o {}'.format(userData[chat_id].steps[0],userData[chat_id].steps[0],))
   else:
      bot.send_message(chat_id, "E-mail inválido. Por favor, tente novamente.")

@bot.message_handler(func=lambda msg:msg.chat.id in userData and userData[msg.chat.id].steps[0] == 'firstName')
def captureFirstName(msg):
   chat_id = msg.chat.id
   name = msg.text

   print('capturando primeiro nome')
   userData[chat_id].firstName = name
   bot.send_message(chat_id, f"Nome registrado com sucesso: {name}")
   userData[chat_id].steps.remove('firstName')
   bot.send_message(chat_id, 'ainda falta {} pra finalizar o cadastro, por favor digite o {}'.format(userData[chat_id].steps[0],userData[chat_id].steps[0],))
   print(f"Salvando no banco de dados: {chat_id} - {name}")

@bot.message_handler(func=lambda msg:  msg.chat.id in userData and userData[msg.chat.id].steps[0] == 'lastName')
def captureFirstName(msg):
   chat_id = msg.chat.id
   lastName = msg.text

   print('capturando sobre nome')
   userData[chat_id].lastName = lastName
   bot.send_message(chat_id, f"Nome registrado com sucesso: {lastName}")
   userData[chat_id].steps.remove('lastName')
   bot.send_message(chat_id, 'ainda falta {} pra finalizar o cadastro, por favor digite o {}'.format(userData[chat_id].steps[0],userData[chat_id].steps[0],))
   print(f"Salvando no banco de dados: {chat_id} - {lastName}")

@bot.message_handler(func=lambda msg: msg.chat.id in userData and userData[msg.chat.id].steps[0] == 'identification')
def capturedocumentType(msg):
   chat_id = msg.chat.id
   cpf = msg.text

   print('capturando CPF')
   userData[chat_id].identification = cpf
   print(f"Salvando no banco de dados: {chat_id} - {cpf}")
   bot.send_message(chat_id, f"CPF registrado com sucesso: {cpf}")
   userData[chat_id].steps.remove('identification')
   if not tryRegisterUser(chat_id):
      bot.send_message(chat_id, 'ainda falta {} pra finalizar o cadastro, por favor digite o {}'.format(userData[chat_id].steps[0],userData[chat_id].steps[0],))
   else: 
      bot.send_message(chat_id,'cadastro concluido, vamos voltar ao pagamento? /join')

# add_command('start', ' 🚀 iniciar o bot')
@bot.message_handler(commands=['start'])
def startCommand(msg):
   bot.reply_to(msg, 'Olá! 👋 Bem-vindo! \n \n  Estou aqui para ajudar você a entrar no canal privado [sla que nome c vai dar pedro]. Aqui estão algumas coisas que você pode fazer comigo: \n \n 📄 /help - Veja uma lista completa dos meus comandos \n ℹ️ /info - Saiba mais sobre o que eu posso fazer \n 🆘 /support - Fale com o suporte para mais ajuda \n \n Se precisar de algo específico, é só digitar o comando ou enviar uma mensagem. Vamos começar! 🚀')

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

def start_bot():
   bot.infinity_polling()

if __name__ == "__main__":
    start_bot()


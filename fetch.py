import mercadopago
from dotenv import load_dotenv
import os
import random
import json
import bot
import classes


load_dotenv()
sdk = mercadopago.SDK(os.getenv('accessToken'))

generated_keys = set()

def generate_unique_key():
    while True:
        key = ''.join(random.choices('0123456789', k=3))
        if key not in generated_keys:
            generated_keys.add(key)
            return key


def fetch(user: classes.User):
    url = "https://api.mercadopago.com/v1/payments"
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': str(user.id)
    }

    payment_data = {
        "transaction_amount": 100,
        "description": "LOTOTIP private room",
        # "date_of_expiration" : '',
        "payment_method_id": "pix",
        "payer": {
            "email": user.email,
            "first_name": user.firstName,
            "last_name": user.lastName,
            "identification": {
                "type": "CPF",
                "number": user.identification
            },
            # "address": {
            #     "zip_code": "06233-200",
            #     "street_name": "Av. das Nações Unidas",
            #     "street_number": "3003",
            #     "neighborhood": "Bonfim",
            #     "city": "Osasco",
            #     "federal_unit": "SP"
            # }
        }
    }


    payment = sdk.payment().create(payment_data, request_options)

    if payment["status"] == 200:
        payment_response = payment["response"]  # Dados do pagamento criado
        print("Pagamento criado com sucesso!", json.dumps(payment_response, indent=4),  '\n \n \n')
        response = { 
            'QRCode' : payment_response['point_of_interaction']['transaction_data']['qr_code'] ,
            'QRCode64' : payment_response['point_of_interaction']['transaction_data']['qr_code_base64'] ,
            'link' :  payment_response['point_of_interaction']['transaction_data']['ticket_url'],
            'status' : 'aproved'
        }
        return response

    else:
        print(f"Erro ao criar pagamento: {payment['status']} -> {payment['response']}")
        response = {
            'status' : 'denied',
            'msg' : payment['response'].message  # Define um valor padrão para response em caso de erro
        }
        return response

def tryPayment(user: classes.User, userInfos : list) -> dict:
    if user and not bot.SearchUserInfoWhoIsNone(user, userInfos):
        result = fetch(user)
        return result
    #     result = fetch.fetch(isInBank)
    #     if result["status"] == "denied":
    #         bot.send_message(chat_id, "Algo deu errado")
    #         bot.send_message(chat_id, result["msg"])
    #     if result["status"] == "aproved":
    #         bot.send_message(chat_id, "Vejo que você já tem cadastro conosco.")
    #         qr = makeQRimage(result["QRCode"])
    #         bot.send_photo(chat_id, qr)
    #         bot.send_message(chat_id, result["link"])

    else:
        return {
        "status": 0,
        "response": {"msg": "o usuario não possui um cadastro completo, ou valido"},
    }


import json
import os
import random
import json
import mercadopago.sdk
import bot
import classes
import mercadopago
from dotenv import load_dotenv

load_dotenv()
sdk = mercadopago.SDK(os.getenv("accessToken"))

generated_keys = set()


def generate_unique_key():
    while True:
        key = "".join(random.choices("0123456789", k=3))
        if key not in generated_keys:
            generated_keys.add(key)
            return key

def tryPayment(user: classes.User, userInfos: list) -> dict:
    if user and not bot.SearchUserInfoWhoIsNone(user, userInfos):
      result = fetch(sdk,user,"pix")
      return result
    else:
        return {
            "status": 0,
            "response":{
                "msg" : "o usuario não possui um cadastro completo, ou valido"
            }}

def fetch(sdk: mercadopago.sdk, user: classes.User, paymentMetod):
    try:
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': str(user.id)
        }

        payment_data = {
            "transaction_amount": 1,
            "description": "LOTOTIP private room",
            "payment_method_id": paymentMetod,
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

        paymentMetodsList = ["pix"]
        if paymentMetod not in paymentMetodsList:
            raise ValueError("metodo de pagamento invalido")
        payment = sdk.payment().create(payment_data, request_options)
        if int(payment["status"]) // 100 == 2:
            payment_response = payment["response"] 
            print("Pagamento criado com sucesso!", json.dumps(payment_response, indent=4),  '\n \n \n')
            response = { 
                'QRCode' : payment_response['point_of_interaction']['transaction_data']['qr_code'] ,
                'link' :  payment_response['point_of_interaction']['transaction_data']['ticket_url'],
                'status' : 'aproved'
            }
            return response

        else:
            print(f"Erro ao criar pagamento: {payment['status']} -> {payment['response']}")
            response = {
                'status' : 'denied',
                'msg' : payment['response']["message"] 
            }
            return response
    except KeyError as e:
        print(f"Erro ao acessar a resposta do SDK: {e}")
        return {
            'status': 'denied',
            'msg': f"Invalid response structure: {e}"
        }
    except ConnectionError as e:
        print(f"Erro de conexão: {e}")
        return {
            'status': 'denied',
            'msg': "Network error occurred, please try again."

        }

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return {
            'status': 'denied',
            'msg': "An unexpected error occurred."
        }
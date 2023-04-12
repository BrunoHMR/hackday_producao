import pandas as pd
import requests
import json
import os
from flask import Flask, request, Response

# constants
token = '6166531884:AAHfsnsqgkQRV4998A92K-tMnOCPYKPCQVk'

# info about bot
# https://api.telegram.org/bot6166531884:AAHfsnsqgkQRV4998A92K-tMnOCPYKPCQVk/getMe

# get updates - pega a última mensagem que eu enviei para o bot
# https://api.telegram.org/bot6166531884:AAHfsnsqgkQRV4998A92K-tMnOCPYKPCQVk/getUpdates

# Webhook
# https://api.telegram.org/bot6166531884:AAHfsnsqgkQRV4998A92K-tMnOCPYKPCQVk/setWebhook?url=https://costa-del-data-api.onrender.com/costa_del_data/predict

# Delete Webhook
# https://api.telegram.org/bot6166531884:AAHfsnsqgkQRV4998A92K-tMnOCPYKPCQVk/deleteWebhook

# send message - envia mensagem do bot para mim
# https://api.telegram.org/bot6166531884:AAHfsnsqgkQRV4998A92K-tMnOCPYKPCQVk/sendMessage?chat_id=5507011943&text=Hi


def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot{}/'.format(token)
    url = url + 'sendMessage?chat_id={}'.format(chat_id)
    r = requests.post(url, json = {'text': text})
    print('Status Code {}'.format(r.status_code))

    return None

def load_data(id_reserva):
    df2 = pd.read_csv('test.csv')

    df_test = df2[df2['id'] == id_reserva]

    if not df_test.empty:

        data = json.dumps(df_test.to_dict(orient = 'records'))

    else:
        data = 'error'

    return data

def predict(data):
    url = 'https://costa-del-data-api.onrender.com/costa_del_data/predict'
    header = {'Content-type': 'application/json'}
    data = data

    r = requests.post(url, data = data, headers = header)
    print('Status Code {}'.format(r.status_code))

    df_api_call = pd.DataFrame(r.json(), columns = r.json()[0].keys())

    return df_api_call

def parse_message(message):
    chat_id = message['message']['chat']['id']
    id_reserva = message['message']['text']

    id_reserva = id_reserva.replace('/','')

    try:
        id_reserva = int(id_reserva)

    except ValueError:
        send_message(chat_id,'O id da reserva está errado')
        id_reserva = 'error'

    return chat_id, id_reserva

# API initialize
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])

def index():
    if request.method == 'POST':

        message = request.get_json()
        chat_id, id_reserva = parse_message(message)

        if id_reserva != 'error':
            data = load_data(id_reserva)

            if data != 'error':
                df_api_call = predict(data)

                msg = 'A reserva de id {} será {}.'.format(df_api_call.loc['id'].values[0], df_api_call.loc['predicao'].values[0])
                send_message(chat_id, msg)
                return Response('Ok', status=200)

            else:
                send_message(chat_id, 'id não disponível')
                return Response('Ok', status = 200)

        else:
            send_message(chat_id, 'O id da reserva está errado')
            return Response('Ok', status = 200)

    else:
        '<h1> Hotel Telegram Bot </h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
# Handler API
import os
import pickle
import pandas as pd
from flask import Flask, request, Response
from costa_del_data.CostaDelData import CostaDelData

# lê o modelo
xgb_final = pickle.load(open('model/xgb_production_vf.pkl', 'rb'))
# inicializa a API
app = Flask(__name__)

@app.route('/costa_del_data/predict', methods=['POST'])
def costa_del_data_predict():

    test_json = request.get_json()  # requisição do arquivo de teste formatado em json

    if test_json:  # se o dado chegou

        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        classe = CostaDelData()
        df_clean = classe.data_cleaning(test_raw)
        df_prep = classe.data_preparation(df_clean)
        df_prod = classe.get_prediction_to_json(xgb_final, test_raw, df_prep)

        return df_prod

    else:  # se o dado não chegou
        return Response('{}', status=200, mimetype='application/json')
        # status = 200 e {}: a requisição deu certo, mas a execução deu errado

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host = '0.0.0.0', port = port, debug = True)
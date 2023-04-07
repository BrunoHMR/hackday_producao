# imports
import math
import numpy             as np
import pandas            as pd
from category_encoders.count import CountEncoder

class CostaDelData(object):

    def __init__(self):
        self.home_path = ""

    def data_cleaning(self, df):
        # limpando coluna classificação do hotel
        df['Classificação do hotel'] = df.apply(lambda line: line['Classificação do hotel'].replace(' estrelas', ' '),
                                                axis=1)

        # preenchendo NAS da coluna número de hospedes com o valor mínimo de hospedes
        df['Número de hospedes'] = df['Número de hospedes'].apply(lambda x: 1 if math.isnan(x) else x)

        # transformando tipos das colunas
        df['Classificação do hotel'] = df['Classificação do hotel'].astype('int64')
        df['Número de hospedes'] = df['Número de hospedes'].astype('int64')
        df['Número de pernoites reservadas'] = df['Número de pernoites reservadas'].astype('int64')
        df['Meses da reserva até o check-in'] = df['Meses da reserva até o check-in'].astype('int64')

        # transformando as colunas categóricas de não em sim em numéricas de 0 e 1 para facilitar as análises
        df['Já se hospedou anterioremente'] = df['Já se hospedou anterioremente'].apply(
            lambda x: 0 if x == 'Não' else 1)
        df['Reserva com Estacionamento'] = df['Reserva com Estacionamento'].apply(lambda x: 0 if x == 'Não' else 1)
        df['Reserva feita por agência de turismo'] = df['Reserva feita por agência de turismo'].apply(
            lambda x: 0 if x == 'Não' else 1)
        df['Reserva feita por empresa'] = df['Reserva feita por empresa'].apply(lambda x: 0 if x == 'Não' else 1)

        # preenchendo os NAs da nacionalidade com Espanha, por ser o país da rede hoteleira
        df = df.fillna('Spain')

        # tratativa de outliers
        df = df[df['Meses da reserva até o check-in'] <= 24]
        df = df[(df['Número de pernoites reservadas'] != 0) & (df['Número de pernoites reservadas'] <= 30)]
        df_clean = df[(df['Número de hospedes'] != 0) & (df['Número de hospedes'] <= 6)]

        return df_clean

    def data_preparation(self, df_clean):
        # encodings e seleção de features
        x_cat_cols = ['Nacionalidade', 'Tipo do quarto reservado', 'Regime de alimentação', 'Reserva com Observações',
                      'Forma de Reserva']
        encoder = CountEncoder(cols=x_cat_cols, return_df=True)
        df_prep = encoder.fit_transform(df_clean)
        df_prep = df_prep.drop(
            ['Reserva feita por agência de turismo', 'Já se hospedou anterioremente', 'Reserva feita por empresa'],
            axis=1)

        return df_prep

    def get_prediction_to_json(self, xgb_final, df_original, df_prep):
        predicao = xgb_final.predict(df_prep)

        df_original['Predição'] = predicao

        return df_original.to_json(orient='records')


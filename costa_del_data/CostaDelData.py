# imports
import math
import numpy             as np
import pandas            as pd
import inflection
from category_encoders.count import CountEncoder

class CostaDelData(object):

    def __init__(self):
        self.home_path = ''

    @staticmethod
    def data_cleaning(self, df):
        # Renomeando colunas
        df = df.rename(columns={'id': 'id',
                    'Classificação do hotel': 'classificacao_do_hotel',
                    'Meses da reserva até o check-in': 'meses_da_reserva_ate_o_check_in',
                    'Número de pernoites reservadas': 'numero_de_pernoites_reservadas',
                    'Número de hospedes': 'numero_de_hospedes',
                    'Regime de alimentação': 'regime_de_alimentacao',
                    'Nacionalidade': 'nacionalidade',
                    'Forma de Reserva': 'forma_de_reserva',
                    'Já se hospedou anterioremente': 'ja_se_hospedou_anteriormente',
                    'Tipo do quarto reservado': 'tipo_do_quarto_reservado',
                    'Reserva feita por agência de turismo': 'reserva_feita_por_agencia_de_turismo',
                    'Reserva feita por empresa': 'reserva_feita_por_empresa',
                    'Reserva com Estacionamento': 'reserva_com_estacionamento',
                    'Reserva com Observações': 'reserva_com_observacoes'})

        # limpando coluna classificação do hotel
        df['classificacao_do_hotel'] = df.apply(lambda line: line['classificacao_do_hotel'].replace(' estrelas', ' '),
                                                axis=1)

        # preenchendo NAS da coluna número de hospedes com o valor mínimo de hospedes
        df['numero_de_hospedes'] = df['numero_de_hospedes'].apply(lambda x: 1 if math.isnan(x) else x)

        # transformando tipos das colunas
        df['classificacao_do_hotel'] = df['classificacao_do_hotel'].astype('int64')
        df['numero_de_hospedes'] = df['numero_de_hospedes'].astype('int64')
        df['numero_de_pernoites_reservadas'] = df['numero_de_pernoites_reservadas'].astype('int64')
        df['meses_da_reserva_ate_o_check_in'] = df['meses_da_reserva_ate_o_check_in'].astype('int64')

        # transformando as colunas categóricas de não em sim em numéricas de 0 e 1 para facilitar as análises
        df['ja_se_hospedou_anteriormente'] = df['ja_se_hospedou_anteriormente'].apply(lambda x: 0 if x == 'Não' else 1)
        df['reserva_com_estacionamento'] = df['reserva_com_estacionamento'].apply(lambda x: 0 if x == 'Não' else 1)
        df['reserva_feita_por_agencia_de_turismo'] = df['reserva_feita_por_agencia_de_turismo'].apply(
            lambda x: 0 if x == 'Não' else 1)
        df['reserva_feita_por_empresa'] = df['reserva_feita_por_empresa'].apply(lambda x: 0 if x == 'Não' else 1)

        # preenchendo os NAs da nacionalidade com Espanha, por ser o país da rede hoteleira
        df = df.fillna('spain')

        # Renomeando linhas das colunas categóricas
        # nacionalidade
        snakecase = lambda x: inflection.underscore(x)
        rows_nac = list(map(snakecase, df['nacionalidade']))
        df['nacionalidade'] = rows_nac
        df['nacionalidade'] = [i.replace(' ', '_') for i in df['nacionalidade']]
        df['nacionalidade'] = [i.replace(',', '_') for i in df['nacionalidade']]
        df['nacionalidade'] = [i.replace("'", '_') for i in df['nacionalidade']]
        df['nacionalidade'] = [i.replace("ô", 'o') for i in df['nacionalidade']]
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'russia' if (x == 'russia') | (x == 'russian_federation') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'south_korea' if (x == 'south_korea') | (x == 'korea__republic_of') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'ivory_coast' if (x == 'ivory_coast') | (x == 'cote_d_ivoire') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'iran' if (x == 'iran') | (x == 'iran__islamic_republic_of') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'tanzania' if (x == 'tanzania') | (x == 'tanzania__united_republic_of') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'taiwan' if (x == 'taiwan') | (x == 'taiwan__province_of_china') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(lambda x: 'france' if (x == 'france') | (x == 'monaco') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'venezuela' if (x == 'venezuela') | (x == 'venezuela__bolivarian_republic_of') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'bolivia' if (x == 'bolivia') | (x == 'bolivia__plurinational_state_of') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'macedonia' if (x == 'macedonia') | (x == 'macedonia__the_former_yugoslav_republic_of') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'dominican_republic' if (x == 'dominica') | (x == 'dominican_republic') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'libya' if (x == 'libya') | (x == 'libyan_arab_jamahiriya') else x)
        df['nacionalidade'] = df['nacionalidade'].apply(
            lambda x: 'vietnam' if (x == 'vietnam') | (x == 'viet_nam') else x)

        # tipo do quarto reservado
        rows_quarto = list(map(snakecase, df['tipo_do_quarto_reservado']))
        df['tipo_do_quarto_reservado'] = rows_quarto
        df['tipo_do_quarto_reservado'] = [j.replace(' ', '_') for j in df['tipo_do_quarto_reservado']]

        # regime de alimentação
        df['regime_de_alimentacao'] = df['regime_de_alimentacao'].apply(
            lambda x: 'cafe_almoco_janta' if (x == 'Café da manha, almoco e jantar') else
            'cafe_janta' if (x == 'Café da manha e jantar') else
            'cafe' if (x == 'Café da manha') else
            'sem_refeicao' if (x == 'Sem refeicao') else x)

        # reserva com observações
        df['reserva_com_observacoes'] = df['reserva_com_observacoes'].apply(lambda x: 'nenhuma' if (x == 'Nenhuma') else
        '1_a_3' if (x == '1 a 3') else
        'mais_de_3' if (x == 'Mais de 3') else x)

        # forma de reserva
        df['forma_de_reserva'] = df['forma_de_reserva'].apply(lambda x: 'agencia' if (x == 'Agência') else
        'balcao' if (x == 'Balcão') else
        'b2b' if (x == 'B2B') else x)

        # tratativa de outliers
        df = df[df['meses_da_reserva_ate_o_check_in'] <= 24]
        df = df[(df['numero_de_pernoites_reservadas'] != 0) & (df['numero_de_pernoites_reservadas'] <= 30)]
        df = df[(df['numero_de_hospedes'] != 0) & (df['numero_de_hospedes'] <= 6)]
        df_clean = df

        return df_clean

    @staticmethod
    def data_preparation(self, df_clean):
        # encodings e seleção de features
        x_cat_cols = ['regime_de_alimentacao', 'nacionalidade', 'forma_de_reserva', 'tipo_do_quarto_reservado', 'reserva_com_observacoes']
        encoder = CountEncoder(cols=x_cat_cols, return_df=True)
        df_prep = encoder.fit_transform(df_clean)

        # Dropando as colunas menos relevantes selecionadas (<1% de importância):
        df_prep = df_prep.drop(
            ['reserva_feita_por_agencia_de_turismo', 'ja_se_hospedou_anteriormente', 'reserva_feita_por_empresa'],
            axis=1)

        return df_prep

    @staticmethod
    def get_prediction_to_json(self, xgb_final, df_original, df_prep):
        predicao = xgb_final.predict(df_prep)

        df_original['predicao'] = predicao

        return df_original.to_json(orient='records')
# Hotel Chain Cancellation Rating

![HotelChain](https://user-images.githubusercontent.com/108444459/232348913-935b9576-98a3-4621-9cd3-3696b086cbf2.PNG)

## Problema de negócio

A Costa del Data é uma tradicional rede hoteleira espanhola. A empresa está preocupada com as suas projeções para os próximos anos, visando a recuperação financeira com o fim das restrições impostas pela pandemia de Covid-19. Com a reabertura das fronteiras, a diminuição nas restrições de viagem e o aumento das vacinações, era esperado que o setor hoteleiro da Espanha retomasse os ganhos outrora esperados. Na contramão desta expectativa, a Costa del Data tem visto um aumento em sua taxa de cancelamentos de reservas! A suspeita da diretoria é de que houve uma mudança no comportamento de cancelamentos por parte do consumidor após a pandemia, que ainda não foi compreendida pela rede. Isso travou ações estratégicas críticas como a expansão da rede hoteleira, a reforma das unidades já com obras programadas e a realização de ações de marketing direcionadas.

Com base no histórico de reservas dos hóspedes, o objetivo é desenvolver um modelo de previsão de cancelamentos. O modelo deve prever a variável alvo "Reserva Cancelada", retornando 1 em caso de cancelamento, e 0 em caso de não cancelamento.

Métrica de Avaliação do problema: F-Score (Macro).

## Passos para a resolução do problema

Para resolver o problema será utilizado o método CRISP DS. O CRISP DS é um método adaptado para a Ciência de Dados, onde são realizadas diversas etapas sequenciais as quais não devem ser interrompidas. Ao finalizar a última etapa, o ciclo reinicia e novas alterações são adicionadas a resolução do problema. Desta forma, é possível entregar uma solução completa com eficiência e rapidez, a qual pode ser aperfeiçoada diversas vezes em ciclos posteriores.

Neste projeto foi realizado um ciclo completo do CRISP DS, contemplando as seguintes etapas:
1. Levantamento do problema de negócio:
- Contexto do problema;
- Passos para a resolução do problema;
- Planejamento da solução.
2. Carregamento dos dados:
- Visão geral dos dados;
- Descrição dos atributos.
3. Limpeza dos dados:
- Aplicação de premissas;
- Descrição dos dados;
- Tratativa de outliers.
4. Análise exploratória de dados:
- Formulação de hipóteses de negócio;
- Proporção de cancelamento de variáveis;
- Análise de variáveis categóricas;
- Análise de variáveis numéricas;
- Conclusão e geração de insights.
5. Preparação dos dados:
- Encodings;
- Seleção de features por importância.
6. Implementação dos modelos de Machine Learning:
- Teste de modelos iniciais;
- Tunagem de parâmetros do modelo escolhido;
- Teste de generalização do modelo escolhido.
7. Resultados financeiros:
- Tradução do erro do modelo;
- Exemplo prático do ganho financeiro do modelo.
8. Modelo em produção:
- Design do ETL;
- Armazenamento do modelo treinado na nuvem;
- Desenvolvimento de API para verificar as reservas canceladas de acordo com o id dos usuários;
- Desenvolvimento de Bot no Telegram para verificar as reservas canceladas de acordo com o id dos usuários.

## Planejamento da solução

Fonte dos dados: https://www.kaggle.com/competitions/cdshackdays4/data

Ferramentas utilizadas: Python 3.9.16 e bibliotecas (contidas no arquivo do projeto 'requirements.txt').

Formato da entrega:
1. Arquivo .csv 'submission.csv' com as previsões para cada 'id' do conjunto de teste.
2. Bot no telegram com as previsões para cada 'id' do conjunto de teste.
* Considera-se o 'id' como um identificador único do usuário.

Para mais detalhes do projeto, ainda serão entregues:
1. Arquivos Python 'hotel-bot.py' e 'hotel-api.py' contendo as APIs remotas.
2. Arquivo Jupyter 'hotel_final', contendo todos os códigos detalhados da execução do projeto e o design do ETL.
3. Arquivo Jupyter 'teste_api_remota', contendo teste em funcionamento da API escrita no arquivo hotel-api.py.
4. Relatório de análise exploratória dos dados 'SWEETVIZ_REPORT.html'.

## Carregamento, limpeza e descrição dos dados

Atributos:
- 'id',
- 'Classificação do hotel',
- 'Meses da reserva até o check-in',
- 'Número de pernoites reservadas',
- 'Número de hospedes',
- 'Regime de alimentação',
- 'Nacionalidade',
- 'Forma de Reserva',
- 'Já se hospedou anterioremente',
- 'Tipo do quarto reservado',
- 'Reserva feita por agência de turismo',
- 'Reserva feita por empresa',
- 'Reserva com Estacionamento',
- 'Reserva com Observações',
- 'Reserva Cancelada'

Premissas:
- Para as linhas não preenchidas da coluna 'Número de hospedes' foi atribuida a quantidade mínima de hóspedes, que é de 1 hóspede.
- Para as linhas não preenchidas da coluna 'Nacionalidade' foi atribuído o país sede da rede hoteleira e que também se repete mais vezes, que é a Espanha.
- Foram tratadas como outliers as linhas da coluna 'Meses da reserva até o check-in' acima de 24 meses, as linhas da coluna 'Número de pernoites reservadas' acima de 30 pernoites e as linhas da coluna 'Número de hospedes' acima de 6 hóspedes, pois foi verificado que a quantidade de reservas totais para estas condições decaia drásticamente, acrescentando quantidades irrelevantes à análise e indicando possíveis preenchimentos equivocados.
- Foram eliminadas as linhas da coluna 'Número de pernoites reservadas' igual a 0 e as linhas da coluna 'Número de hospedes' igual a 0, pois subentende-se que deve ser reservada pelo menos uma pernoite e deve haver pelo menos 1 hóspede.

Como sugestão para próximos ciclos (quando houverem mais linhas NaNs para treinamento no conjunto), uma opção para o preenchimento destes NaNs sem utilizar apenas a Espanha, a fim de aumentar a performance do modelo, é preencher as linhas NaNs da nacionalidade utilizando um algoritmo de classificação, como o KNN ou a Random Forest. Neste ciclo foi testada esta possibilidade, porém o ganho na performance do modelo foi de apenas 0,05%. Deste modo, foi preferível manter os NaNs como Espanha.

![SweetVizNacionalidade](https://user-images.githubusercontent.com/108444459/232348839-6f19ca75-e2ae-49e8-af88-cacb5eaa01f7.PNG)

## Formulação das hipóteses de negócio

Apesar de numéricas, as colunas 'Já se hospedou anterioremente', 'Reserva com Estacionamento', 'Classificação do hotel', 'Reserva feita por empresa' e 'Reserva feita por agência de turismo' indicam classificações. Neste caso, serão interpretadas como categóricas.

Hipóteses relacionadas as variáveis categóricas:
- 1. Hotéis com classificação 5 estrelas possuem uma proporção de cancelamentos menor que hotéis com classificação de 4 estrelas.
- 2. Clientes que já se hospedaram anteriormente possuem uma proporção de cancelamentos menor que clientes que nunca se hospedaram antes.
- 3. Reservas feitas por balcão tem uma proporção de cancelamento maior que as realizadas por agência de turismo ou B2B.
- 4. Reservas feitas com estacionamento possuem uma menor proporção de cancelamento.
- 5. Reservas feitas com café da manhã, almoço e jantar possuem uma menor proporção de cancelamento que as demais.
- 6. Reservas feitas sem nenhuma observação possuem uma maior proporção de cancelamento que as demais.
- 7. Reservas feitas por países do continente europeu possuem uma menor proporção de cancelamento as demais.

Hipóteses relacionadas as variáveis numéricas:
- 8. Reservas feitas com um tempo igual ou menor a 2 meses do período de check-in possuem uma menor proporção de cancelamento.
- 9. Reservas feitas com apenas uma pernoite possuem uma maior quantidade de cancelamentos em média que as demais.
- 10. Reservas feitas com 2 hóspedes possuem uma maior quantidade de cancelamentos em média que as demais.

## Análise exploratória dos dados:

Após a realização de uma análise estatística dos dados, onde foram realizadas as seguintes etapas:
- Cálculo das proporções de cancelamento para cada atributo do conjunto de dados;
- Análise univariada das variáveis numéricas e da variável resposta;
- Análise bivariada das variáveis numéricas e das variáveis categóricas;
- Correlação de Pearson para as variáveis numéricas;
- Método de Cramer's V para as variáveis categóricas.

Foi possível obter os seguintes resultados em relação às hipóteses de negócio formuladas:

Hipótese Conclusão Relevância Insight

i -------- V --------- B ---------- I

ii -------- V --------- B ---------- I

iii	------- F --------- B ---------- P

iv ------- V --------- B ---------- P

v -------- V --------- B ---------- P

vi	------- V --------- M ---------- P

vii ------- V*	-------- M ---------- P

viii ------ V --------- M ---------- P

ix ------- F --------- B ---------- P

x -------- V --------- B ---------- P

Legendas:
- Conclusão: V para verdadeira, F para falsa, * para exceto Espanha.
- Relevância: B para baixa, M para média, A para alta.
- Insight: I para improvável, P para provável.

Consideração sobre a coluna id:
- A coluna id está diretamente ligada ao comportamento das reservas canceladas.

É possível dividir os ids em 4 grupos:
- Do id 0 a 20 mil, em média, a quantidade de cancelamentos é muito maior que a quantidade de reservas confirmadas.
- Do id 20 mil ao 50 mil, em média, a quantidade de cancelamentos é muito menor que a quantidade de reservas confirmadas.
- Do id 50 mil ao id 80 mil, em média, a quantidade de cancelamentos é novamente muito maior que a quantidade de reservas confirmadas.
- Do id 80 mil em diante, em média, a quantidade de cancelamentos é novamente muito menor que a quantidade de reservas confirmadas.

![SweetVizId](https://user-images.githubusercontent.com/108444459/232348664-1b4af3e4-719e-4625-9b27-477d4243d6fe.PNG)

Sugestões à empresa:
- Como a proporção de cancelamentos por balcão é menor que as proporções por agência e B2B, oferecer pacotes com desconto, realizar parcerias com agências de turismo e com empresas e alocar recursos de marketing nestes grupos de clientes pode reduzir a taxa de cancelamentos.
- Inserir multas progressivas ou reembolsos parciais para cancelamentos de reservas realizadas a mais de 30 dias.
- Inserir pequenas multas progressivas ou reembolsos parciais para cancelamentos de reservas realizadas para 2 ou mais pernoites.

## Encodings

Como o problema é de classificação, foram pensados algoritmos de árvores de decisão para o treinamento do modelo. Por este motivo, foi realizado apenas o encoding das variáveis categóricas, visto que as árvores de decisão não realizam contas, apenas recortes no espaço de dados. Então, foi definido um encoding do tipo Count Encoder, que realiza a transformação dos atributos categóricos em numéricos de acordo com a quantidade de vezes que o atributo aparece no conjunto de dados.

Isto poderia ser um problema caso as classificações da variável resposta fossem muito desbalanceadas. Porém, como a proporção dos dados era de 63% para não confirmados e 37% para confirmados o desbalanceamento não era tão grande, apresentando resultados semelhantes após a modelagem em comparação ao One Hot Encoding e ao Target Encoding, que poderiam ser opções mais viáveis para dados não balanceados. Para um próximo ciclo, conforme mais dados forem armazenados, caso o o desbalanceamento aumente deve ser considerado outro tipo de encoding.

## Seleção de features

Para a seleção dos atributos foi utilizado um algoritmo de Random Forest e um método da biblioteca scikit-learn chamado feature_importances_, que quando aplicado é capaz de treinar um modelo e definir a relevância de cada uma das features para a modelagem através do decrescimento médio da impureza (MDI).

Ficou evidente a importância do 'id', o qual apresentou um MDI maior que 60%. Ou seja, só ele explicava cerca de 60% do fenômeno. Além disso, foram dropadas as colunas com menos de 1% de relevância para o modelo: 'reserva_feita_por_agencia_de_turismo', 'ja_se_hospedou_anteriormente' e 'reserva_feita_por_empresa'.

![FeatureImportances](https://user-images.githubusercontent.com/108444459/232348529-c1ae0ab0-65eb-4ecc-81f8-6593fb6a7fcd.PNG)

## Modelagem

Primeiramente o arquivo .csv de treino foi separado em treino e teste, onde foram dedicados 20% dos dados para teste.

Para a modelagem foram testados 3 modelos de árvore de decisão, os quais são de fácil implementação e apresentam resultados excelentes em problemas de classificação: Random Forest, XGBoost e LGBM. Sem a tunagem dos parâmetros e com a aplicação da técnica de Cross-Validation para 5 divisões do conjunto de dados, foram obtidas as seguintes performances de F1-Score Macro médio:
- Random Forest: 96,98%.
- XGBoost: 96,89%.
- LGBM: 96,36%.

Devido ao fato do XGBoost apresentar uma melhora um pouco mais significativa após a realização da tunagem dos parâmetros e os resultados terem sido muito semelhantes, foi realizada escolhido seguir apenas com o XGBoost para a entrega de uma solução em menor tempo.

Para um próximo ciclo de projeto, sugere-se realizar a separação entre treino e teste tratando o id como parâmetro referencial devido a sua potencial indicação de sazonalidade. Ou seja, os ids maiores devem ser separados para teste, enquanto os demais ficam como treino. Desta forma, os resultados do algoritmo seriam mais fiéis, pois o problema seria tratado como uma time-series.

## Tunagem dos parâmetros

Os métodos de tunagem foram separados em: Grid Search, Random Search e Bayes Search.
- Grid Search: foi descartada devido ao tempo de resposta ser muito alto. Como a performance do modelo já é considerada bem elevada mesmo sem a tunagem, do ponto de vista de negócio, para uma entrega de solução rápida, a Grid Search acaba sendo inviável.
- Random Search: apresentou uma relativa demora na execução, mesmo para uma quantidade de apenas 10 iterações. Além disso, apresentou um resultado inferior à Bayes Search.
- Bayes Search: foi a escolhida por ter alcançado a melhor performance e por ter demorado menos tempo para ser executada (4h30min para 100 interações e 5 folds, com uma lista de 6 parâmetros, cada um com 5 valores distintos a serem testados).

## Generalização do modelo

Após a tunagem dos parâmetros foi realizado o retreino do modelo. Desta vez, sobre os dados separados para teste, para verificar a capacidade de generalização do modelo e detectar um possível overfitting. Neste último treino, foram obtidos os seguintes valores:
- F1-Score Macro médio final:  96,34%.
- Precision média final:  96,76%.
- Recall médio final:  95,92%.

Como a queda no F1-Score Macro médio foi de menos de 1%, os dados separados foram concatenados e retreinados para serem enviados à produção.

![Performance](https://user-images.githubusercontent.com/108444459/232349071-61450fe1-fe60-4e7d-8645-14363d11b243.PNG)

## Resultados financeiros

Para traduzir os resultados do modelo em resultados financeiros, é possível realizar a seguinte análise:

- Percentual de reservas canceladas: 37,3%.
- F1-Score Macro médio do algoritmo (pós generalização): 96,3%.
- Percentual de reservas canceladas que o algoritmo consegue prever (recall): 95,9%.

Multiplicando o percentual de reservas canceladas pelo recall do algoritmo:
37,3% * 95,9% = 35,8%.

Deste modo, o aumento que a empresa terá com reservas em sua receita pode chegar até 35,8%. Isso ocorreria caso ela conseguisse reverter 100% dos cancelamentos. Portanto, para prever o percentual de aumento de receita através das reservas a empresa deve multiplicar os 35,8% pela sua taxa de reversão de cancelamentos.

Exemplo prático:

A diária tem um ticket médio de USS 1.000,00 e consegue uma quantidade média de 1.000 reservas diárias. Em um dia, a empresa está perdendo, em média, 373 reservas, totalizando o valor médio diário de US$ 373.000,00, mensal de US$ 11.190.000,00 e anual de US$ 134.280.000,00.

Considere uma taxa de reversão de cancelamentos hipotética da empresa de 50%. Multiplicando este valor pelo percentual de reservas canceladas que o algoritmo consegue prever, que é de 35,8%, é obtido um valor percentual médio de reservas canceladas de 17,9%. Então, em um dia, a empresa consegue reverter 179 cancelamentos (17,9% de 1000 reservas diárias), totalizando o valor médio diário de US$ 179.000,00, mensal de US$ 5.370.000,00 e anual de USS 64.440.000,00!

Em comparação, com o baseline de 67% setado no início do projeto o retorno seria de: 37,3% * 67% * 50% = 12,5%

Ou seja, a empresa conseguiria recuperar 125 clientes, totalizando um valor médio diário de US$ 125.000,00, mensal de USS 3.750.000,00 e anual de US$ 45.000.000,00.

Fazendo a diferença entre o potencial do algoritmo do projeto em relação ao algoritmo baseline, o valor médio anual obtido é US$ 19.440.000,00 maior!

## Como testar um Bot no Telegram

Para testar o Bot você deve realizar as seguintes etapas:
- Na barra de pesquisa do seu aplicativo Telegram, busque por: HotelBot
- Na conversa com o Bot, digite /id (troque 'id' por um número, por exemplo: /877).

![HotelBot](https://user-images.githubusercontent.com/108444459/232347859-f2f70bbc-9f3b-40db-8ddf-3a02400d455d.PNG)

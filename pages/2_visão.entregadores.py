# 0.1. importar livros
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go 
import streamlit as st
import datetime
from PIL import Image
from streamlit_folium import folium_static

#bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
from haversine import haversine, Unit
import folium

# Funções

def clean_code(df):
    # a) Limpeza e tratamento dos dados

    # 0.3. Tratamento dos dados
    # b) Tratamento e Limpeza dos dados
    # b.1) Removendo os 'NaN'
    linhas_selecionadas = ((df['Delivery_person_Age'] != 'NaN ' ) & 
                        (df["multiple_deliveries"] != 'NaN ') & 
                        (df['Road_traffic_density'] != 'NaN ') & 
                        (df['City'] != 'NaN ') & 
                        (df['Festival'] != 'NaN ') &
                        (df['Time_taken(min)'] != 'NaN ' ) & 
                        (df['Delivery_person_Age'] != 'Low ' ) &
                        (df['Order_Date'] != 'NaN '))
    df1 = df.loc[linhas_selecionadas, :]

    # b.2) Tratamento das colunas
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype( float )
    df1["Order_Date"] = pd.to_datetime( df1["Order_Date"], format='%d-%m-%Y' )
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype ( int )

    # b.3) Remmovendo os espaço de strings/texto/object: O str cria uma condição que permite utilizar o strip diretamente
    # Para indentificar se a coluna tem espaço utilize o df.loc[0, "Nome da coluna"]
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    # b.4) Removendo o min do tempo médio
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(str).apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    return df1

# b) Top entregadores

def top_delivery(df1, top_asc):
                """
                df1 = Dataframe
                top_asc True: Crescente ou False: Decrescente

                input = Dataframe
                output = Dtaraframe (name = df3)
                """
                Delivery_per_Time_taken = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                                              .groupby( ['City', 'Delivery_person_ID'])
                                              .mean()
                                              .sort_values( ['City', 'Time_taken(min)'], ascending=top_asc).reset_index())
                
                # Criando os filtros
                df_aux1 = Delivery_per_Time_taken.loc[Delivery_per_Time_taken['City'] == 'Metropolitian', :].head(10)
                df_aux2 = Delivery_per_Time_taken.loc[Delivery_per_Time_taken['City'] == 'Urban', :].head(10)
                df_aux3 = Delivery_per_Time_taken.loc[Delivery_per_Time_taken['City'] == 'Semi-Urban', :].head(10)

                # Unindo as tabelas
                df3 = pd.concat( [df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
                return df3

# Tamnaho da página
st.set_page_config(
    page_title="Visão Entregadores",
    page_icon='🛵',
    layout="wide")

# 0.2. Importar dataset 
    # Para que o comando seja exibido no terminal devemos utilizar o print
df = pd.read_csv( 'train.csv')

df1 = clean_code(df)

# ==========================================================
 # 2. Layout do Streamlit
# ==========================================================

# 2.0. Barra lateral (st.sidebar)
# Imagem da Logo
#imagem_path = "logo.jpg"
imagem = Image.open( 'logo.jpg')
st.sidebar.image ( imagem, width=240)

st.sidebar.markdown( '# Curry Company')
st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown( '''___''')

# 2.0.1 Filtros de data
st.sidebar.markdown( '## Selecione uma data limite')

# a) Slider com datas
date_slider = st.sidebar.slider(
    'Até qual valor?',
    min_value=datetime.datetime(2022, 1, 1),
    max_value=datetime.datetime(2022, 4, 6),
    value=datetime.datetime(2022, 4, 6),
).strftime('%d-%m-%Y')

st.sidebar.markdown( '''___''')

# b) Seleção multiplas
traffic_options = st.sidebar.multiselect( 
    'Quais as condições do transito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown( '''___''')
st.sidebar.markdown('## Portfólio de Projetos Marcos Paulo')

# 2.0.2. Conectando os filtros a base de dados

# a) Filtros de data
linhas_selecionadas_filtro = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas_filtro, :]

# b) Filtros de transito
    # isin Verifica se a lista de dados está dentro da variável
linhas_selecionadas_filtro = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas_filtro, :]

# 2.1. Tela Inicial
st.markdown('# Marketplace - Visão Entregadores')
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
         st.title('1. Overall Metrics')
            # gap='large': Distancia entre as colunas
         col1, col2, col3, col4 = st.columns(4)
         with col1:
        # A maior idade dos entregadores
             colunas221 = ['Delivery_person_Age']
             maior_idade = df1.loc[:, colunas221].max().values[0]
             col1.metric( 'Maior Idade', maior_idade)
       
         with col2:
        # A menor idade dos entregadores
            menor_idade = df1.loc[:, colunas221].min().values[0]
            col2.metric( 'Menor Idade', menor_idade)

         with col3:
            colunas222 = ['Vehicle_condition']
            melhor_condição = df.loc[:, colunas222].max().values[0]
            col3.metric( 'Melhor Condição de Veículo', melhor_condição)
       
         with col4:
            pior_condição = df.loc[:, colunas222].min().values[0]
            col4.metric( 'Pior Condição de Veículo', pior_condição)
    with st.container():
         st.markdown('''___''')
         st.title( '2. Avaliações')
         col1, col2 = st.columns( 2 )

         with col1:
            st.markdown(' ##### Avaliações Média por entregador')
            colunas223 = ['Delivery_person_ID', 'Delivery_person_Ratings']
            df_avg_ratings_per_deliver = (df1.loc[:, colunas223]
                                             .groupby('Delivery_person_ID')
                                             .mean()
                                             .round(2)
                                             .sort_values('Delivery_person_Ratings', 
                                                       ascending= False).reset_index())
            
            # Adicionando o CSS para garantir que a tabela ocupe toda a largura da coluna
            st.dataframe(df_avg_ratings_per_deliver)

         with col2:
                 st.markdown(' ##### Avaliaçõe Média por Transito')
                 colunas224 = ['Delivery_person_Ratings','Road_traffic_density']
                 df_avg_ratings_per_traffic = (df1.loc[:, colunas224]
                                                  .groupby( 'Road_traffic_density')
                                                  .agg( {'Delivery_person_Ratings':['mean', 'std']})
                                                  .round(2))
                # Mudando nome de colunas
                    # o .agg() retorna colunas multiníveis, vamos reorganiza-las para um nível
                 df_avg_ratings_per_traffic.columns = ['Ratings_mean', 'Ratings_std']

                 # Resetando o index e exibindo a coluna
                 df_avg_ratings_per_traffic.reset_index()
                 # Adicionando o CSS para garantir que a tabela ocupe toda a largura da coluna
                 
                 st.dataframe(df_avg_ratings_per_traffic)

                 st.markdown(' ##### Avaliaçõe Média por Condição Climática')
                 colunas225 = ['Delivery_person_Ratings','Weatherconditions']
                 df_avg_ratings_per_weathercond = (df1.loc[:, colunas225]
                                                      .groupby( 'Weatherconditions')
                                                      .agg( {'Delivery_person_Ratings':['mean', 'std']})
                                                      .round(2))
                 # Mudando nome de colunas
                    # o .agg() retorna colunas multiníveis, vamos reorganiza-las para um nível
                 df_avg_ratings_per_weathercond.columns = ['Weath_mean', 'Weath_std']

                # Resetando o index e exibindo a coluna
                 df_avg_ratings_per_weathercond.reset_index()
                 st.dataframe(df_avg_ratings_per_weathercond)

    with st.container():
         st.markdown('''___''')
         st.title( '3. Velocidade de Entrega')
         col1, col2 = st.columns(2)
         with col1:
              st.markdown(' ##### Top Entregadores mais Rápidos')
              df3 = top_delivery(df1, top_asc=True)
              st.dataframe(df3)
              
         with col2:
              st.markdown(' ##### Top Entregadores mais Lentos')
              df3 = top_delivery(df1, top_asc=False)
              st.dataframe(df3)
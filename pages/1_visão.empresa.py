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

# Tamnaho da página
st.set_page_config(
    page_title="Visão Empresa",
    page_icon='💼',
    layout="wide")

# =====================================================================================================================
# 0. Funções
# =====================================================================================================================

# 0.1. Função de limpeza
    # Essa função tem a respondabilidade de limpar o Datafream
    # Tipos de limpeza:
    # 1. Remoção dos dados NaN
    # 2. Mudança do tipo da coluna
    # 3. Remoção dos espaço das variaveis de texto
    # 4. Formatação da data
    # 5. Limpeza da coluna de tempo ( Remoção do texto da variável numérica)

    # input: Datafream
    # output: Datafream

def clean_code(df):
# a) Removendo os 'NaN'
    linhas_selecionadas = ((df['Delivery_person_Age'] != 'NaN ' ) & 
                        (df["multiple_deliveries"] != 'NaN ') & 
                        (df['Road_traffic_density'] != 'NaN ') & 
                        (df['City'] != 'NaN ') & 
                        (df['Festival'] != 'NaN ') &
                        (df['Time_taken(min)'] != 'NaN ' ) & 
                        (df['Delivery_person_Age'] != 'Low ' ) &
                        (df['Order_Date'] != 'NaN '))
    df1 = df.loc[linhas_selecionadas, :]

    # n) Tratamento das colunas
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype( float )
    df1["Order_Date"] = pd.to_datetime( df1["Order_Date"], format='%d-%m-%Y' )
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype ( int )

    # c) Remmovendo os espaço de strings/texto/object: 
        #  O str cria uma condição que permite utilizar o strip diretamente
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    # d) Removendo texto da coluna numérica
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(str).apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# 0.2. Função de gráficos bar
    # Essa função tem a respondabilidade de criar uma figura para ser utilizada em um gráfico

    # input: Datafream
    # output: fig

def order_metric( df1 ):
            colunas211 = ['ID', 'Order_Date']
            colgpby211 = ['Order_Date']
            dfaux211 = (df1.loc[:, colunas211]
                           .groupby( colgpby211 )
                           .count()
                           .sort_values( colgpby211 )
                           .reset_index())
            dfaux211.columns = ['Ordem_date', 'Entregas_feitas']

            # b) Gráfico
            fig_1 = px.bar( dfaux211, x = 'Ordem_date', y = 'Entregas_feitas')
            
            return fig_1

# Função de Gráfico 2 pie
def traffic_order_share( df1 ):
                # a) Tabela
                colunas213 = ['ID', 'Road_traffic_density']
                colgpby213 = ['Road_traffic_density']
                dfaux213 = (df1.loc[:, colunas213]
                               .groupby( colgpby213 )
                               .count()
                               .sort_values( 'ID', ascending=False)
                               .reset_index())
                dfaux213['perc_ID'] = dfaux213['ID']/dfaux213['ID'].sum()

                # b) Gráfico
                fig_2 = px.pie( dfaux213, values='perc_ID', names = 'Road_traffic_density')

                return fig_2

# Função de Gráfico 3 scatter
def traffic_order_city(df1):
                # a) Tabela
                colunas214 = ['ID', 'City', 'Road_traffic_density']
                colgpby214 = ['City', 'Road_traffic_density']
                dfaux214 = (df1.loc[:, colunas214]
                               .groupby( colgpby214 )
                               .count().reset_index()
                               .sort_values( ['City','Road_traffic_density'] ))
                
                # b) Gráficos
                fig_3 = px.scatter(dfaux214, x='City', y='Road_traffic_density', size = 'ID')
                return fig_3

# Função de Gráfico 4 bar
def order_by_week(df1):
            # a) Tabela
            # Criando a coluna das semanas do ano
            df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], errors='coerce')
            df1['week_of_year'] = df1['Order_Date'].dt.isocalendar().week

            # Contando os pedidos por semana
            colunas212 = ['ID', 'week_of_year']
            colgpby212 = ['week_of_year']

            dfaux212 = df1.loc[:, colunas212].groupby( colgpby212 ).count().sort_values( colgpby212 ).reset_index()
            
            # b) Gráfico
            fig_4 = px.bar( dfaux212, x='week_of_year', y='ID')
            return fig_4

# Função de Gráfico 5 line
def order_share_by_week(df1):
             # a) Tabela
            order_week216 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
            delivery_week216 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

            # b) Gráfico
            dfaux216 = pd.merge( order_week216, delivery_week216, how='inner')
            dfaux216['order_delivery'] = (dfaux216['ID']/dfaux216['Delivery_person_ID']).round(2)
            fig_5 = px.line( dfaux216, x='week_of_year', y='order_delivery')
            return fig_5

# Função de mapa
def country_maps(df1):
        # a) Tabela
        colunas215 = ['Restaurant_latitude', 'Restaurant_longitude', 'City', 'Road_traffic_density']
        colgpby215 = ['City', 'Road_traffic_density']

        dfaux215 = (df1.loc[:, colunas215]
                    .groupby(colgpby215)
                    .median()
                    .reset_index()
                    .sort_values(colgpby215))

        # b) Mapa
        map_ = folium.Map( zoom_start=11)
        for index, location_info in dfaux215.iterrows():
            folium.Marker( 
                        location= [location_info['Restaurant_latitude'],
                        location_info['Restaurant_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to( map_ )
        
        folium_static( map_, width=1024, height=600)
        return None
# ----------------------------------------------------------------- Inicio da Estrutura Lógica do Código -----------------------------------------------------------------

# 0.2. Importar dataset 
    # Para que o comando seja exibido no terminal devemos utilizar o print
df = pd.read_csv( 'train.csv')
# Limpando os dados
df1 = clean_code(df)

# ==========================================================
 # 2. Layout do Streamlit
# ==========================================================

# 2.0. Barra lateral (st.sidebar)
# Imagem da Logo
# imagem_path = "logo.jpg"
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

# a.1) Exibição do date_slider na tela inicial
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

# 2.1. Tela inicial
st.title( 'Marketplace - Visão Empresa')
# 2.1.1. Abara
tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 
                             'Visão Tática', 
                             'Visão Geográfica'])
# I) tab1
with tab1:
    with st.container():
        st.markdown('# 1. Orders by day')
        # a) Tabela
        fig_1 = order_metric( df1 )
        st.plotly_chart( fig_1, use_container_width=True)
        st.markdown( '''___''')

    # Colunas
    with st.container():
        col1, col2 = st.columns( 2 )

        with col1:
            st.markdown('# 2. Traffic Order Share')
            fig_2 = traffic_order_share( df1)
            st.plotly_chart( fig_2, use_container_width=True)

        with col2:
            st.markdown('# 3. Traffic Order City')
            fig_3 = traffic_order_city(df1)
            st.plotly_chart( fig_3, use_container_width=True)

st.markdown( '''___''')

with tab2:
    with st.container():
         st.markdown( '# 4. Order by week')
         fig_4 = order_by_week(df1)
         st.plotly_chart( fig_4, use_container_width=True)
         st.markdown( '''___''')
    
    with st.container():
         # Quantas entregas na semana / Quantos entregadores únicos por semana
         st.markdown( '# 5. Order Share by Week')
         st.markdown( 'Esse gráfico reflete a quatidade de entregadores feitas por entregador durante a semana. '
                      'Ou seja, a quantidade de entregas feitas por cada entregador cadastrado na base de dados durante o período analisado.' \
                      ' Esse gráfico é fundamental para encontrar quais são os momentos em que o fastfood precisará' \
                      'de mais entregadores')
         fig_5 = order_share_by_week(df1)
         st.plotly_chart( fig_5, use_container_width=True)

with tab3:
    st.markdown( '# 6. Country Maps')
    country_maps(df1)
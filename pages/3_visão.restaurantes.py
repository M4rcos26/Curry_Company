# =============================================================================
# 0. Sumário
# =============================================================================

# 1. Introdução............................................................. 46
    # a) Organização dos dados.............................................. 49
    # b) Principais comando do streamlit.................................... 54

# 2. Preparação............................................................. 60
    # a) Livros............................................................. 63
    # b) Bibliotecas........................................................ 73
    # c) Importação dataset................................................. 81
    # d) Tratamento dos dados............................................... 84
        # I) Limpeza dos dados.............................................. 85
            # I.I) Removendo os 'NaN'....................................... 86
            # I.II) Tratamento das colunas.................................. 97
            # I.III) Removendo os espaço de strings/texto/object:........... 103
            # I.IV) Coluna 'Time_taken(min)'................................ 113

# 3. Layout do Streamlit.................................................... 119
    # a) Barra Lateral...................................................... 122
        # I) Imagem da Logo................................................. 125
        # II) Filtros de data............................................... 134
        # III) Slider com datas............................................. 137
        # IV) Seleção multiplas............................................. 146
        # V) Conectando os filtros a base de dados.......................... 156
            # V.I) Filtros de data.......................................... 157
            # V.II) Filtros de transito..................................... 161
    # b) Tela Inicial....................................................... 165
        # I) Visão Gerencial................................................ 169
            # I.I) Métricas Gerais.......................................... 172
                # I.I.I) Entregadores Únicos................................ 178
                # I.I.II) Distância Média................................... 183
                # I.I.III) Tempo médio - Festival........................... 194
                # I.I.IV) Desvio padrão - Festival.......................... 209
                # I.I.V) Tempo médio - Sem Festival......................... 223
                # I.I.VI) Desvio padrão - Sem Festival...................... 222
            # I.II) Tempo Médio de Entrega.................................. 253
                # I.II.I) Gráfico de Barras................................. 259
                # I.II.II) Tabela........................................... 283
            # I.III) Distribuição do Tempo.................................. 298
                # I.III.I) Gráfico de Pizza................................. 304
                # I.III.II) Gráfico de Sunburst............................. 329

# =============================================================================
# 1. Introdução
# =============================================================================

# a) Organização dos dados
    # I) df: Dataset original
    # II) df1: Dataset apos a limpeza e tratamento dos dados
    # III) Os filtros seram inseridos na sidebar (barra lateral)

# b) Principais comando do streamlit
    # I) st.sidebar: Insere o elemento na sidebar (barra lateral)
    # II) st.sidebar.markdown utilizado para inserir textos
    # III) st.sidebar.image: utilizado para carregar imagens


# =============================================================================
# 2. Função
# =============================================================================

# a) Limpeza de dados
def clean_code(df):
    """
    df: Dataframe
    
    1. O que o código faz?
    I) Limpeza dos dados
    I.I) Removendo os 'NaN'
    I.II) Tratamento das colunas
    I.III) Remmovendo os espaço de strings/texto/object: 
    I.IV) Coluna 'Time_taken(min)'

    input: Dataframe
    output: Datarame
    """
    # d) Tratamento dos dados
    # I) Limpeza dos dados
    # I.I) Removendo os 'NaN'
    linhas_selecionadas = ((df['Delivery_person_Age'] != 'NaN ' ) & 
                        (df["multiple_deliveries"] != 'NaN ') & 
                        (df['Road_traffic_density'] != 'NaN ') & 
                        (df['City'] != 'NaN ') & 
                        (df['Festival'] != 'NaN ') &
                        (df['Time_taken(min)'] != 'NaN ' ) & 
                        (df['Delivery_person_Age'] != 'Low ' ) &
                        (df['Order_Date'] != 'NaN '))
    df1 = df.loc[linhas_selecionadas, :]

    # I.II) Tratamento das colunas
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype( float )
    df1["Order_Date"] = pd.to_datetime( df1["Order_Date"], format='%d-%m-%Y' )
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype ( int )

    # I.III) Remmovendo os espaço de strings/texto/object: 
        # O str cria uma condição que permite utilizar o strip diretamente
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    # I.IV) Coluna 'Time_taken(min)'
        # É necesário removendo o min para efetuar a análise dos dados
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(str).apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    return df1

# b) Distancia
def distance(df, fig):
                if fig == False:
                    colunas = ['Restaurant_latitude', 'Restaurant_longitude', 
                            'Delivery_location_latitude', 'Delivery_location_longitude']
                    df1['distance'] = df1.loc[:, colunas].apply( lambda x:
                                                                        haversine(
                                                                                    (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), 
                                                                                    axis=1)
                    avg_distance = np.round(df1['distance'].mean(), 2)
                    return avg_distance
                else:
                    # I.III.I.I) Tabela com os dados
                    colunas = ['Restaurant_latitude', 'Restaurant_longitude', 
                               'Delivery_location_latitude', 'Delivery_location_longitude']
                    df1['distance'] = (df1.loc[:, colunas]
                                        .apply( lambda x:
                                                    haversine(
                                                        (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 ))

                    avg_disance = (df1.loc[:, ['City', 'distance']].groupby( 'City' )
                                                                   .mean()
                                                                   .reset_index()
                                                                   .round(2))
                    
                    # I.III.I.II) Gráfico de Pizza (Desloca uma das Fatias)
                        # pull: Determina qual fatia será Deslocada e o quanto
                    fig = go.Figure( data=[ go.Pie( labels=avg_disance['City'], 
                                                    values=avg_disance['distance'], 
                                                    pull=[0, 0.1, 0])])
                    return fig   

# c) avg_time e std_time da entrega
def avg_std_time_delivery(df1, festival, op):
                """
                    Essa função calcula o tempo médio e o desvio padrão do tempo de entrega.
                    Parâmetros:
                        input: 
                            - df: Dataframe
                            - festival: 
                                - 'Yes': Com Festival
                                - 'No': Sem Festival
                            - op: Operação
                                - 'avg_time': Calcula o tempo médio de entrega
                                - 'std_time': Calcula o desvio padrão do tempo de entrega
                        outpu:
                            - Datafreme com 2 colunas e 1 linha
                """
                df_aux_236 = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                                .groupby('Festival')
                                .agg( {'Time_taken(min)': ['mean', 'std']}))

                # I.I.III.I) Organizando as colunas em um nível
                df_aux_236.columns = [ 'avg_time', 'std_time']
                df_aux_236 = df_aux_236.reset_index()

                # I.I.III.II) Seleção das linhas com o festival
                avg_time_festival = df_aux_236[df_aux_236['Festival'] == festival][op]
                avg_time_festival = np.round(avg_time_festival, 2)
                return avg_time_festival

# d) gráfico de barras
def avg_std_time_graph(df1):
                # I.II.I.II) Tabela contendo os dados
                colunas = ['Time_taken(min)', 'City']
                df_aux_233 = (df1.loc[:, colunas].groupby('City')
                                                .agg( {'Time_taken(min)': ['mean', 'std']})
                                                .round(2))

                # I.II.I.II) Organização das colunas em um nível
                df_aux_233.columns = [ 'avg_time', 'std_time']
                df_aux_233 = df_aux_233.reset_index()

                # I.II.I.III) Gráfico de barras (destaque para o desvio-padrão)
                fig = go.Figure()
                fig.add_trace ( go.Bar(name='Control',
                                    x=df_aux_233['City'],
                                    y=df_aux_233['avg_time'],
                                    error_y=dict (type='data', 
                                                    array=df_aux_233['std_time'])))

                fig.update_layout( barmode='group')
                return fig

# e) Gráfico sunburst
def avg_std_time_on_traffic(df1):
                # I.III.II.I) Tabela com os dados
                colunas = ['Time_taken(min)', 'City', 'Road_traffic_density']
                df_aux_235 = (df1.loc[:, colunas]
                                .groupby(['City', 'Road_traffic_density'])
                                .agg( {'Time_taken(min)': ['mean', 'std']}))

                # I.III.II.II) Organizando as colunas em um nível
                df_aux_235.columns = [ 'avg_time', 'std_time']
                df_aux_235 = df_aux_235.reset_index()

                # I.III.II.III) Gráfico Sunburst
                fig = px.sunburst(df_aux_235, 
                                path=['City', 'Road_traffic_density'], 
                                values='avg_time',
                                color='std_time', color_continuous_scale='RdBu_r',
                                color_continuous_midpoint=np.average(df_aux_235['std_time']))
                return fig
# =============================================================================
# 2. Preparação
# =============================================================================

# a) Livros
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go 
import streamlit as st
import datetime
import numpy as np
from PIL import Image
from streamlit_folium import folium_static

# b) Bibliotecas 
import pandas as pd
import numpy as np
import plotly.express as px
from haversine import haversine, Unit
import folium

# Tamnaho da Página
st.set_page_config(
    page_title="Visão Restaurantes",
    page_icon='🍗',
    layout="wide")

# c) Importação dataset 

df = pd.read_csv( 'train.csv')
df1 = clean_code(df)

# =============================================================================
# 3. Layout do Streamlit
# =============================================================================

# a) Barra lateral 
    # Para colocar um elemento na barra lateral utilizamos o st.sidebar

# I) Imagem da Logo
# imagem_path = "logo.jpg"
imagem = Image.open( 'logo.jpg')
st.sidebar.image ( imagem, width=240)

st.sidebar.markdown( '# Curry Company')
st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown( '''___''')

# II) Filtros de data
st.sidebar.markdown( '## Selecione uma data limite')

# III) Slider com datas
date_slider = st.sidebar.slider(
                            'Até qual valor?',
                             min_value=datetime.datetime(2022, 1, 1),
                             max_value=datetime.datetime(2022, 4, 6),
                             value=datetime.datetime(2022, 4, 6), ).strftime('%d-%m-%Y')

st.sidebar.markdown( '''___''')

# IV) Seleção multiplas
traffic_options = (st.sidebar
                     .multiselect( 
                            'Quais as condições do transito',
                            ['Low', 'Medium', 'High', 'Jam'],
                            default=['Low', 'Medium', 'High', 'Jam']))

st.sidebar.markdown( '''___''')
st.sidebar.markdown('## Portfólio de Projetos Marcos Paulo')

# V) Conectando os filtros a base de dados
# V.I) Filtros de data
linhas_selecionadas_filtro = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas_filtro, :]

# V.II) Filtros de transito
linhas_selecionadas_filtro = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas_filtro, :]

# b) Tela Inicial
st.markdown('# Marketplace - Visão Restaurante')
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'])

# I) VIsão Gereancial
with tab1:

    # I.I) Métricas Gerais
    with st.container():
        st.title( '1. Métricas Gerais')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
       
        # I.I.I) Entregadores Únicos na base de dados
        with col1:
            Delivery_Unico = df1.loc[:, 'Delivery_person_ID'].nunique()
            col1.metric( 'Entregadores', Delivery_Unico)

        # I.I.II) Distância Média dos Restaurantes e dos Locais de Entrega
        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric( 'Distância Média Entregadores', avg_distance)

        # I.I.III) Tempo médio de entrega (durante o festival)
        with col3:
            avg_time_festival = avg_std_time_delivery(df1,'Yes', 'avg_time')
            col3.metric( 'avg Entrega Festival', avg_time_festival)

        # I.I.IV) O desvio padrão das entregas (durante o festival)
        with col4:
            std_time_festival = avg_std_time_delivery(df1,'Yes', 'std_time')
            col4.metric( 'std Entrega Festival', std_time_festival)

        # I.I.V) O tempo médio das entrega (sem o festival)
        with col5:
            avg_time_festival = avg_std_time_delivery(df1,'No', 'avg_time')
            col5.metric( 'avg Entrega', avg_time_festival)
        
        # I.I.VI) O desvio padrão das entrega (sem o festival)
        with col6:
            std_time_festival = avg_std_time_delivery(df1,'No', 'std_time')
            col6.metric( 'std Entrega', std_time_festival)

    # I.II) Tempo Médio de Entrega
    with st.container():
        st.markdown( '''___''')
        st.title( '2. Tempo Médio de Entrega')
        col1, col2 = st.columns(2)
        
        # I.II.I) Gráfico de Barras
        with col1:
            st.markdown( '##### 2.1. Tempo médio e desvio padrão por, Cidade' )
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)
        
        # I.II.II) Tabela
        with col2:
            st.markdown( '##### 2.2. Tempo médio e desvio padrão por, Cidade e Tipo de Pedido')

             # I.II.II.I) Criação da Tabela ( Não precisa de função)
            df_aux_234 = (df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']]
                             .groupby(['City', 'Type_of_order'])
                             .agg( {'Time_taken(min)': ['mean', 'std']})
                             .round(2))

            # # I.II.II.II) Organização das coluna em um nível
            df_aux_234.columns = [ 'avg_time', 'std_time']
            df_aux_234 = df_aux_234.reset_index()
            st.dataframe(df_aux_234)
    
    # I.III) Distribuição do Tempo
    with st.container():
        st.markdown( '''___''')
        st.title( '3. Distribuição de Tempo e distância por cidade')
        col1, col2 = st.columns(2)

        # I.III.I) Gráfico de Pizza
        with col1:
            st.markdown( '##### 3.1. Representatividade da distância média' )
            fig = distance(df1, fig=True)
            st.plotly_chart(fig)

        # I.III.II) Gráfico de Sunburst
        with col2:
            st.markdown( '##### 3.2. Tempo de entrega por Cidade e Densidade de Transito' )
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)
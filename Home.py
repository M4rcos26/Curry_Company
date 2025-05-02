import streamlit as st
from PIL import Image

# Tamanho da Página
st.set_page_config(
    page_title="Home",
    page_icon='🎲',
    layout="wide")

# a) Barra lateral 
    # Para colocar um elemento na barra lateral utilizamos o st.sidebar

# I) Imagem da Logo
# imagem_path = "logo.jpg"
imagem = Image.open( 'logo.jpg')
st.sidebar.image ( imagem, width=240)

st.sidebar.markdown( '# Curry Company')
st.sidebar.markdown( '## Fastest Delivery in Town')
st.sidebar.markdown( '''___''')

st.write('# Curry Company Growth Dashboard')
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
### Como utilizar esse Growth Dashboard?
- Visão Empresa:
    - Visão Gerencial: Métricas gerais de comportamento.
    - Visão Tática: Indicadores semanais de crescimento.
    - Visão Geográfica: Insights de geolocalização.
- Visão Entregador:
    - Acompanhamento dos indicadores semanais de crescimento
- Visão Restaurante:
    - Indicadores semanais de crescimento dos restaurantes
### Ask for Help
- Time de Data Science no Discord
    - @MarcosPaulo

    """)
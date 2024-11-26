import streamlit as st
import pandas as pd
from dataset import df
from utils import format_number,df_entregas_municipio,Porcentagemdf1
from PIL import Image 
import plotly.express as px
import urllib.request 

# side bar logo pricipal
st.sidebar.image("dados/imagens/logoseaf.png") 
if "data" not in st.session_state:
    st.session_state["data"] = df

df = st.session_state["data"]
# pegar municipios, 

municipios = df["municipioTransferencia"].value_counts().index
muni =st.sidebar.selectbox("Municipio",municipios)
# pegar agora equipamentos, maquinas motorizada agricolas

df_maquinarios = df[df["municipioTransferencia"]==muni] 
maq = df_maquinarios["contaAtual"].value_counts().index
maq1 =st.sidebar.selectbox("Contas/Grupos equipamentos",maq)
maq1_stats = df_maquinarios[df_maquinarios["contaAtual"] == maq1].iloc[0]

equipe = df_maquinarios["descricaoCompleta"].value_counts().index
equipe1 =st.sidebar.selectbox("descrição equipamentos",equipe)
equipe_stats = df_maquinarios[df_maquinarios["descricaoCompleta"] == equipe1].iloc[0]



st.title(f"{maq1_stats['contaAtual']}")
st.markdown(f"Municipio: {maq1_stats['municipioTransferencia']}")
# st.metric('total do equipamento', format_number(maq1_stats['valorUnitario'].sum(), 'R$'))
# st.metric('total de Contas', (maq.shape[0]))
# st.metric('tolal por equipamentos',(equipe.shape[0]))


def metrics():
   from streamlit_extras.metric_cards import style_metric_cards
   col1,col2,col3,col4 =st.columns(4)
   col1.metric("Valor Total do equipamento", value=format_number(maq1_stats['valorUnitario'].sum(), 'R$'), delta="Valor Total do equipamento")
   col2.metric("Total de Contas", value=f"{(maq.shape[0])}",delta="Total de Contas")
   col3.metric('Total por equipamentos',(equipe.shape[0]),delta="Total por equipamento")
   col4.metric('Valor equipamento',value=format_number(equipe_stats['valorUnitario'], 'R$'), delta="Valor equipamento")

   style_metric_cards(background_color="#080054",border_left_color="#2a65ff")
metrics()

# st.markdown(f"## {maq1_stats['contaAtual']}")
 
# st.dataframe(Porcentagemdf) 
st.dataframe(Porcentagemdf1)

# col1,col2,col3 = st.columns(3)
# with col1:
#      st.title(f"{maq1_stats['descricaoCompleta']}")
# with col2:    
#         st.metric('total de itens', format_number(maq.shape[0]))
# with col3:
#     __path__ = "dados/imagens/escavadeira.jpg"

#     Imagem = Image.open(__path__)

# st.image(Imagem,
#          caption='escavadeira',
#          use_column_width='auto')

                 

# with tab4:
#     df1 = px.data.gapminder().query("year == 2007")

#     grafico =px.scatter_geo(df1,locations="iso_alpha", color="continent", hover_name="country", size ="pop",
#                             projection= "natural earth" ) 
#     grafico
         

# image_file = st.file_uploader("Carregue uma foto e aplique um filtro no menu lateral", type=['jpg', 'jpeg', 'png'])

# if image_file:
#     user_image = Image.open(image_file)
#     st.sidebar.text("Imagem Original")
#     st.sidebar.image(user_image, width=150)
# else:
#     user_image = Image.open('dados/imagens/escavadeira.jpg')

import streamlit as st
import plotly.express as px
from dataset import df
from utils import format_number,Porcentagemdf
from graficos import grafico_rec_mensal, grafico_rec_categoria, grafico_entregas_municipio, grafico_QTDEnt_municipio

    
             
 
st.set_page_config(layout='wide') 
st.title("Dashboard de Entregas :shopping_trolley:")
page_icon="🚜",
# side bar logo pricipal
st.sidebar.image("dados/imagens/logoseaf.png")

st.markdown("""<h3 style="color:#002b50;">DASHBOARDS SIGPAT SEAF(PATRIMÔNIO)</h3>""",unsafe_allow_html=True)
#chamar css style 
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

# usando sidebar (menu lateral para inserir filtros)
st.sidebar.title('Filtro por Municípos')

filtro_municipio = st.sidebar.multiselect( 
    'Municipios',
    df['municipioTransferencia'].unique()

)
if filtro_municipio:
   Porcentagemdf = df[df['municipioTransferencia'].isin(filtro_municipio)]


# st.sidebar.title('Filtro por Entregas')

# st.sidebar.title('Filtro por grupo de Maquinarios')


aba1, aba2, aba3 = st.tabs(['Dataset', 'Valor total invetário','Entregas Municipio'])
with aba1:
    st.dataframe(Porcentagemdf)

with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('total do equipamento', format_number(Porcentagemdf['valorUnitario'].sum(), 'R$'))

    with coluna2:
        st.metric('total de itens', format_number(Porcentagemdf.shape[0]))
        st.plotly_chart(grafico_rec_mensal, use_container_width= True)
        st.plotly_chart(grafico_rec_categoria, use_container_width= True)
        
with aba3:
    coluna1,coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(grafico_entregas_municipio)
    with coluna2: 
        st.plotly_chart(grafico_QTDEnt_municipio)


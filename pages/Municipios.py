import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
from utils import format_number,df_entregas_municipio,Porcentagemdf1,df_entregas_municipio1
import plotly.express as px
from dataset import df

st.set_page_config(
page_title="Entregas Agricultura Familiar",
page_icon="🚜",
layout="wide"

)
# side bar logo pricipal
st.sidebar.image("dados/imagens/logoseaf.png")
# pegara uma session no cache para diminuir processamento
if "data" not in st.session_state:
    st.session_state["data"] = df

df = st.session_state["data"]

municipios = df["municipioTransferencia"].value_counts().index
muni =st.sidebar.selectbox("Municipio",municipios)

# filtrar todos veiculos estao no municipio por conta atual 

df_filtred = df[df["municipioTransferencia"] == muni].set_index("contaAtual")
# df_filtred = df2_contascontabeis2 [df2_contascontabeis2 ["municipioTransferencia"] == muni].set_index("codigoConta")

st.markdown(f"## {muni}")


columns = ["numeroPatrimonio","valorUnitario","codigoConta","descricaoMaterial",
"dataInclusao","destinoTransferencia","municipioTransferencia","descricao","descricaoCompleta"]

# formular parametros de maneira especial usando coluns_confi , inserindo dicionario do python, a coluna a modificars

st.dataframe(df_filtred[columns],
             column_config={
                 "valorUnitario": st.column_config.ProgressColumn("valorUnitario", format="R$ %.2f",min_value=10000, max_value=1000000),
                #  "valorUnitario": st.column_config.NumberColumn()
             }, height=1000)


st.dataframe(Porcentagemdf1)
st.dataframe(df_entregas_municipio)
st.dataframe(df_entregas_municipio1)

# treemap=df_entregas_municipio1[["municipioTransferencia","contaAtual","count"]].groupby(by= ["municipioTransferencia","contaAtual"])["count"].sum().reset_index
grafico_entregas_municipioTree= px.treemap(df_filtred,path= ["municipioTransferencia","descricaoSubGrupo","descricaoCompleta"], values = "valorUnitario",hover_data = ["destinoTransferencia"],
                                           color= "descricao",height=700, width=600) 
                                           
grafico_entregas_municipioTree.update_layout(width = 800, height = 650,margin = dict(t=50, l=25, r=25, b=25))
grafico_entregas_municipioTree.update_traces(root_color="black",marker=dict(cornerradius=25))

st.plotly_chart(grafico_entregas_municipioTree)    


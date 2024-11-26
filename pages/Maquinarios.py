import streamlit as st
from dataset import df
import plotly.express as px
import pandas as pd
from utils import convert_csv, mensagem_sucesso, df_rec_mensal, df_rec_Categoria, df_entregas_municipio,format_number
from PIL import Image 
import altair as alt
import numpy as num
import matplotlib.pyplot as plt
import seaborn as sns

# side bar logo pricipal
st.sidebar.image("dados/imagens/logoseaf.png")
st.title('Todos bens  / Graficos')

with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as colunas',
        list(df.columns),
        list(df.columns)
               
    )
    # substitui campo contaAtual por descricaoCompleta

st.sidebar.title('filtros')   
with st.sidebar.expander('Conta Atual'):
    conta = st.multiselect(
        'Selecione os equipamentos',
        df['contaAtual'].unique(),
        df['contaAtual'].unique()

    )

with st.sidebar.expander('Equipamento'):
    equipamentos = st.multiselect(
        'Selecione os equipamentos',
        df['descricaoCompleta'].unique(),
         df['descricaoCompleta'].unique()
    )
with st.sidebar.expander('Valor Unitário'):
    valor = st.slider(
        'Selecione o Valor', 0.0, 5000000.0, (25.0, 75.0)
       
    )

with st.sidebar.expander('Data inclusão'):
    
    data_inclusao = st.date_input(
        'selecione a data',
        (df['dataInclusao'].min(),
        df['dataInclusao'].max())

    )
with st.sidebar.expander('Município'):
    
    municipio = st.multiselect(
        'Selecione Municípios',
        df['municipioTransferencia'].unique(),
        # df['municipioTransferencia'].unique()
    
    )

with st.sidebar.expander('Status do Bem'):
    
    status = st.multiselect(
        'Selecione tipo do status do bem',
        df['status'].unique(),
        df['status'].unique(),
     
    )
query = ''' 
    `contaAtual` in @conta and \
    `descricaoCompleta` in @equipamentos and \
    @valor[0] <= valorUnitario  <= @valor[1] and \
    @data_inclusao[0] <= `dataInclusao` <= @data_inclusao[1] and \
    `municipioTransferencia` in @municipio and \
    `status` in @status
    
'''

filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]

st.dataframe(filtro_dados)

# coletar numero de linhas que tem dentro do dataframe com uso do f string
st.markdown(f'A tabela possui :blue[{filtro_dados.shape[0]}]  linhas e :blue[{filtro_dados.shape[1]}] colunas')

st.markdown('Nome do arquivo')

coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input(
        'Nome',
        label_visibility='hidden'
    )
    nome_arquivo+= '.csv'
with coluna2:
    st.download_button(
        'Baixar arquivo',
        data=convert_csv(filtro_dados),
        file_name=nome_arquivo,
        mime='text/csv',
        on_click= mensagem_sucesso
    )

# st.metric('total do equipamento', format_number(filtro_dados['valorUnitario'].sum(), 'R$'))
# st.metric('total de itens', format_number(filtro_dados.shape[0]))

contagem_linhas = len(filtro_dados.index)
# começando criando outras 32 colunas  



def metrics():
   from streamlit_extras.metric_cards import style_metric_cards
   col1,col2,col3=st.columns(3)
   col1.metric("Total Itens", value=filtro_dados.shape[0], delta="Total Itens")
   col2.metric("Total valor municipio", value=f"{filtro_dados.valorUnitario.sum():,.0f}", delta="Total valor municipio")

   style_metric_cards(background_color="#071021",border_left_color="#2a66af")

# metrics()   

#pie chart
div1, div2=st.columns(2)
def pie():
    with div1:
        theme_plotly=None
        fig=px.pie(filtro_dados,values="valorUnitario",names="descricaoCompleta", title= "Município e valor")
        fig.update_layout(legend_title="Descricao", legend_y=0.9)
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig,use_container_width=True,theme=theme_plotly)
# pie()


#bar chart

def bar():
    with div2: 
        theme_plotly=None
        fig=px.bar(filtro_dados, y="valorUnitario", x="descricaoCompleta", text_auto='.2s',title="Grafico valor e equipamento")
        fig.update_traces(textfont_size=18,textangle=0,textposition="outside",cliponaxis=False)
        st.plotly_chart(fig,use_container_width=True,theme=theme_plotly)
# bar()        

def table():
    with st.expander("Tabela"):
     shwdata=st.multiselect("Filtar tabela",filtro_dados.columns,default=["numeroPatrimonio","valorUnitario","codigoConta","contaAtual","descricaoMaterial",
     "dataInclusao","destinoTransferencia","municipioTransferencia","descricao"])
     st.dataframe(filtro_dados[shwdata],use_container_width=True)
# table()    
b1,b2 =st.columns(2)
#dot plot
with b1:
    st.subheader("Equipamentos e valor unitarios", divider="rainbow")
    source=filtro_dados
    chart=alt.Chart(source).mark_circle().encode(
       x="descricaoCompleta",
       y="valorUnitario",
       color="contaAtual" 
    ).interactive()
    # st.altair_chart(chart,theme="streamlit",use_container_width=True )
with b2:
    st.subheader("Equipamentos e valor total", divider="rainbow") 
    energy_source=pd.DataFrame({
        "descricao Completa": filtro_dados["descricaoCompleta"],
        "valor Unitario (R$)": filtro_dados["valorUnitario"],
        "Data": filtro_dados["dataInclusao"]
    })
    bar_chart=alt.Chart(energy_source).mark_bar().encode(
        x="year(Data):O",
        y="sum(valor Unitario (R$)):Q",
        color ="descricao Completa:N"
    )
    # st.altair_chart(bar_chart,use_container_width=True)

c1,c2=st.columns(2)
with c1:
    st.subheader("Equipamentos e valor total", divider="rainbow") 
    feature_x=st.selectbox("Selicione eixo X, Dados Qualitativos",filtro_dados.select_dtypes("object").columns)
    feature_y=st.selectbox("Selicione eixo Y, Dados Quantitativos",filtro_dados.select_dtypes("number").columns)
    fig, ax=plt.subplots()
    sns.scatterplot(data=filtro_dados,x=feature_x,y=feature_y,hue=filtro_dados.descricaoCompleta, ax=ax)
    st.pyplot(fig)
with c2:
    st.subheader("Equipamentos por Frequencia", divider='rainbow',)
    feature=st.selectbox('Selecione apenas dados Qualitativos', filtro_dados.select_dtypes("object").columns)
    fig1,ax=plt.subplots()
    ax.hist(filtro_dados[feature],bins=20) 
    ax.set_title(f'histograma de {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frequencia')
    st.pyplot(fig1)

#passar filtro agrupados descricao completa 
filtro_dados1= filtro_dados[["descricaoCompleta","valorUnitario"]].groupby(by="descricaoCompleta")["valorUnitario"].sum()


#side navigation
from streamlit_option_menu import option_menu
with st.sidebar:
    selected= option_menu(
        menu_title="Menu",
        options=["Gráficos","Tabela Minimizada"],
        icons=["house", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )
if selected=="Gráficos":
    pie()
    bar()
    metrics()
    st.altair_chart(chart,theme="streamlit",use_container_width=True )
    st.altair_chart(bar_chart,use_container_width=True)
    # st.pyplot(fig)
    

if selected=="Tabela Minimizada":
     table()
# filtro_dados.describe().T







# ate 08/09   
# col1, col2 = st.columns((2))
# df["dataInclusao"] = pd.to_datetime(df["dataInclusao"])
# startDate = pd.to_datetime(df["dataInclusao"]).min()
# endDate = pd.to_datetime(df["dataInclusao"]).max()

# with col1:
#     date1 = pd.to_datetime(st.date_input("Data inicial:", startDate))
                           
# with col2:
   
#     date2 = pd.to_datetime(st.date_input("Data final:", endDate))                                                     

# df = df[(df["dataInclusao"]>= date1) & (df["dataInclusao"] <= date2)].copy()
# filtroGraf_df = df
# filtroGraf_df = filtroGraf_df.groupby(by = ["municipioTransferencia"], as_index = False)["valorUnitario"].sum()
# filtroGraf1_df = df
# filtroGraf1_df = filtroGraf1_df.groupby(by = ["municipioTransferencia"], as_index = False)["descricaoCompleta"].sum()

# with col1:
#     st.subheader("Municípios por valor ")
#     fig = px.bar(filtroGraf_df, x= "municipioTransferencia", y= "valorUnitario", text= ['${:,.2f}'.format(x) for x in filtroGraf_df["valorUnitario"]],
#                  template = "seaborn")
#     st.plotly_chart(fig, use_container_width= True, height = 200)

# with col2:
#     st.subheader("Municipio por equipamentos")  
#     fig = px.pie(filtroGraf1_df, values = "municipioTransferencia", names = "descricaoCompleta")
#     fig.update_traces(text = filtroGraf1_df["municipioTransferencia"],textposition = "outside")
#     st.plotly_chart(fig, use_container_width = True) 

# __path__ = "dados/imagens/escavadeira.jpg"
# Imagem = Image.open(__path__)

# st.image(Imagem,
#          caption='escavadeira',
#          use_column_width='auto')

# __path__ = "dados/imagens/caminhao 12.jpg"
# Imagem = Image.open(__path__)

# st.image(Imagem,
#          caption='Caminhão 12M',
#          use_column_width='auto')
# st.metric('total de itens', format_number(filtro_dados.shape[0]))
# ate 08/09  



























# grafico_entregas_municipio = px.bar(
#     df_entregas_municipio[['sum']].sort_values('sum', ascending= False).head(150),
#     x= 'sum',
#     y= df_entregas_municipio[['sum']].sort_values('sum', ascending= False).head(150).index,
#     text_auto= True,
#     title= 'Valor total Entregas Municipio'

# )



# grafico_QTDEnt_municipio = px.bar(
#     df_entregas_municipio[['count']].sort_values('count', ascending= False).head(150),
#     x= 'count',
#     y= df_entregas_municipio[['count']].sort_values('count', ascending= False).head(150).index,
#     text_auto= True,
#     title= 'Quantidade de entregas por Municipio'
# )    



# st.plotly_chart(grafico_QTDEnt_municipio)
# st.plotly_chart(grafico_entregas_municipio)


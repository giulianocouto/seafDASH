import streamlit as st
from dataset import df
import plotly.express as px
from utils import convert_csv, mensagem_sucesso

st.title('Estoque Geral (para exportar .CSV) por Município')
# side bar logo pricipal
st.sidebar.image("dados/imagens/logoseaf.png")

with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as colunas',
        list(df.columns),
        list(df.columns)
               
        )
    
st.sidebar.title('filtros')    
with st.sidebar.expander('Grupo Equipamentos(Conta atual)'):
    equipamentos = st.multiselect(
        'Selecione os equipamentos',
        df['contaAtual'].unique(),
        df['contaAtual'].unique()

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
        default=df['municipioTransferencia'].unique()
        )       

query = '''
    `contaAtual` in @equipamentos and \
    @valor[0] <= valorUnitario  <= @valor[1] and \
    @data_inclusao[0] <= `dataInclusao` <= @data_inclusao[1] and \
    `municipioTransferencia` in @municipio
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





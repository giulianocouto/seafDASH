from dataset import df
import pandas as pd
from datetime import datetime
import streamlit as st
import time



def format_number(value, prefix = ''):
    for unit in ['', 'Mil']:
        if value < 1000:
            return f'{prefix} {value:.3f} {unit}'
        value /= 100000
    return f'{prefix} {value:.3f} Milhões '


# def format_number(value, prefix = ''):
#     for unit in ['', 'mil']:
#         if value < 1000:
#             return f'{prefix} {value:.3f} {unit}'
#         value /= 10000
#     return f'{prefix} {value:.3f} milhões'


df_rec_municipio = df.groupby('municipioTransferencia')[['valorUnitario']].sum()
# df_rec_municipio = df.drop_duplicates(subset='municipioTransferencia')[['municipioTransferencia']].merge(df_rec_municipio, left_on='municipioTransferencia', right_index=True).sort_values('valorUnitario',ascending=False)

# print(df_rec_municipio.head(10))


# funcionando 
# df_rec_anual = df.groupby('dataAquisicao')['valorUnitario'].sum()
# print(df_rec_anual)



# funcionando agrupado por ano e gastos
# df_rec_anual =df.groupby(pd.Grouper(key='dataInclusao', freq='YE', origin=pd.to_datetime('2021-01-10')),dropna=True).sum()
# df_rec_anual['Ano'] = df_rec_anual['dataAquisicao'].dt.year
# print(df_rec_anual)

# funcionando agrupado por mes e gastos
# df_rec_mensal =df.groupby(pd.Grouper(key='dataInclusao', freq='ME', origin=pd.to_datetime('2021-01-10')),dropna=True).sum()


# funcionando agrupado por ano mostrando nome do ano e gastos
# df['Ano'] = pd.to_datetime(df['dataInclusao'], format='%ye').dt.year

# df_rec_anual = df.groupby('dataAquisicao')['valorUnitario'].sum()
# df_rec_anual['Ano'] = pd.to_datetime(df['dataInclusao'], format='%ye').dt.year
# print(df_rec_anual['Ano'])

# funcionando agrupado por mes mostrando nome do mes e gastos
# df['Mes'] = pd.to_datetime(df['dataInclusao'], format='%me').dt.month_name().str.slice(stop=3)

# df_rec_mensal = df.groupby('dataAquisicao')['valorUnitario'].sum()
# df_rec_mensal['Mes'] = pd.to_datetime(df['dataInclusao'], format='%me').dt.month_name().str.slice(stop=3)
# print(df_rec_mensal['Mes'])


# # agrupado por mes mostrando nome do mes e gastos
# df_rec_mensal = df.set_index('dataAquisicao').groupby(pd.Grouper(freq='Me'))['valorUnitario'].sum().reset_index()



df_rec_mensal = df.groupby(['dataAquisicao'])['valorUnitario'].sum().reset_index()
df_rec_mensal['Ano'] = pd.to_datetime(df['dataInclusao'], format='%YE').dt.year
df_rec_mensal['Mes'] = pd.to_datetime(df['dataInclusao'], format='%ME').dt.month_name().str.slice(stop=3)
# print(df_rec_mensal)
# df_rec_mensal

# 3 - dataframe Receita por Estado

df_rec_Categoria = df.groupby('contaAtual')[['valorUnitario']].sum().sort_values('valorUnitario', ascending=False)
# print(df_rec_Categoria.head())

# funcionando agrupado por semana e gastos
# df_rec_semanal =df.groupby(pd.Grouper(key='dataInclusao', freq='W')).sum()
# print(df_rec_semanal)

# funcionando procurando por string
# df[df['codigoEntrada'] =='0']
# print(df)

# 3 - dataframe Entregas Municipio (contagens com agregação )

# df_entregas_municipio1 = df.groupby('municipioTransferencia')[['contaAtual','valorUnitario']].agg(['sum', 'count'])
# df_entregas_municipio1=pd.DataFrame(df.groupby('municipioTransferencia')[['contaAtual','valorUnitario']].agg(['sum','count']))
df_entregas_municipio = pd.DataFrame(df.groupby('municipioTransferencia')['valorUnitario'].agg(['sum','count']))
df_entregas_municipio1 =pd.DataFrame(df.groupby(['municipioTransferencia']).agg({"valorUnitario": st.column_config.ProgressColumn("valorUnitario", format="R$ %.2f",min_value=10000, max_value=10000000),'contaAtual':'count','valorUnitario':'sum'})/142).reset_index()
# df_entregas_municipio1 =pd.DataFrame(df.groupby(['municipioTransferencia']).agg({"valorUnitario": st.column_config.ProgressColumn("valorUnitario", format="R$ %.2f",min_value=10000, max_value=10000000),'contaAtual':'count','valorUnitario':'sum'})/142).reset_index()

# print(df_entregas_municipio1)

# df_entregas_municipio2=len(df[df['municipioTransferencia']== 'ACORIZAL'])

df1_contascontabeis = pd.DataFrame(df.groupby('contaAtual')['valorUnitario'].agg(['sum','count']))


Porcentagemdf =  pd.DataFrame(df['valorUnitario'] / df.groupby('municipioTransferencia')['valorUnitario'].transform('sum'))
Porcentagemdf1 = df.groupby(['municipioTransferencia', 'contaAtual','descricaoCompleta']).size().reset_index()
# print(Porcentagemdf1.head(150))

# df_entregas = pd.DataFrame(df.groupby(['municipioTransferencia'])['valorUnitario'].sum().reset_index())

# print(Porcentagemdf)

#  funcao para converter arq .csv 

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')
def mensagem_sucesso():
    success = st.success(
        'Arquivo baixado com sucesso',
        icon="🚜"
        )
    time.sleep(3)
    success.empty()


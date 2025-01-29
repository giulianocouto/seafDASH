import json
import requests, os , sys
import pandas as pd
import streamlit as st
# from utils import format_number

def load_data():
    # response = requests.get('https://servicos.seplag.mt.gov.br/apisigpatseaf/inventario/listarTodos/3a46beefb6997be4a7230a92c7ba5e041ef1d017')
    response = requests.get('https://servicos.seplag.mt.gov.br/apisigpatseaf/inventario/listarTodosCustomizado/3a46beefb6997be4a7230a92c7ba5e041ef1d017')

    data = response.json()
    return pd.DataFrame(data)
    
#  carregar dados
data = load_data()
df = data
st.table(df.head(10))

# pegar dic response.json()'
#  pegar dados json todos geral

# file = open('dados/sigpattodos.json', encoding="utf8")
# data = json.load(file)
# df = pd.DataFrame.from_dict(data)


#  pegar dados json contaAtual
file1 = open('dados/sigpatcontaRel.json', encoding="utf8")
data1 = json.load(file1)

df1 = pd.DataFrame.from_dict(data1)
df['dataInclusao'] = pd.to_datetime(df['dataInclusao'], format='%Y-%m-%d', dayfirst= True)

# file.close()

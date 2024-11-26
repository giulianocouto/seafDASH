import json
#import requests
import pandas as pd

# maquinario = requests.get('https://servicos.seplag.mt.gov.br/apisigpatseaf/inventario/listarTodos/3a46beefb6997be4a7230a92c7ba5e041ef1d017')
# maquinario = maquinario.json()
# # print(maquinario)

# maquinario_trator = maquinario['listaViewInventario']
# print(maquinario_trator)

#  pegar dados json todos geral
file = open('dados/sigpattodos.json', encoding="utf8")
data = json.load(file)


df = pd.DataFrame.from_dict(data)


#  pegar dados json contaAtual
file1 = open('dados/sigpatcontaRel.json', encoding="utf8")
data1 = json.load(file1)

df1 = pd.DataFrame.from_dict(data1)


# list(df.columns.values)

# print(df['listaViewInventario'].to_string(index=False))

# df['dataInclusao'] = pd.to_datetime(df['dataInclusao'])


df['dataInclusao'] = pd.to_datetime(df['dataInclusao'], format='%Y-%m-%d', dayfirst= True)

# type(df['dataInclusao'][0])
df
# print(df)

file.close()

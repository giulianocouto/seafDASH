import plotly.express as px
from utils import  format_number,df_rec_mensal, df_rec_Categoria, df_entregas_municipio,Porcentagemdf
from dataset import df

#grafico_map_municipio = px.scatter_geo
# grafico_rec_mensal = px.line(
#   df_rec_anual,
#   x='Ano',
#   y='valorUnitario',
#   markers= True,
#   range_y=(0,df_rec_anual.max()),
#   color='Ano',
#   line_dash= 'Ano'


# )
# pegar os ultimo registros usar o tiel, pegar os primeiros usar o head
grafico_rec_mensal = px.line(
    df_rec_mensal,
    x ='Mes',
    y ='valorUnitario',
    markers = True,
    range_x = (0, df_rec_mensal.max()),
    color= 'Ano',
    line_dash ='Ano',
    title = 'receita mensal'
)
grafico_rec_mensal.update_layout(yaxis_title = 'Receita')


grafico_rec_categoria = px.bar(
    df_rec_Categoria.head(18),
    text_auto= True,
    title= 'Categoria Equipamentos Seaf',

)

grafico_entregas_municipio = px.bar(
    df_entregas_municipio[['sum']].sort_values('sum', ascending= False).head(150),
    x= 'sum',
    y= df_entregas_municipio[['sum']].sort_values('sum', ascending= False).head(150).index,
    text_auto= True,
    title= 'Valor total Entregas Municipio'

)
grafico_QTDEnt_municipio = px.bar(
    df_entregas_municipio[['count']].sort_values('count', ascending= False).head(150),
    x= 'count',
    y= df_entregas_municipio[['count']].sort_values('count', ascending= False).head(150).index,
    text_auto= True,
    title= 'Quantidade de entregas por Municipio'

)

# grafico_QTDEnt_municipioPercent = px.bar(
#     Porcentagemdf[['marca']].sort_values('sum', ascending= False).head(150),
#     x= 'sum',
#     y= Porcentagemdf[['marca']].sort_values('sum', ascending= False).head(150).index,
#     text_auto= True,
#     title= 'Quantidade de entregas por Municipio Percent'

# )



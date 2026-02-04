import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Sustentabilidade dos Países", layout="wide")
st.title("Monitor de Emisões de CO2 Global")
st.markdown("Análise de emissões de carbono ao longo dos anos.")

def carregar_dados():
    df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
    return df

df = carregar_dados()
df = df.rename(columns={'year': 'Ano', 'country': 'País', 'iso_code': 'sigla'})
df = df.rename(columns={'oil_co2': 'Óleo', 'gas_co2': 'Gás Natural', 'coal_co2': 'Carvão', 'cement_co2': 'Produção de Materiais para Construção Civil (Cal, Cimento, etc.)', 'flaring_co2': 'Flaring (Chaminés Petrolíferas)'})

st.sidebar.header("Filtros")
Estado = st.sidebar.multiselect("Selecione os Países", options=df['País'].unique(), default=["Brazil", "United States", "China"])

ano_min, ano_max = int(df['Ano'].min()), int(df['Ano'].max())
periodo = st.sidebar.slider("Período", ano_min, ano_max, (1750, 2024))

df_filtrado = df[(df["País"].isin(Estado)) & (df['Ano'].between(periodo[0], periodo[1]))]

fig = px.line(df_filtrado, x='Ano', y='co2', color='País', title='Emissões de CO2 (em milhões de toneladas)', labels={'co2': "CO2 em Toneladas", 'Ano': 'Ano'})

st.plotly_chart(fig, use_container_width=True)

st.subheader("Estatísticas Rápidas")
col1, col2 = st.columns(2)
with col1:
  total_co2 = df_filtrado['co2'].sum()
  st.metric("Total de CO2 no período", f"{total_co2:,.2f} Mt")

ano_atual = df['Ano'].max()
df_mapa = df[df['Ano'] == ano_atual]

fig_mapa = px.choropleth(df_mapa, locations='sigla', color='co2', hover_name='País', title=f'Emissões de CO2 por País em {ano_atual}', color_continuous_scale=px.colors.sequential.Reds)
st.plotly_chart(fig_mapa, use_container_width=True)

st.subheader("Fontes de Emissão")
fontes = ['Carvão', 'Gás Natural', 'Óleo', 'Flaring (Chaminés Petrolíferas)', 'Produção de Materiais para Construção Civil (Cal, Cimento, etc.)']
dado_recente_pais = df_filtrado[df_filtrado['País'] == Estado[0]].iloc[-1]

valores = dado_recente_pais[fontes].fillna(0)
fig_pizza = px.pie(names=fontes, values=valores, title=f"Origem do CO2: {Estado[0]}", hole = 0.3)
st.plotly_chart(fig_pizza)
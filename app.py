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

st.sidebar.header("Filtros")
Estado = st.sidebar.multiselect("Selecione os Países", options=df['country'].unique(), default=["Brazil", "United States", "China"])

ano_min, ano_max = int(df['year'].min()), int(df['year'].max())
periodo = st.sidebar.slider("Período", ano_min, ano_max, (1750, 2024))

df_filtrado = df[(df["country"].isin(Estado)) & (df['year'].between(periodo[0], periodo[1]))]

fig = px.line(df_filtrado, x='year', y='co2', color='country', title='Emissões de CO2 (em milhões de toneladas)', labels={'co2': "CO2 em Toneladas", 'year': "Ano"})

st.plotly_chart(fig, use_container_width=True)

st.subheader("Estatísticas Rápidas")
col1, col2 = st.columns(2)
with col1:
  total_co2 = df_filtrado['co2'].sum()
  st.metric("Total de CO2 no período", f"{total_co2:,.2f} Mt")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
from io import BytesIO

# Inicializar a variável de estado
if 'mostrar_grafico_total' not in st.session_state:
    st.session_state.mostrar_grafico_total = False

# Load the data
file_path = "marcas.xlsx"
df = pd.read_excel(file_path, sheet_name="Planilha1")

# Adjust the data
colunas_esperadas = ["Grupo", "Subgrupo", "Online", "Offline", "Nunca tocou", "Total"]
df.columns = colunas_esperadas
df["Subgrupo"] = df["Subgrupo"].replace("nan", pd.NA)

# Create filters
st.sidebar.header("Filters")
subgrupo_selecionado = st.sidebar.selectbox("Select a Subgroup", ["All"] + df["Subgrupo"].dropna().unique().tolist())

# Filter data based on selected Subgrupo
if subgrupo_selecionado != "All":
    df_filtered = df[df["Subgrupo"] == subgrupo_selecionado]

st.title("Saúde das Marcas")
st.dataframe(df)

# Botão para mostrar/esconder o gráfico total
if st.button("Mostrar/Esconder Distribuição Total de Lojas"):
    st.session_state.mostrar_grafico_total = not st.session_state.mostrar_grafico_total

if st.session_state.mostrar_grafico_total:
    # Calcular a soma de cada categoria para todas as lojas
    total_online = df['Online'].sum()
    total_offline = df['Offline'].sum()
    total_nunca_tocou = df['Nunca tocou'].sum()

    # Criar o gráfico de pizza com a soma de todas as lojas
    labels = ['Online', 'Offline', 'Nunca tocou']
    values = [total_online, total_offline, total_nunca_tocou]

    # Define color map
    color_map = {
        'Online': 'blue',
        'Offline': 'red',
        'Nunca tocou': 'yellow'
    }
    colors = [color_map[label] for label in labels]

    fig = go.Figure(data=[go.Pie(labels=labels,
                                  values=values,
                                  textinfo='label+percent',
                                  insidetextorientation='radial',
                                  marker=dict(colors=colors)
                                  )])
    fig.update_layout(title_text="Distribuição Total de Lojas")
    st.plotly_chart(fig)

# Verificar se um subgrupo foi selecionado
if subgrupo_selecionado != "All":
    # Prepare data for pie charts
    df_pie = df_filtered.groupby('Subgrupo').agg({
        'Online': 'sum',
        'Offline': 'sum',
        'Nunca tocou': 'sum',
        'Total': 'sum'
    }).reset_index()

    # Function to generate pie chart with Plotly
    def create_pie_chart(data, title):
        labels = ['Online', 'Offline', 'Nunca tocou']
        values = data[['Online', 'Offline', 'Nunca tocou']].values.tolist()

        # Define color map
        color_map = {
            'Online': 'blue',
            'Offline': 'red',
            'Nunca tocou': 'yellow'
        }

        # Filter out labels with 0% values, but keep the original order
        filtered_labels = [label for label in labels if data[label] > 0]
        filtered_values = [data[label] for label in labels if data[label] > 0]
        colors = [color_map[label] for label in filtered_labels]

        fig = go.Figure(data=[go.Pie(labels=filtered_labels,
                                      values=filtered_values,
                                      textinfo='label+percent',
                                      insidetextorientation='radial',
                                      marker=dict(colors=colors)
                                      )])
        fig.update_layout(title_text=title)
        return fig

    # Create and display pie charts for each Subgrupo
    for index, row in df_pie.iterrows():
        st.plotly_chart(create_pie_chart(row, f"Loja {row['Subgrupo']}"))

    # Download pie charts as PDF
    def download_pdf(data):
        pdf_buffer = BytesIO()
        # ... (código para download do PDF)

    download_pdf(df_pie)
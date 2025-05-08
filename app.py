import streamlit as st
import subprocess
import pandas as pd
import os

# Caminhos dos arquivos CSV
CSV_SALVO = 'salvanoticiascrap.csv'
CSV_ANALISE = 'outputbart.csv'

st.set_page_config(page_title="Análise de Notícias Ambientais", layout="centered")
st.title("📰 Análise de Notícias Ambientais com IA")

# --- 1. INSERIR LINK DA NOTÍCIA ---
st.header("📥 Inserir Link de Notícia")

def adicionar_noticia(link):
    # Executa o Scraping.py com o link fornecido
    comando = f'python scraping.py "{link}"'
    subprocess.run(comando, shell=True)

noticia_link = st.text_input("Cole o link da matéria jornalística:")

if st.button("Adicionar Notícia"):
    if noticia_link:
        adicionar_noticia(noticia_link)
        st.success("Notícia adicionada com sucesso!")
    else:
        st.warning("Por favor, insira um link válido.")

# --- 2. EXECUTAR ANÁLISE DE SENTIMENTOS ---
st.header("🤖 Analisar Sentimentos com IA")

if st.button("Executar Análise de Sentimentos"):
    try:
        subprocess.run("python huggingfaceai.py", shell=True)
        st.success("Análise de sentimentos concluída com sucesso!")

        if os.path.exists(CSV_ANALISE):
            df_result = pd.read_csv(CSV_ANALISE, names=["Texto", "Polaridade"], header=None)
            st.dataframe(df_result.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao executar a análise: {e}")

# --- 3. GERAR GRÁFICOS ---
st.header("📊 Gerar Gráficos")

if st.button("Gerar Gráficos"):
    try:
        subprocess.run("python geradorgraph.py", shell=True)
        st.success("Gráficos gerados com sucesso! Eles apareceram em janelas externas.")
    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {e}")

# --- 4. EXIBIR PROTOCOLO UTILIZADO ---
st.header("🔎 Protocolos Utilizados nas Notícias")

if os.path.exists(CSV_SALVO):
    df_proto = pd.read_csv(CSV_SALVO, names=["Texto", "Data", "Protocolo"], header=None)
    protocolos = df_proto[["Data", "Protocolo"]].drop_duplicates()
    st.dataframe(protocolos.reset_index(drop=True), use_container_width=True)
else:
    st.info("Nenhuma notícia adicionada ainda.")


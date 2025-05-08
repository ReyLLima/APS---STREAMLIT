import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter

# Defina o caminho do CSV
csv_path = r'C:\Users\Analista Duofy\Documents\VSCODE\APS - BART\APS---NLP\Backend\BART\outputbart.csv'

# Lista de assuntos/palavras-chave
assuntos = ['desmatamento', 'queimada', 'enchente', 'alagamento', 'seca', 'inundação', 'fogo', 'incêndio', 'tempestade', 'chuva']

def identificar_assunto(texto):
    texto = texto.lower()
    contagem = Counter({assunto: texto.count(assunto) for assunto in assuntos})
    assunto_mais_comum, freq = contagem.most_common(1)[0]
    if freq > 0:
        return assunto_mais_comum
    else:
        return 'outros'

if not os.path.exists(csv_path):
    print(f"Arquivo {csv_path} não encontrado.")
    exit(1)

try:
    # Leitura do CSV
    colunas = ['texto', 'data', 'protocolo', 'polaridade']
    df = pd.read_csv(csv_path, names=colunas, header=None, encoding='utf-8', sep=',')# Gerar coluna 'assunto' a partir do texto
    df['assunto'] = df['texto'].apply(identificar_assunto)    # Remover a coluna 'protocolo' do DataFrame para os gráficos
    if 'protocolo' in df.columns:
        df = df.drop(columns=['protocolo'])


    # Remover espaços extras e padronizar polaridade e assunto
    df['polaridade'] = df['polaridade'].astype(str).str.strip().str.lower()
    df['data'] = df['data'].astype(str).str.strip().str[:10]
    df['polaridade'] = df['polaridade'].astype(str).str.strip().str.lower()
    df['data'] = df['data'].astype(str).str.strip().str[:10]
    df['assunto'] = df['assunto'].astype(str).str.strip().str.lower()
    print(df.head())
    print('Valores únicos de polaridade:', df['polaridade'].unique())
    print('Valores únicos de assunto:', df['assunto'].unique())

    # Gráfico 1: Quantidade de notícias por data e polaridade
    contagem_data = df.groupby(['data', 'polaridade']).size().unstack(fill_value=0)
    if not contagem_data.empty:
        contagem_data.plot(kind='bar', stacked=False)
        plt.title('Quantidade de notícias por data e polaridade')
        plt.xlabel('Data')
        plt.ylabel('Quantidade de notícias')
        plt.tight_layout()
        plt.legend(title='Polaridade')
        plt.show()
    else:
        print('Não há dados para plotar o gráfico de datas.')

    # Gráfico 2: Quantidade de notícias por assunto e polaridade (apenas positivo/negativo)
    df2 = df[df['polaridade'].isin(['positivo', 'negativo'])]
    contagem_assunto = df2.groupby(['assunto', 'polaridade']).size().unstack(fill_value=0)

    # Adicionar categorias faltantes e reordenar
    todos_assuntos = assuntos + ['outros']
    contagem_assunto = contagem_assunto.reindex(todos_assuntos, fill_value=0)

    print('Contagem por assunto e polaridade:')
    print(contagem_assunto)

    if not contagem_assunto.empty:
        contagem_assunto.plot(kind='bar', stacked=False)
        plt.title('Quantidade de notícias por assunto e polaridade')
        plt.xlabel('Assunto')
        plt.ylabel('Quantidade de notícias')
        plt.tight_layout()
        plt.legend(title='Polaridade')
        plt.show()
    else:
        print('Não há dados para plotar o gráfico de assuntos.')

except Exception as e:
    print(f"Erro ao processar o arquivo: {str(e)}")

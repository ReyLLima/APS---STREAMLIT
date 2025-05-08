import re
import os
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

def analisar_sentimento_transformers(texto, classifier):
    # Passa truncation=True e max_length=512 para evitar textos longos demais
    resultado = classifier(texto, truncation=True, max_length=512)
    # Mapeia o índice para o rótulo de sentimento
    mapeamento_sentimentos = {0: "NEGATIVO", 1: "NEUTRO", 2: "POSITIVO"}
    label_idx = resultado[0]['label'].split('_')[1]
    sentimento = mapeamento_sentimentos[int(label_idx)]
    return sentimento, resultado[0]['score']

def analisar_csv_com_transformers(caminho_csv, classifier):
    """
    Lê um arquivo CSV simples (uma frase por linha, sem pontuação/score) e aplica análise de sentimento.
    """
    resultados = []
    with open(caminho_csv, mode='r', encoding='utf-8') as f:
        for linha in f:
            texto = linha.strip()
            # Ignora linhas vazias
            if not texto:
                continue
            label, score = analisar_sentimento_transformers(texto, classifier)
            resultados.append({
                'texto': texto,
                'sentimento': label,
                'score': score
            })
    return resultados

if __name__ == "__main__":
    # Pega o caminho do diretório do modelo
    model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bart_tunado'))

    # Checa se o diretório do modelo existe
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Diretório do modelo não encontrado: {model_dir}")

    # Carrega o modelo e o tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    caminho_csv = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salvanoticiascrap.csv'))
    resultados = analisar_csv_com_transformers(caminho_csv, classifier)
    for r in resultados:
        print(f"Texto: {r['texto']}\nSentimento: {r['sentimento']} (score: {r['score']:.2f})\n")

    # Salva o resultado em um novo CSV, cada linha: texto original + sentimento
    output_csv = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputbart.csv'))
    with open(output_csv, mode='w', encoding='utf-8') as f_out:
        for r in resultados:
            f_out.write(f"{r['texto']},{r['sentimento']}\n")
    print(f"Arquivo salvo com sentimento em: {output_csv}")

import requests
from bs4 import BeautifulSoup

def extrair_texto_noticia(link):
    """
    Faz o scraping do corpo da matéria jornalística a partir do link e retorna o texto limpo, a data e o protocolo.
    """
    try:
        response = requests.get(link, timeout=10)
        protocolo = response.url.split(':')[0]
        print(f"Protocolo utilizado: {protocolo.upper()}")
        response.raise_for_status()
    except Exception as e:
        print(f"Erro ao acessar o link: {e}")
        return None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    artigo = soup.find('article')
    if artigo:
        paragrafos = artigo.find_all('p')
    else:
        paragrafos = soup.find_all('p')

    texto = ' '.join(p.get_text(strip=True) for p in paragrafos)
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = ' '.join(texto.split())  # Remove espaços duplicados
    texto = texto.replace('"', ' ')  # Remove todas as aspas duplas

    # Tenta extrair a data de publicação
    data = None
    # Procura por <time datetime="...">
    time_tag = soup.find('time')
    if time_tag:
        if time_tag.has_attr('datetime'):
            data = time_tag['datetime']
        elif time_tag.text:
            data = time_tag.text.strip()
    # Procura por meta tags comuns
    if not data:
        meta_date = soup.find('meta', {'property': 'article:published_time'})
        if meta_date and meta_date.has_attr('content'):
            data = meta_date['content'][:-15] if len(meta_date['content']) > 15 else meta_date['content']
    if not data:
        meta_date = soup.find('meta', {'name': 'pubdate'})
        if meta_date and meta_date.has_attr('content'):
            data = meta_date['content'][:-15] if len(meta_date['content']) > 15 else meta_date['content']
    if not data:
        meta_date = soup.find('meta', {'name': 'date'})
        if meta_date and meta_date.has_attr('content'):
            data = meta_date['content'][:-15] if len(meta_date['content']) > 15 else meta_date['content']
    if not data:
        meta_date = soup.find('meta', {'itemprop': 'datePublished'})
        if meta_date and meta_date.has_attr('content'):
            data = meta_date['content'][:-15] if len(meta_date['content']) > 15 else meta_date['content']

    return texto if texto else None, data, protocolo.upper()

def salvar_noticia_csv(texto, data, protocolo, caminho_csv=r"C:\Users\Analista Duofy\Documents\VSCODE\APS - BART\APS---NLP\Backend\BART\salvanoticiascrap.csv"):
    """
    Salva o texto, data e protocolo no CSV, separados por vírgula, cada campo entre aspas duplas.
    """
    if texto:
        texto_final = f'"{texto}","{data if data else ""}","{protocolo if protocolo else ""}"'
        with open(caminho_csv, 'a', encoding='utf-8') as csvfile:
            csvfile.write(texto_final + '\n')
        print("Matéria adicionada ao CSV com sucesso.")
    else:
        print("Texto vazio. Nada foi salvo.")

def main():
    while True:
        link = input("Cole o link da matéria jornalística: ")
        texto, data, protocolo = extrair_texto_noticia(link)
        if texto:
            salvar_noticia_csv(texto, data, protocolo)
        else:
            print("Não foi possível extrair o corpo da matéria.")
        continuar = input("Deseja adicionar outra notícia? (s/n): ").strip().lower()
        if continuar == 'n':
            print("Encerrando o programa.")
            break

if __name__ == "__main__":
    main() 
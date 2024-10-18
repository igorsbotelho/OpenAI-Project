from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()


client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
modelo = "gpt-4"


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            print("Oi")
            return dados
    except  IOError as e:
        print(f"O erro foi: {e}")
        
def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Error: {e}")
        

def analisa_sentimentos(produto):
    prompt_system = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """
    
    prompt_user = carrega(f"./dados/avaliacoes-{produto}.txt")
    print(f"Iniciou a análise de sentimentos do produto {produto}")

    lista_mensagens = [
        {
            "role" : "system",
            "content" : prompt_system
        },
        {
            "role": "user",
            "content": prompt_user
        }
    ]
    
    resposta = client.chat.completions.create(
        messages=lista_mensagens,
        model=modelo
    )
    
    text_reposta = resposta.choices[0].message.content
    salva(f"./dados/analise-{produto}.txt", text_reposta)

analisa_sentimentos("Sucos")
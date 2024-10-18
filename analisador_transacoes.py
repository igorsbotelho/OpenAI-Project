

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = "Set your API HERE"

client = OpenAI(api_key=api_key)
modelo = "gpt-4"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except  IOError as e:
        print(f"O erro foi: {e}")
        
def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Error: {e}")

def analisa_transacao(lista_transacoes):
    print("1. Executando a Análise")
    
    prompt_sistema = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
        Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """
    lista_mensagens = [
        {
            "role":
                "system",
            "content":
                prompt_sistema
        },
        {
            "role" : "user",
            "content" : f"Dado o CSV, onde cada linha é uma transação diferente: {lista_transacoes}. Sua resposta deve adotar o formato #Resposta (Apenas um json sem outros comentários)"
        }
    ]
    
    resposta = client.chat.completions.create(
        messages=lista_mensagens,
        model = modelo,
        temperature=0
    )
    
    conteudo = resposta.choices[0].message.content.replace("'", '"')
    print("Conteúdo:", conteudo)
    return conteudo

        
lista_de_transacoes = carrega("transacoes.csv")
resultado = analisa_transacao(lista_transacoes=lista_de_transacoes)



from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

def categorizaProduto(nome_produto, lista_categorias):
    promptSistema= f"""
            Identifique o perfil de compra para cada cliente a seguir
            
            # Formato da Saída
            cliente  - perfil do cliente em 3 palavras
    """

    resposta = cliente.chat.completions.create(
        messages=[
        {
            "role":"system",
            "content": promptSistema
        }, {
            "role" : "user",
            "content": nome_produto
            }
        ],
        model=modelo,
        temperature=0.5,
        max_tokens=200
    )
    
    return resposta.choices[0].message.content

categorias_val = input("Categorias Válidas: ")

while True:
    nome_produto = input("Nome produto: ")
    texto_resposta = categorizaProduto(nome_produto, categorias_val)    
    print(texto_resposta)

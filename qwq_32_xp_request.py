import requests
from dotenv import load_dotenv
import os
import json
import re
import time

load_dotenv()

huggingface_token = os.getenv("HUGGINGFACE_API_KEY")

headers = {
    "Authorization": f"Bearer {huggingface_token}",
    "Content-Type": "application/json"
}

def exibir_texto_animado(texto, delay=0.03):
    """Exibe o texto caractere por caractere com um efeito de animação."""
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def consultar_qwen(pergunta):
    data = {
        "model": "Qwen/QwQ-32B",
        "messages": [
            {
                "role": "user",
                "content": pergunta
            }
        ],
        "max_tokens": 500,
        "stream": False
    }

    response = requests.post(
        "https://router.huggingface.co/hf-inference/models/Qwen/QwQ-32B/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        resultado = response.json()
        
        # Extrair e separar o thinking da resposta real
        if 'choices' in resultado and len(resultado['choices']) > 0:
            conteudo = resultado['choices'][0]['message']['content']
            
            # Verificar se há um padrão de thinking
            thinking_pattern = r'(.*?)</think>\n\n(.*)'
            match = re.search(thinking_pattern, conteudo, re.DOTALL)
            
            if match:
                thinking = match.group(1).strip()
                resposta_real = match.group(2).strip()
                
                # Atualizar o conteúdo no resultado
                resultado['choices'][0]['message']['thinking'] = thinking
                resultado['choices'][0]['message']['content'] = resposta_real
                
                # Exibir o thinking de forma animada
                print("\n\n🤔 THINKING:\n")
                exibir_texto_animado(thinking)
                print("\n-----------------------\n")
                
                # Exibir a resposta de forma animada
                print("\n💬 RESPOSTA:\n")
                exibir_texto_animado(resposta_real)
                print("\n-----------------------\n")
        
        # Salvar o JSON completo em um arquivo para referência, se necessário
        with open("ultima_resposta.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
            
        print(f"\n[✓] JSON completo salvo em 'ultima_resposta.json'")
        return resultado
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return None

# Solicitar pergunta ao usuário
pergunta_usuario = input("Digite sua pergunta: ")
consultar_qwen(pergunta_usuario)

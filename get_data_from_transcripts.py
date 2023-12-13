import os
import json

count = 0

# Caminho para o diretório principal
diretorio_principal = "data/transcriptions"

# Nome do arquivo JSON de saída
arquivo_json_saida = "data/data.json"

# Inicializa a lista que conterá os dados do JSON
dados_json = []

# Itera sobre os diretórios dentro do diretório principal
for diretorio_Xi in os.listdir(diretorio_principal):
    diretorio_Xi_path = os.path.join(diretorio_principal, diretorio_Xi)

    # Verifica se é um diretório
    if os.path.isdir(diretorio_Xi_path):
        # Itera sobre os arquivos TXT dentro do diretório Xi
        for arquivo_txt in os.listdir(diretorio_Xi_path):
            arquivo_txt_path = os.path.join(diretorio_Xi_path, arquivo_txt)

            # Verifica se é um arquivo TXT
            if os.path.isfile(arquivo_txt_path) and arquivo_txt.endswith(".txt"):
                # Lê o conteúdo do arquivo TXT
                with open(arquivo_txt_path, 'r', encoding='utf-8') as arquivo:
                    # Processa as linhas do arquivo
                    for linha in arquivo:
                        if linha.startswith("Transcript: "):
                            count += 1
                            # Remove o prefixo "Transcript: " e adiciona à lista de dados
                            caption = linha[len("Transcript: "):].strip()
                            dados_json.append({
                                'caption': caption,
                                'highlight': 0,
                                'src': arquivo_txt
                            })

print(f"O numero de transcricoes processadas foi de", count)

# Salva os dados no arquivo JSON
with open(arquivo_json_saida, 'w', encoding='utf-8') as json_file:
    json.dump(dados_json, json_file, ensure_ascii=False, indent=2)

print("Processo concluído. Dados salvos em", arquivo_json_saida)
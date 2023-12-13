import os
import json
import random

count = 0

# Caminho para o diretório principal
diretorio_principal = "data/transcriptions"

# Nome dos arquivos JSON de saída
TRAIN_PATH = 'data/train.json'
DEV_PATH   = 'data/dev.json'  
TEST_PATH  = 'data/test.json' 

# Inicializa as listas que conterão os dados dos JSONs
dados_json_train = []
dados_json_dev = []
dados_json_test = []

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

                            # Determina em qual conjunto colocar os dados
                            random_number = random.uniform(0, 1)
                            if random_number < 0.8:
                                dados_json_train.append({
                                    'caption': caption,
                                    'highlight': 0,
                                    'src': arquivo_txt
                                })
                            elif random_number < 0.9:
                                dados_json_dev.append({
                                    'caption': caption,
                                    'highlight': 0,
                                    'src': arquivo_txt
                                })
                            else:
                                dados_json_test.append({
                                    'caption': caption,
                                    'highlight': 0,
                                    'src': arquivo_txt
                                })

print(f"O número de transcrições processadas foi de", count)

# Salva os dados nos arquivos JSON
with open(TRAIN_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(dados_json_train, json_file, ensure_ascii=False, indent=2)

with open(DEV_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(dados_json_dev, json_file, ensure_ascii=False, indent=2)

with open(TEST_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(dados_json_test, json_file, ensure_ascii=False, indent=2)

print("Processo concluído. Dados salvos em", TRAIN_PATH, DEV_PATH, TEST_PATH)
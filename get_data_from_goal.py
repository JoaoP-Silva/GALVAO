import json
import pandas as pd

# Ler o arquivo brutos.JSON
with open('data/goal/train.jsonl', 'r') as file:
    data = [json.loads(line) for line in file]

# Inicializar listas para cada coluna
captions = []
highlight = []
src = []
minute = []

# Iterar sobre os dados e extrair informações
total = 0
size = 0
for entry in data:
    while(total < 800):
        total += len(entry['chunks'])
        for chunk in entry['chunks']:
            captions.append(chunk['caption'])
            size += len(chunk['caption'])
            highlight.append(1)  # Preencher a coluna "highlight" com 1
            src.append('GOAL')  # Substitua pela informação desejada para a coluna "src"

print(f"O tamanho medio do trecho e de", size/total, "caracteres.")
# Criar um DataFrame do pandas
df = pd.DataFrame({
    'caption': captions,
    'highlight': highlight,
    'src': src,
})

# Ler o arquivo JSON existente
with open('data/data.json', 'r', encoding='utf-8') as json_file:
    dados_json_existente = json.load(json_file)

# Adicionar os dados do DataFrame ao final do JSON existente
dados_json_existente.extend(df.to_dict(orient='records'))

# Salvar o arquivo JSON atualizado
with open('data/data.json', 'w', encoding='utf-8') as json_file:
    json.dump(dados_json_existente, json_file, ensure_ascii=False, indent=2)

print("Dados adicionados ao arquivo data.json.")
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

# Divide os novos dados
num_rows = len(df)
train_rows = int(0.8 * num_rows)
dev_rows = int(0.1 * num_rows)


# Carrega os dados existentes
existing_train_data = pd.read_json('data/train.json')
existing_dev_data = pd.read_json('data/dev.json')
existing_test_data = pd.read_json('data/test.json')


# Adiciona os dados aos existentes
existing_train_data = existing_train_data.append(df[:train_rows], ignore_index=True)
existing_dev_data = existing_dev_data.append(df[train_rows:train_rows+dev_rows], ignore_index=True)
existing_test_data = existing_test_data.append(df[train_rows+dev_rows:], ignore_index=True)

# Salva os dados atualizados
existing_train_data.to_json('data/train.json', orient='records')
existing_dev_data.to_json('data/dev.json', orient='records')
existing_test_data.to_json('data/test.json', orient='records')
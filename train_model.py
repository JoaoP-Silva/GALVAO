import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification, BertTokenizer, AdamW

import json

# Carregar o dataset
with open('data/data.json', 'r') as f:
    data = json.load(f)

# Exemplo de preprocessamento - ajuste conforme necessário
texts = [item['caption'] for item in data]
labels = [item['highlight'] for item in data]

# Carregar o modelo pré-treinado e tokenizer
model_name = 'bert-base-uncased'
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Tokenizar os textos
tokenized_texts = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

# Criar o DataLoader
class CustomDataset(Dataset):
    def __init__(self, tokenized_texts, labels):
        self.tokenized_texts = tokenized_texts
        self.labels = torch.tensor(labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            'input_ids': self.tokenized_texts['input_ids'][idx],
            'attention_mask': self.tokenized_texts['attention_mask'][idx],
            'labels': self.labels[idx]
        }

dataset = CustomDataset(tokenized_texts, labels)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# Definir os parâmetros de treinamento
optimizer = AdamW(model.parameters(), lr=5e-5)
num_epochs = 3

# Loop de treinamento
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for batch in dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()
        optimizer.step()

    average_loss = total_loss / len(dataloader)
    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {average_loss}')

# Salvar o modelo treinado
model.save_pretrained('fine_tuned_model')
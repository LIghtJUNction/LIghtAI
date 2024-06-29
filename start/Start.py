import torch
from torch.utils.data import DataLoader
from transformers import AdamW

def train(model, train_dataset, epochs=3, batch_size=8):
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size)
    optimizer = AdamW(model.parameters(), lr=5e-5)

    model.train()
    for epoch in range(epochs):
        for batch in train_dataloader:
            optimizer.zero_grad()
            inputs = {key: value.to('cuda') for key, value in batch.items() if key != 'labels'}
            labels = batch['labels'].to('cuda')
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

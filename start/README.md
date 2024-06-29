# README

### English Version

#### Introduction

This repository contains a Python program for fine-tuning the BERT model using PyTorch. The code is modularized into different parts: data processing, model definition, training loop, and validation loop. This makes it easy to understand and extend.

#### Dependencies

Make sure you have the necessary libraries installed:

```bash
pip install torch transformers datasets
```

#### Data Processing

The data processing module loads the dataset using the `datasets` library and tokenizes it using the `BertTokenizer`.

```python
from datasets import load_dataset
from transformers import BertTokenizer

def load_and_preprocess_data(dataset_name, split):
    dataset = load_dataset(dataset_name, split=split)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding='max_length', truncation=True)
  
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    return tokenized_dataset
```

#### Model Definition

The model definition module loads the pre-trained BERT model for sequence classification.

```python
from transformers import BertForSequenceClassification

def load_model():
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    return model
```

#### Training Loop

The training loop module handles the forward pass, loss calculation, backpropagation, and parameter updates.

```python
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
```

#### Validation Loop

The validation loop module evaluates the model on the validation set.

```python
from torch.utils.data import DataLoader

def evaluate(model, eval_dataset, batch_size=8):
    eval_dataloader = DataLoader(eval_dataset, batch_size=batch_size)

    model.eval()
    total_loss = 0
    correct_predictions = 0

    with torch.no_grad():
        for batch in eval_dataloader:
            inputs = {key: value.to('cuda') for key, value in batch.items() if key != 'labels'}
            labels = batch['labels'].to('cuda')
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()

            predictions = torch.argmax(outputs.logits, dim=-1)
            correct_predictions += (predictions == labels).sum().item()

    avg_loss = total_loss / len(eval_dataloader)
    accuracy = correct_predictions / len(eval_dataset)
    print(f"Validation Loss: {avg_loss}, Accuracy: {accuracy}")

    return avg_loss, accuracy
```

#### Main Program

The main program combines the above modules to load data, train the model, and evaluate it.

```python
def main():
    train_dataset = load_and_preprocess_data('imdb', split='train[:10%]')
    eval_dataset = load_and_preprocess_data('imdb', split='test[:10%]')

    model = load_model().to('cuda')

    train(model, train_dataset, epochs=3, batch_size=8)
    evaluate(model, eval_dataset, batch_size=8)

if __name__ == "__main__":
    main()
```

### 中文版本

#### 介绍

此代码库包含一个使用PyTorch微调BERT模型的Python程序。代码被模块化为不同的部分：数据处理、模型定义、训练循环和验证循环。这使得代码易于理解和扩展。

#### 依赖

确保你已安装必要的库：

```bash
pip install torch transformers datasets
```

#### 数据处理

数据处理模块使用`datasets`库加载数据集，并使用`BertTokenizer`进行分词。

```python
from datasets import load_dataset
from transformers import BertTokenizer

def load_and_preprocess_data(dataset_name, split):
    dataset = load_dataset(dataset_name, split=split)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding='max_length', truncation=True)
  
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    return tokenized_dataset
```

#### 模型定义

模型定义模块加载用于序列分类的预训练BERT模型。

```python
from transformers import BertForSequenceClassification

def load_model():
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    return model
```

#### 训练循环

训练循环模块处理前向传播、损失计算、反向传播和参数更新。

```python
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
```

#### 验证循环

验证循环模块评估模型在验证集上的表现。

```python
from torch.utils.data import DataLoader

def evaluate(model, eval_dataset, batch_size=8):
    eval_dataloader = DataLoader(eval_dataset, batch_size=batch_size)

    model.eval()
    total_loss = 0
    correct_predictions = 0

    with torch.no_grad():
        for batch in eval_dataloader:
            inputs = {key: value.to('cuda') for key, value in batch.items() if key != 'labels'}
            labels = batch['labels'].to('cuda')
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()

            predictions = torch.argmax(outputs.logits, dim=-1)
            correct_predictions += (predictions == labels).sum().item()

    avg_loss = total_loss / len(eval_dataloader)
    accuracy = correct_predictions / len(eval_dataset)
    print(f"Validation Loss: {avg_loss}, Accuracy: {accuracy}")

    return avg_loss, accuracy
```

#### 主程序

主程序结合上述模块来加载数据、训练模型和评估模型。

```python
def main():
    train_dataset = load_and_preprocess_data('imdb', split='train[:10%]')
    eval_dataset = load_and_preprocess_data('imdb', split='test[:10%]')

    model = load_model().to('cuda')

    train(model, train_dataset, epochs=3, batch_size=8)
    evaluate(model, eval_dataset, batch_size=8)

if __name__ == "__main__":
    main()
```

### 示例

以下是如何运行整个程序的示例：

1. 安装依赖：
   ```bash
   pip install torch transformers datasets
   ```
2. 运行主程序：
   ```bash
   python main.py
   ```

这将加载IMDB数据集，微调BERT模型，并输出训练和验证的结果。

---

希望这个README文件能帮助你更好地理解和使用这个微调BERT模型的程序。如果有任何问题或建议，请随时提出！

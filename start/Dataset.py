from datasets import load_dataset
from transformers import AutoTokenizer

def load_and_preprocess_data(dataset_name, split):
    dataset = load_dataset(dataset_name, split=split)
    tokenizer = AutoTokenizer.from_pretrained('ollama/gamma2-9b')

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding='max_length', truncation=True)
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    return tokenized_dataset

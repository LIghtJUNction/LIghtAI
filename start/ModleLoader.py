from transformers import AutoModelForSequenceClassification

def load_model():
    model = AutoModelForSequenceClassification.from_pretrained('ollama/gamma2-9b', num_labels=2)
    return model

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

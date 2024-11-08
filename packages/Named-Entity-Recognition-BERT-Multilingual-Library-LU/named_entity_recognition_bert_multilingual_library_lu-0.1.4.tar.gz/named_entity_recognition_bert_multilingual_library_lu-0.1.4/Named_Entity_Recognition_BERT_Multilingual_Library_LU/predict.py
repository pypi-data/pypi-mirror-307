import torch

def predict(model, tokenizer, sentence, label_list):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predictions = torch.argmax(outputs.logits, dim=2)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    labels = [label_list[pred] for pred in predictions[0].cpu().numpy()]
    
    return list(zip(tokens, labels))

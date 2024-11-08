# model.py

from transformers import AutoModelForTokenClassification, AutoTokenizer

def initialize_model_and_tokenizer(pretrained_model_name, num_labels):
    """
    Initialize a BERT-based model and tokenizer for NER.
    """
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    model = AutoModelForTokenClassification.from_pretrained(pretrained_model_name, num_labels=num_labels)
    return model, tokenizer

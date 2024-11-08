import torch
from .data_loader import load_data, convert_to_hf_format
from .model import initialize_model_and_tokenizer
from .train import train_model, tokenize_and_align_labels
from .evaluate import compute_metrics
from .predict import predict
from .utils import get_label_mappings
from datasets import Dataset

class NERPipeline:
    def __init__(self, pretrained_model="bert-base-multilingual-cased"):
        self.pretrained_model = pretrained_model
        self.tokenizer = None
        self.model = None
        self.label_to_id = None
        self.id_to_label = None

    def prepare_data(self, train_path, val_path, test_path):
        # Load and process data
        train_sentences, train_labels = load_data(train_path)
        val_sentences, val_labels = load_data(val_path)
        test_sentences, test_labels = load_data(test_path)
        
        # Create label mappings
        self.label_to_id, self.id_to_label = get_label_mappings(
            train_labels + val_labels + test_labels
        )
        
        # Convert datasets to Hugging Face format
        train_dataset = convert_to_hf_format(train_sentences, train_labels, self.label_to_id)
        val_dataset = convert_to_hf_format(val_sentences, val_labels, self.label_to_id)
        test_dataset = convert_to_hf_format(test_sentences, test_labels, self.label_to_id)

        # Tokenize and align labels
        train_dataset = train_dataset.map(lambda x: tokenize_and_align_labels(x, self.tokenizer), batched=True)
        val_dataset = val_dataset.map(lambda x: tokenize_and_align_labels(x, self.tokenizer), batched=True)
        
        return train_dataset, val_dataset, test_dataset

    def initialize_model(self, num_labels):
        self.model, self.tokenizer = initialize_model_and_tokenizer(num_labels, self.pretrained_model)

    def train(self, train_dataset, val_dataset):
        train_model(self.model, self.tokenizer, train_dataset, val_dataset, compute_metrics)

    def predict(self, sentence):
        return predict(self.model, self.tokenizer, sentence, self.id_to_label)

    def evaluate(self, predictions, labels):
        return compute_metrics((predictions, labels), self.id_to_label)

# __init__.py

from .pipeline import NERPipeline
from .data_loader import load_data, convert_to_hf_format
from .model import initialize_model_and_tokenizer
from .train import train_model, tokenize_and_align_labels
from .evaluate import compute_metrics

__all__ = [
    "NERPipeline",
    "load_data",
    "convert_to_hf_format",
    "initialize_model_and_tokenizer",
    "train_model",
    "tokenize_and_align_labels",
    "compute_metrics",
]

def welcome_message():
    print(
        "Welcome to Named_Entity_Recognition_BERT_Multilingual_Library_LU!\n"
        "This library supports Named Entity Recognition (NER) using BERT model in multiple languages.\n"
        "Input data should follow the CoNLL format, as shown below:\n\n"
        "Example CoNLL format:\n"
        "Token1\tLabel1\n"
        "Token2\tLabel2\n\n"
        "Token3\tLabel3\n"
        "Each sentence must be separated by a blank line."
    )

welcome_message()

from datasets import Dataset

def load_data(file_path):
    sentences = []
    labels = []
    current_sentence = []
    current_labels = []
    
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == "":
                if current_sentence:
                    sentences.append(current_sentence)
                    labels.append(current_labels)
                    current_sentence = []
                    current_labels = []
            else:
                token, label = line.strip().split("\t")
                current_sentence.append(token)
                current_labels.append(label)
                
    return sentences, labels

def convert_to_hf_format(sentences, labels, label_to_id):
    return Dataset.from_dict({
        "tokens": sentences,
        "ner_tags": [[label_to_id[label] for label in label_seq] for label_seq in labels]
    })

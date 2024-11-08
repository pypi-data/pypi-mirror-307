def get_label_mappings(labels):
    label_list = sorted(set(label for label_seq in labels for label in label_seq))
    label_to_id = {label: i for i, label in enumerate(label_list)}
    id_to_label = {i: label for label, i in label_to_id.items()}
    return label_to_id, id_to_label

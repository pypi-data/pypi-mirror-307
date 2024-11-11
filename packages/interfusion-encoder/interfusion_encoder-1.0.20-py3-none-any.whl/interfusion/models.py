# interfusion/models.py

import torch
import torch.nn as nn
from transformers import AutoModel
import numpy as np


class DummyTqdm:
    def __init__(self, iterable=None, **kwargs):
        self.iterable = iterable if iterable is not None else []
        self.iterator = iter(self.iterable)
        self.desc = kwargs.get('desc', '')
        self.start_time = None
        self.end_time = None

    def __iter__(self):
        self.start_time = time.time()
        return self

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            if self.desc:
                print(f"{self.desc} completed in {total_time:.2f} seconds")
            else:
                print(f"Iteration completed in {total_time:.2f} seconds")
            raise

    def __getattr__(self, attr):
        # Return a dummy function for any other attributes
        return lambda *args, **kwargs: None

    def update(self, n=1):
        pass

    def set_description(self, desc=None, refresh=True):
        pass

    def close(self):
        pass


def get_tqdm(config):
    if not config.get('use_tqdm', True):
        return DummyTqdm
    else:
        tqdm_type = config.get('tqdm_type', 'standard')
        try:
            if tqdm_type == 'notebook':
                from tqdm.notebook import tqdm
            else:
                from tqdm import tqdm
        except ImportError:
            print("tqdm is not installed. Progress bars will be disabled.")
            return DummyTqdm
        return tqdm


class CrossEncoderModel(nn.Module):
    def __init__(self, config, candidate_feature_size=0, job_feature_size=0):
        super(CrossEncoderModel, self).__init__()
        # Load the transformer model
        self.model = AutoModel.from_pretrained(config['cross_encoder_model_name'])
        hidden_size = self.model.config.hidden_size
        self.use_sparse = config['use_sparse']

        if self.use_sparse:
            self.candidate_feature_size = candidate_feature_size
            self.job_feature_size = job_feature_size
            total_feature_size = self.candidate_feature_size + self.job_feature_size
            classifier_input_size = hidden_size * 3 + total_feature_size
        else:
            classifier_input_size = hidden_size * 3

        self.dropout = nn.Dropout(0.5)

        # Attention Mechanism to weigh token embeddings
        self.attention = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )

        # Interaction Layer to capture interactions between tokens
        self.interaction = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )

        # Enhanced multi-layer classifier with activation functions
        self.classifier = nn.Sequential(
            nn.Linear(classifier_input_size, classifier_input_size // 2),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(classifier_input_size // 2, classifier_input_size // 4),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(classifier_input_size // 4, 1)
        )

    def forward(self, input_ids, attention_mask, features=None):
        # Pass inputs through the transformer model
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state  # Shape: [batch_size, seq_length, hidden_size]

        # Apply Attention Mechanism over token embeddings
        attention_weights = self.attention(last_hidden_state).squeeze(-1)  # Shape: [batch_size, seq_length]
        attention_weights = torch.softmax(attention_weights, dim=1).unsqueeze(-1)  # Shape: [batch_size, seq_length, 1]
        weighted_embeddings = last_hidden_state * attention_weights  # Shape: [batch_size, seq_length, hidden_size]
        attended_output = weighted_embeddings.sum(dim=1)  # Shape: [batch_size, hidden_size]

        # Apply Interaction Layer
        interacted = self.interaction(last_hidden_state)  # Shape: [batch_size, seq_length, hidden_size]
        interacted = torch.mean(interacted, dim=1)  # Shape: [batch_size, hidden_size]

        # Combine [CLS] token, Attended Output, and Interaction
        cls_output = last_hidden_state[:, 0, :]  # [CLS] token representation
        combined_representation = torch.cat([cls_output, attended_output, interacted], dim=1)  # Shape: [batch_size, hidden_size * 3]

        if self.use_sparse and features is not None:
            combined_representation = torch.cat((combined_representation, features), dim=1)  # Shape: [batch_size, hidden_size * 3 + total_feature_size]

        combined = self.dropout(combined_representation)  # Shape: [batch_size, ...]
        logits = self.classifier(combined)  # Shape: [batch_size, 1]
        return logits.squeeze(-1)  # Shape: [batch_size]

def compute_bi_encoder_embeddings(model, tokenizer, texts, config):
    
    tqdm = get_tqdm(config)

    model.eval()
    device = next(model.parameters()).device
    embeddings = []
    batch_size = config['bi_encoder_batch_size']
    max_length = config['max_length']
    with torch.no_grad():
        for i in tqdm(range(0, len(texts), batch_size), desc="Computing embeddings"):
            batch_texts = texts[i:i+batch_size]
            inputs = tokenizer(batch_texts, max_length=max_length, padding=True, truncation=True, return_tensors='pt')
            input_ids = inputs['input_ids'].to(device)
            attention_mask = inputs['attention_mask'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            cls_embeddings = outputs.last_hidden_state[:, 0]  # CLS token
            embeddings.append(cls_embeddings.cpu())
    embeddings = torch.cat(embeddings, dim=0)
    return embeddings


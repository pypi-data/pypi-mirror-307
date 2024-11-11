# InterFusion Encoder

InterFusion Encoder is a Python package for training and inference of a cross-encoder model designed to match candidates with jobs using both textual data and optional sparse features. It utilizes state-of-the-art transformer models and incorporates an attention mechanism and interaction layers to enhance performance.

## **Table of Contents**

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Training](#training)
  - [Inference](#inference)
- [Data Preparation](#data-preparation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## **Features**

- Supports candidate and job features of different lengths.
- Incorporates both bi-encoder and cross-encoder architectures.
- Utilizes hard negative sampling and random negatives for robust training.
- Includes attention mechanisms and interaction layers for improved performance.
- Supports training continuation from saved checkpoints.
- Integrated with Weights & Biases (W&B) for experiment tracking.

## **Installation**

Install the package using pip:

```bash
pip install interfusion_encoder
```

## **Usage**

### **Training**

```python
from interfusion import train_model

# Prepare your data
candidates = [
    {
        "candidate_id": "cand_001",
        "candidate_text": "Experienced software engineer...",
        "candidate_features": [0.8, 0.7, 0.9]
    },
    # Add more candidates
]

jobs = [
    {
        "job_id": "job_001",
        "job_text": "Looking for a software engineer...",
        "job_features": [0.85, 0.75, 0.9, 0.95]
    },
    # Add more jobs
]

positive_matches = [
    {
        "candidate_id": "cand_001",
        "job_id": "job_001"
    },
    # Add more positive matches
]

# Define your configuration (optional)
user_config = {
    'use_sparse': True,
    'num_epochs': 5,
    'learning_rate': 3e-5,
    'cross_encoder_model_name': 'bert-base-uncased',
    'bi_encoder_model_name': 'bert-base-uncased',
    'wandb_project': 'interfusion_project',
    'wandb_run_name': 'experiment_1',
    # Add or override other configurations as needed
}

# Start training
train_model(candidates, jobs, positive_matches, user_config=user_config)
```

### **Inference**

```python
from interfusion import InterFusionInference

# Initialize inference model
config = {
    'use_sparse': True,
    'cross_encoder_model_name': 'bert-base-uncased',
    'saved_model_path': 'saved_models/interfusion_final.pt',
    'candidate_feature_size': 3,  # Set according to your data
    'job_feature_size': 4         # Set according to your data
}
inference_model = InterFusionInference(config=config)

# Prepare candidate and job texts and features
candidate_texts = [
    "Experienced software engineer...",
    # Add more candidate texts
]

job_texts = [
    "Looking for a software engineer...",
    # Add more job texts
]

candidate_features_list = [
    [0.8, 0.7, 0.9],
    # Add more candidate features
]

job_features_list = [
    [0.85, 0.75, 0.9, 0.95],
    # Add more job features
]

# Predict match scores
scores = inference_model.predict(candidate_texts, job_texts, candidate_features_list, job_features_list)

# Print the results
for candidate, job, score in zip(candidate_texts, job_texts, scores):
    print(f"Candidate: {candidate}")
    print(f"Job: {job}")
    print(f"Match Score: {score:.4f}\\n")
```

## **Data Preparation**

Ensure your data is in the form of lists of dictionaries with the following structure:

**Candidates:**

```python
[
  {
    "candidate_id": "cand_001",
    "candidate_text": "Experienced software engineer with a strong background in Python and machine learning.",
    "candidate_features": [0.8, 0.7, 0.9]
  },
  {
    "candidate_id": "cand_002",
    "candidate_text": "Data scientist with a focus on statistical modeling and data visualization using R and Python.",
    "candidate_features": [0.9, 0.6, 0.85]
  },
  {
    "candidate_id": "cand_003",
    "candidate_text": "Front-end developer skilled in React, HTML, and CSS with a keen eye for design and user experience.",
    "candidate_features": [0.7, 0.8, 0.75]
  }
]
```

**Jobs:**

```python
[
  {
    "job_id": "job_001",
    "job_text": "Looking for a software engineer with experience in Python and machine learning to work on cutting-edge AI projects.",
    "job_features": [0.85, 0.75, 0.9]
  },
  {
    "job_id": "job_002",
    "job_text": "We are seeking a data scientist with strong skills in statistical analysis and experience in Python or R.",
    "job_features": [0.9, 0.65, 0.8]
  },
  {
    "job_id": "job_003",
    "job_text": "Hiring a front-end developer proficient in React, CSS, and HTML for a dynamic and fast-paced work environment.",
    "job_features": [0.7, 0.85, 0.8]
  }
]
```

**Positive Matches:**

```python
[
  {
    "candidate_id": "cand_001",
    "job_id": "job_001"
  },
  {
    "candidate_id": "cand_002",
    "job_id": "job_002"
  },
  {
    "candidate_id": "cand_003",
    "job_id": "job_003"
  }
]
```

## **Configuration**

You can customize the model and training parameters by passing a user_config dictionary to the train_model function. Here are some of the configurable parameters:

- random_seed: Random seed for reproducibility.
- max_length: Maximum sequence length for tokenization.
- use_sparse: Whether to use sparse features.
- bi_encoder_model_name: Pre-trained model name for the bi-encoder.
- cross_encoder_model_name: Pre-trained model name for the cross-encoder.
- learning_rate: Learning rate for the optimizer.
- num_epochs: Number of training epochs.
- train_batch_size: Batch size for training.
- wandb_project: W&B project name for logging.
- saved_model_path: Path to save or load the trained model.

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## **License**

This project is licensed under the MIT License - see the LICENSE file for details.

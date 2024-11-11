# interfusion/config.py

def get_default_config():
    # Default configuration dictionary
    config = {
        'random_seed': 66,
        'max_length': 32,
        'use_sparse': False,
        'start_rank': 2000,
        'use_wandb': True,   # Set to True to enable wandb, False to disable
        'use_mlflow': False, # Set to True to enable mlflow, False to disable
        'bi_encoder_model_name': 'bert-base-uncased',  # Update with your model
        'cross_encoder_model_name': 'bert-base-uncased',  # Update with your model
        'use_tqdm': True,           # Set to True to enable tqdm progress bars, False to disable
        'tqdm_type': 'notebook',    # Options: 'standard', 'notebook'
        'learning_rate': 2e-5,  # Maximum learning rate
        'initial_learning_rate': 2e-8,  # Initial learning rate at epoch 0
        'num_epochs': 10,
        'train_batch_size': 32,  # Number of data samples per batch
        'accumulation_steps': 4,
        'bi_encoder_batch_size': 64,
        'negative_batch_size': 64,
        "random_candidate_sample_amount": 0.2,
        'M': 250,  # Number of negatives to precompute per candidate
        'N': 10,   # Number of hard negatives and random negatives per candidate (each)
        'apply_count_threshold': 10,
        'eval_Ns': [1, 5, 10],
        'save_dir': 'saved_models',
        'num_workers': 4,  # Number of worker threads for data loading
        'eval_K': 50,
        'eval_epoch': 10,
        'eval_apply_count_threshold': 5,
        'hard_negative_sampling_frequency': 5,
        'temperature': 1.0,  # Temperature parameter for softmax
        'wandb_project': 'interfusion_project',  # W&B project name
        'wandb_run_name': 'interfusion_run',     # W&B run name
        'continue_training': False,  # Set to True to load saved model and continue training
        'saved_model_path': '',  # Path to the saved model
    }
    return config


from json import dump as json_dump
from json import load as json_load

from os import path as os_path
from transformers import BertConfig, BertModel

class ModelsRepo:
    def __init__(self, repo_file):
        # JSON file to store models' configurations
        self.repo_file = repo_file
        
        # Load existing models from the JSON file if it exists
        self.repo = self._load_repo()

    def _load_repo(self):
        """Load models configurations from the JSON file."""
        if os_path.exists(self.repo_file):
            with open(self.repo_file, 'r') as file:
                return json_load(file)
        return {}

    def _save_repo(self):
        """Save the updated models configurations to the JSON file."""
        with open(self.repo_file, 'w') as file:
            json_dump(self.repo, file, indent=4)

    def _get_model_key(self, model_name, **config):
        """Generate a unique key based on model name and configuration."""
        config_str = "-".join([f"{key}-{value}" for key, value in config.items()])
        return f"{model_name}-{config_str}"

    def add_model(self, model_name, **config):
        """Add a new model configuration if it doesn't exist."""
        model_key = self._get_model_key(model_name, **config)

        # Check if the model already exists
        if model_key in self.repo:
            print(f"Model {model_key} already exists.")
            return self.repo[model_key]
        
        # Create a new model if it doesn't exist
        print(f"Creating new model: {model_key}")
        if model_name == 'bertlight':
            bert_config = BertConfig(num_hidden_layers=config.get('num_hidden_layers', 3))
            model = BertModel(bert_config)
        else:
            raise ValueError(f"Unknown model name: {model_name}")
        
        # Save the new model configuration in the repo and write to the JSON file
        self.repo[model_key] = config
        self._save_repo()
        return model

    def delete_model(self, model_name, **config):
        """Delete a model configuration from the repo and JSON file."""
        model_key = self._get_model_key(model_name, **config)

        # Check if the model exists in the repo
        if model_key in self.repo:
            del self.repo[model_key]
            self._save_repo()  # Update the JSON file
            print(f"Deleted model {model_key}")
        else:
            print(f"Model {model_key} does not exist.")
    
    def list_models(self):
        """List all models stored in the repo."""
        return list(self.repo.keys())

# Usage
repo_file_path = "modelsRepo.json"  # The JSON file path to store the models' repo

models_repo = ModelsRepo(repo_file_path)

# Adding models
model1 = models_repo.add_model("bertlight", num_hidden_layers=3)
model2 = models_repo.add_model("bertlight", num_hidden_layers=4)

# Trying to add the same model again (will return the existing one)
model3 = models_repo.add_model("bertlight", num_hidden_layers=3)

# Listing all models in the repo
print("Available models:", models_repo.list_models())

# Deleting a model
models_repo.delete_model("bertlight", num_hidden_layers=3)

# Listing again after deletion
print("Available models after deletion:", models_repo.list_models())
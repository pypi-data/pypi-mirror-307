import os
import yaml

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "default_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


CONFIG = load_config()

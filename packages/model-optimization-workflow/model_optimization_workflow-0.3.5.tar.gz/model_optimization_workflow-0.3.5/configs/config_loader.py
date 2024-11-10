import importlib
import os
from datetime import datetime, timezone

import yaml


class ConfigLoader:
    def __init__(self, config_path=None, user_config_path=None):
        base_path = os.path.dirname(os.path.abspath(__file__))
        if config_path is None:
            config_path = os.path.join(base_path, 'default_workflow_config.yaml')

        self.default_config_path = config_path
        self.user_config_path = user_config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.default_config_path, 'r') as file:
            default_config = yaml.safe_load(file)

        if self.user_config_path:
            with open(self.user_config_path, 'r') as file:
                user_config = yaml.safe_load(file)
            config = self.merge_configs(default_config, user_config)
        else:
            config = default_config

        return config

    def merge_configs(self, default_config, user_config):
        if isinstance(default_config, dict) and isinstance(user_config, dict):
            merged_config = default_config.copy()
            for key, value in user_config.items():
                if key in merged_config and isinstance(merged_config[key], dict):
                    merged_config[key] = self.merge_configs(merged_config[key], value)
                else:
                    merged_config[key] = value
            return merged_config
        else:
            return user_config

    def map_classes(self, config_section):
        if isinstance(config_section, dict):
            mapped_config = {}
            for key, value in config_section.items():
                if key in ['day_from', 'day_to'] and isinstance(value, str):
                    mapped_config[key] = datetime.strptime(value, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                elif key == 'class' and isinstance(value, str):
                    try:
                        module_name, class_name = value.rsplit('.', 1)
                        module = importlib.import_module(module_name)
                        cls = getattr(module, class_name)
                        mapped_config[key] = cls
                    except Exception as e:
                        raise ImportError(f"Failed to import class '{value}': {e}")
                elif isinstance(value, dict):
                    mapped_config[key] = self.map_classes(value)
                elif isinstance(value, list):
                    mapped_config[key] = [self.map_classes(item) for item in value]
                else:
                    mapped_config[key] = value
            return mapped_config
        elif isinstance(config_section, list):
            return [self.map_classes(item) for item in config_section]
        else:
            return config_section

    def get_config(self):
        config = self.config.copy()
        return self.map_classes(config)

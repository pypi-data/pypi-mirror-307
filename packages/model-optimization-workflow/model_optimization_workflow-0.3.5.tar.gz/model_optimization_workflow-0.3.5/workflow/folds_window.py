import os
from typing import List

from common.common import prepare_directory

from model_container.model_container import ModelContainer
from report.report import WindowReport


class FoldsWindow:
    def __init__(self, config, params, window_folds_schema, root_directory):
        self.params = params
        self.window_folds_schema = window_folds_schema
        self.config = config
        self.root_directory = root_directory
        self.window_id = f'window_{self.window_folds_schema[0]}'
        self.window_directory = os.path.join(self.root_directory, f'windows/{self.window_id}')
        prepare_directory(self.window_directory)
        self.model_containers: List[ModelContainer] = self._load_containers()

    def _load_containers(self):
        containers = []
        model_containers_config = self.config['workflow']['model_containers']
        for container_config in model_containers_config:
            container_id = container_config['name']
            parameters = container_config['parameters'].copy()

            folds_from = parameters.pop('fold_from', None)
            folds_to = parameters.pop('fold_to', None)
            container_class = parameters.pop('class', None)

            container_params = {}
            for key, value in self.params['containers_params'].items():
                prefix = f"container_{container_id}_"
                if key.startswith(prefix):
                    param_name = key[len(prefix):]
                    container_params[param_name] = value

            folds_indices = list(range(folds_from, folds_to + 1))
            folds_schema = [self.window_folds_schema[i] for i in folds_indices]
            folds_directory = os.path.join(self.root_directory, f'folds')
            container = container_class(container_params, self.window_directory, folds_directory, container_id,
                                        folds_schema)
            containers.append(container)

        return containers

    def execute(self):
        containers_reports = []

        for container in self.model_containers:
            containers_reports.append(container.run())

        return WindowReport(window_id=self.window_id, containers_reports=containers_reports)

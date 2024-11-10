import json
import os
from abc import ABC, abstractmethod
from datetime import datetime

from report.report import ContainerReport


class ModelContainer(ABC):
    def __init__(self, params: dict, root_folder: str, folds_folder: str, container_id: str, folds_schema: []):
        self.params = params
        self.folds_folder = folds_folder
        self.container_folder = os.path.join(root_folder, container_id)
        self.container_id = container_id
        self.folds_schema = folds_schema
        self.folds = self._load_folds()

    def _load_folds(self):
        all_folds_data = []

        for fold_number in self.folds_schema:
            fold_path = os.path.join(self.folds_folder, f'{fold_number}')
            fold_files = []

            for file_name in os.listdir(fold_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(fold_path, file_name)
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        fold_files.append(data)

            fold_files.sort(key=lambda x: x['from'])
            all_folds_data.append(fold_files)

        return all_folds_data

    def run(self):
        print(f"process-{os.getpid()}, time: {datetime.now()}, executing container: {self.container_id} with folds: {self.folds_schema}")
        self.execute(self.folds)
        return self.get_report()

    @abstractmethod
    def execute(self, folds):
        pass

    @abstractmethod
    def get_report(self) -> ContainerReport:
        pass

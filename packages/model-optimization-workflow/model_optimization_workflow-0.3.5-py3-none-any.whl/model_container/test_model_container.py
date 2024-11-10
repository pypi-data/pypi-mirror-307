import random

from model_container.model_container import ModelContainer
from report.report import ValidationRow, ModelReport, ContainerReport


class TestModelContainer(ModelContainer):
    def get_report(self):
        models_reports = []
        for model_index in range(2):
            validation_rows = []

            for index, (t_from, labels) in enumerate(self.saved_data):
                planned = {
                    "labels": labels
                }
                predicted = {
                    "labels": {
                        "class_1": random.randint(0, 1)
                    }
                }
                validation_rows.append(
                    ValidationRow(time=t_from, planned=planned, predicted=predicted)
                )

            model_report = ModelReport(model_id=f"model_{model_index + 1}", validation_rows=validation_rows)
            models_reports.append(model_report)

        return ContainerReport(container_id=self.container_id, models_reports=models_reports)

    def execute(self, folds):
        self._extract_labels_and_times()

    def _extract_labels_and_times(self):
        self.saved_data = []
        last_fold = self.folds[-1]
        for dataset in last_fold:
            self.saved_data.append((dataset['from'], dataset['labels']))

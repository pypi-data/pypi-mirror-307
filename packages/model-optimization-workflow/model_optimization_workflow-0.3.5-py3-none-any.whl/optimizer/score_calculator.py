from abc import ABC, abstractmethod
from typing import List

from report.report import RunReport, ValidationRow


class ScoreCalculator(ABC):
    def __init__(self, window_indices: List[int], container_indices: List[int], model_indices: List[int]):
        self.window_indices = window_indices
        self.container_indices = container_indices
        self.model_indices = model_indices

    def execute(self, report: RunReport):
        window_indices = self.window_indices if self.window_indices else list(range(len(report.windows_reports)))

        window_validation_rows = []
        for w_idx in window_indices:
            window_report = report.windows_reports[w_idx]
            containers_validation_rows = []
            container_indices = self.container_indices if self.container_indices else list(
                range(len(window_report.containers_reports)))
            selected_container_reports = [window_report.containers_reports[c_idx] for c_idx in container_indices]

            for container_report in selected_container_reports:
                model_indices = self.model_indices if self.model_indices else list(
                    range(len(container_report.models_reports)))
                selected_model_reports = [container_report.models_reports[m_idx] for m_idx in model_indices]

                for model_report in selected_model_reports:
                    containers_validation_rows.extend(sorted(model_report.validation_rows, key=lambda row: row.time))

            window_validation_rows.append(containers_validation_rows)

        return self.calculate(window_validation_rows)

    @abstractmethod
    def calculate(self, validation_rows: List[List[ValidationRow]]) -> float:
        pass

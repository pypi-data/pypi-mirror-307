from typing import List


class ValidationRow:
    def __init__(self, time: int, planned: dict, predicted: dict):
        self.time = time
        self.planned = planned
        self.predicted = predicted

    def to_dict(self):
        return {
            "time": self.time,
            "planned": self.planned,
            "predicted": self.predicted
        }


class ModelReport:
    def __init__(self, model_id: str, validation_rows: List[ValidationRow]):
        self.model_id = model_id
        self.validation_rows = validation_rows

    def to_dict(self):
        return {
            "model_id": self.model_id,
            "validation_rows": [row.to_dict() for row in self.validation_rows]
        }


class ContainerReport:
    def __init__(self, container_id: str, models_reports: List[ModelReport]):
        self.container_id = container_id
        self.models_reports = models_reports

    def to_dict(self):
        return {
            "container_id": self.container_id,
            "models_reports": [report.to_dict() for report in self.models_reports]
        }


class WindowReport:
    def __init__(self, window_id: str, containers_reports: List[ContainerReport]):
        self.window_id = window_id
        self.containers_reports = containers_reports

    def to_dict(self):
        return {
            "window_id": self.window_id,
            "containers_reports": [report.to_dict() for report in self.containers_reports]
        }


class RunReport:
    def __init__(self, run_id: str, params, windows_reports: List[WindowReport]):
        self.score = 0
        self.run_id = run_id
        self.params = params
        self.windows_reports = windows_reports

    def to_dict(self):
        return {
            "run_id": self.run_id,
            "score": self.score,
            "params": self.params,
            "windows_reports": [report.to_dict() for report in self.windows_reports]
        }


class VisualizationBinaryRow:
    def __init__(self, time: int, is_correct: bool):
        self.time = time
        self.is_correct = is_correct

    def to_dict(self):
        return {
            "time": self.time,
            "is_correct": self.is_correct
        }


class VisualizationBinaryReport:
    def __init__(self, run_id: str, score: float, params, validation_results: List[VisualizationBinaryRow]):
        self.score = score
        self.run_id = run_id
        self.params = params
        self.validation_results = validation_results

    def to_dict(self):
        return {
            "run_id": self.run_id,
            "score": self.score,
            "params": self.params,
            "validation_results": [report.to_dict() for report in self.validation_results]
        }

from typing import List

from report.report import RunReport, VisualizationBinaryReport, VisualizationBinaryRow


class VisualizationFilter:
    def __init__(self, window_indices: List[int], container_indices: List[int], model_indices: List[int]):
        self.window_indices = window_indices
        self.container_indices = container_indices
        self.model_indices = model_indices

    def transform(self, report: RunReport) -> VisualizationBinaryReport:
        selected_window_indices = self.window_indices if self.window_indices else list(
            range(len(report.windows_reports)))

        validation_results = []
        for window_index in selected_window_indices:
            window_report = report.windows_reports[window_index]

            selected_container_indices = self.container_indices if self.container_indices else list(
                range(len(window_report.containers_reports))
            )
            selected_container_reports = [window_report.containers_reports[idx] for idx in selected_container_indices]

            for container_report in selected_container_reports:
                selected_model_indices = self.model_indices if self.model_indices else list(
                    range(len(container_report.models_reports))
                )
                selected_model_reports = [container_report.models_reports[idx] for idx in selected_model_indices]

                for model_report in selected_model_reports:
                    sorted_validation_rows = sorted(model_report.validation_rows, key=lambda r: r.time)
                    validation_results.extend(self._convert_to_visualization_rows(sorted_validation_rows))

        return VisualizationBinaryReport(
            run_id=report.run_id,
            score=report.score,
            params=report.params,
            validation_results=validation_results
        )

    @staticmethod
    def _convert_to_visualization_rows(validation_rows) -> List[VisualizationBinaryRow]:
        visualization_rows = []
        for row in validation_rows:
            planned_label = row.planned['labels']['class_1']
            predicted_label = row.predicted['labels']['class_1']
            is_correct = planned_label == predicted_label
            visualization_row = VisualizationBinaryRow(time=row.time, is_correct=is_correct)
            visualization_rows.append(visualization_row)

        return visualization_rows
import json
import os

from common.common import prepare_directory

from report.all_runs_validation_report import AllRunsValidationReport
from report.сross_params_distribution_report import CrossParamsDistributionReport


class ValidationsReportManager:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.reports_validation_directory = os.path.join(self.root_directory, 'reports', 'validation')
        self.reports_screens_directory = os.path.join(self.root_directory, 'reports', 'screens')
        prepare_directory(self.reports_screens_directory)
        self.validation_results = self._load_validation_results()

    def _load_validation_results(self):
        validation_results = []
        for filename in os.listdir(self.reports_validation_directory):
            if filename.endswith('.json'):
                with open(os.path.join(self.reports_validation_directory, filename), 'r') as file:
                    data = json.load(file)
                    validation_results.append(data)

        return validation_results

    def generate_reports(self):
        AllRunsValidationReport(validation_results=self.validation_results,
                                output_folder=self.reports_screens_directory).generate()
        CrossParamsDistributionReport(validation_results=self.validation_results,
                                      output_folder=self.reports_screens_directory).generate()
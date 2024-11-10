from typing import List

from sklearn.metrics import f1_score

from optimizer.score_calculator import ScoreCalculator
from report.report import ValidationRow


class BinaryClassScoreCalculator(ScoreCalculator):

    @staticmethod
    def _adjusted_f_score(y_true, y_pred, penalty_factor=0.01):
        F_score = f1_score(y_true, y_pred, average='binary')

        states = []
        for yt, yp in zip(y_true, y_pred):
            if yt == yp:
                states.append('C')  # Correct
            else:
                states.append('E')  # Error

        max_error_sequence_length = 0
        current_error_sequence_length = 0

        for state in states:
            if state == 'E':
                current_error_sequence_length += 1
                if current_error_sequence_length > max_error_sequence_length:
                    max_error_sequence_length = current_error_sequence_length
            else:
                current_error_sequence_length = 0

        penalty = penalty_factor * max_error_sequence_length

        penalty = min(penalty, F_score)

        Adjusted_F_score = F_score - penalty

        Adjusted_F_score = max(Adjusted_F_score, 0)

        return Adjusted_F_score

    def calculate(self, validation_rows: List[List[ValidationRow]]) -> float:
        adjusted_f1_scores = []

        for fold in validation_rows:
            true_labels = []
            predicted_labels = []

            for row in fold:
                planned_label = row.planned['labels']['class_1']
                predicted_label = row.predicted['labels']['class_1']

                true_labels.append(planned_label)
                predicted_labels.append(predicted_label)

            fold_adjusted_f1_score = self._adjusted_f_score(true_labels, predicted_labels)
            adjusted_f1_scores.append(fold_adjusted_f1_score)

        average_adjusted_f1_score = sum(adjusted_f1_scores) / len(adjusted_f1_scores)
        return average_adjusted_f1_score

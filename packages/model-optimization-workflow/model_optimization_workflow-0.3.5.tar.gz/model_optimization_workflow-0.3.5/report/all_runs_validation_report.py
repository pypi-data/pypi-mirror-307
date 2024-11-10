import seaborn as sns
from matplotlib import pyplot as plt


class AllRunsValidationReport:
    def __init__(self, output_folder, validation_results, min_score=0.0):
        self.output_folder = output_folder
        self.validation_results = validation_results
        self.min_score = min_score

    def generate(self):
        sns.set_style('white')
        plt.figure(figsize=(14, 8))

        for entry in self.validation_results:
            if entry['score'] < self.min_score:
                continue

            validation_results = entry['validation_results']
            scores = []
            indices = []

            score = 0

            for idx, result in enumerate(validation_results):
                score += 1 if result['is_correct'] else -1
                scores.append(score)
                indices.append(idx)

            sns.lineplot(
                x=indices,
                y=scores,
                linewidth=0.5,
                marker=None,
                label=f"Run: {entry['run_id']} (Score: {entry['score']:.2f})"
            )

        plt.title(f'Validation Results (Score >= {self.min_score})', fontsize=16)
        plt.xlabel('Index', fontsize=14)
        plt.ylabel('Accumulated Score', fontsize=14)
        plt.legend(loc='best', fontsize='small')
        plt.tight_layout()
        plt.savefig(f'{self.output_folder}/all_runs.png', dpi=300)
        plt.close()

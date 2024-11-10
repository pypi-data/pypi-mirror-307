import optuna


class GlobalHyperparameterOptimizer:
    def __init__(self, config):
        self.config = config
        optimizer_config = self.config['hyperparameter_optimizer']
        self.patience = optimizer_config['patience']
        self.tolerance = optimizer_config['tolerance']
        self.storage_url = optimizer_config['storage_url']
        self.study_name = optimizer_config['study_name']
        self.direction = optimizer_config['direction']
        self.best_metric = None
        self.no_improvement_count = 0

        self.study = optuna.create_study(
            study_name=self.study_name,
            storage=self.storage_url,
            direction=self.direction,
            load_if_exists=True
        )

    def suggest_parameters(self):
        if self.no_improvement_count >= self.patience:
            return None, None

        trial = self.study.ask()
        params = {
            'instruments': self._suggest_instruments(trial),
            'aggregations_configs': self._suggest_aggregations_configs(trial),
            'training_window': trial.suggest_categorical(
                'training_window',
                self.config['assembler']['dataset_labeler']['parameters']['training_window']
            ),
            'containers_params': self._suggest_model_container_params(trial),
            'total_folds': trial.suggest_categorical(
                'total_folds',
                self.config['workflow']['total_folds']
            )
        }
        return params, trial

    def _suggest_aggregations_configs(self, trial):
        aggregations = []
        for i, config in enumerate(self.config['assembler']['aggregations_configs']):
            ohlc_config = config['ohlc']
            ohlc_params = {
                "window_sec": trial.suggest_categorical(f"agr_window_sec_{i}", ohlc_config['window_sec']),
                "history_size": ohlc_config['history_size']
            }

            indicators_params = []
            if 'indicators' in config:
                for j, indicator in enumerate(config['indicators']):
                    class_name = indicator['class'].__name__
                    indicator_params = {
                        "class_name": class_name,
                        "parameters": {
                            "window_length": trial.suggest_categorical(
                                f"agr_window_sec_{i}_{class_name}_window_length_{j}",
                                indicator['parameters']['window_length']
                            )
                        }
                    }
                    indicators_params.append(indicator_params)

            aggregations.append({
                "ohlc": ohlc_params,
                "indicators": indicators_params
            })
        return aggregations

    def _suggest_model_container_params(self, trial):
        model_containers = self.config['workflow']['model_containers']
        model_params = {}

        for container in model_containers:
            container_name = container['name']
            parameters = container.get('parameters', {}).copy()
            parameters.pop('class', None)
            parameters.pop('fold_from', None)
            parameters.pop('fold_to', None)

            container_params = {}
            for param_name, param_values in parameters.items():
                suggestion_name = f"container_{container_name}_{param_name}"
                container_params[param_name] = trial.suggest_categorical(suggestion_name, param_values)
            model_params[container_name] = container_params

        return model_params

    def _suggest_instruments(self, trial):
        assembler_config = self.config['assembler']
        available_instruments = assembler_config['instruments']
        instruments = []
        for instrument in available_instruments:
            include = trial.suggest_categorical(f"include_{instrument}", [True, False])
            if include:
                instruments.append(instrument)
        return instruments

    def report_result(self, trial, metric):
        self.study.tell(trial, metric)

        if self.best_metric is None or metric > self.best_metric + self.tolerance:
            self.best_metric = metric
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1

    def passed(self, trial):
        self.study.tell(trial, float('-inf'))

    def print_final_results(self):
        trial_count = len(self.study.trials)
        best_trial = self.study.best_trial

        aggregations_configs = []
        num_aggregations = len(self.config['assembler']['aggregations_configs'])

        for i in range(num_aggregations):
            ohlc_key = f"agr_window_sec_{i}"
            if ohlc_key in best_trial.params:
                aggregation_config = {
                    "ohlc": {
                        "window_sec": best_trial.params[ohlc_key],
                        "history_size": self.config['assembler']['aggregations_configs'][i]['ohlc']['history_size']
                    },
                    "indicators": []
                }

                if 'indicators' in self.config['assembler']['aggregations_configs'][i]:
                    for j, indicator in enumerate(self.config['assembler']['aggregations_configs'][i]['indicators']):
                        indicator_class_name = indicator['class'].__name__
                        indicator_param_key = f"agr_window_sec_{i}_{indicator_class_name}_window_length_{j}"
                        if indicator_param_key in best_trial.params:
                            aggregation_config["indicators"].append({
                                "class_name": indicator_class_name,
                                "parameters": {
                                    "window_length": best_trial.params[indicator_param_key]
                                }
                            })

                aggregations_configs.append(aggregation_config)

        model_params = {}
        for key, value in best_trial.params.items():
            if key.startswith("container_"):
                parts = key.split('_')
                container_name = parts[1]
                param_name = '_'.join(parts[2:])
                if container_name not in model_params:
                    model_params[container_name] = {}
                model_params[container_name][param_name] = value

        instruments = [
            instrument
            for instrument in self.config['assembler']['instruments']
            if best_trial.params.get(f"include_{instrument}", False)
        ]

        formatted_params = {
            'instruments': instruments,
            'aggregations_configs': aggregations_configs,
            'training_window': best_trial.params['training_window'],
            'containers_params': model_params,
            'total_folds': best_trial.params['total_folds']
        }

        print(f"Optimization complete!")
        print(f"Total trials: {trial_count}")
        print(f"Best trial value (metric): {best_trial.value}")
        print(f"Best trial parameters:")
        print(formatted_params)

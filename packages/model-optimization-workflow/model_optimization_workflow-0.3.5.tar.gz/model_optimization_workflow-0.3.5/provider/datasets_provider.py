import os
from typing import List

from assembling.aggregation_config import AggregationConfig, OHLCConfig, IndicatorConfig
from assembling.historical_assembler_manager import HistoricalAssemblerManager
from providers.crypto_series_data_provider import CryptoSeriesDataProvider


class DatasetProvider:
    def __init__(self, global_config, optuna_params):
        self.global_config = global_config
        self.optuna_params = optuna_params
        self.output_folder = './out/datasets'
        os.makedirs(self.output_folder, exist_ok=True)

    def create_dataset(self):
        assembler_settings = self.global_config['assembler']
        labeler_class = assembler_settings['dataset_labeler']['class']

        manager = HistoricalAssemblerManager(
            instruments=self.optuna_params['instruments'],
            day_from=assembler_settings['day_from'],
            day_to=assembler_settings['day_to'],
            aggregations_configs=self._build_aggregation_configs(assembler_settings['aggregations_configs']),
            dataset_labeler=labeler_class(training_window=self.optuna_params['training_window']),
            raw_series_folder=CryptoSeriesDataProvider.raw_series_folder,
            max_workers=assembler_settings['max_workers']
        )

        return manager.generate_dataset()

    def _build_aggregation_configs(self, config_templates) -> List[AggregationConfig]:
        aggregation_configs = []

        for i, param_config in enumerate(self.optuna_params['aggregations_configs']):
            base_config = config_templates[0]
            ohlc_config = OHLCConfig(
                window_sec=param_config['ohlc']['window_sec'],
                history_size=param_config['ohlc']['history_size']
            )

            indicators = [
                IndicatorConfig(
                    indicator_class=base_config['indicators'][j]['class'],
                    window_length=indicator['parameters']['window_length']
                )
                for j, indicator in enumerate(param_config['indicators'])
            ]

            aggregation_configs.append(AggregationConfig(
                ohlc=ohlc_config,
                indicators=indicators
            ))

        return aggregation_configs

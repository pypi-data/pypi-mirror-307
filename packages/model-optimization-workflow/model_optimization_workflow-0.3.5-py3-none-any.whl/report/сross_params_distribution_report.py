import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


class CrossParamsDistributionReport:
    """
    Generates a report on cross-parameter distributions and their relationship with scores.
    """

    def __init__(self, validation_results, output_folder):
        """
        Initializes the CrossParamsDistributionReport class.

        Args:
            validation_results (list): List of dictionaries containing validation results.
            output_folder (str): Path to the folder where outputs will be saved.
        """
        self.validation_results = validation_results
        self.output_folder = output_folder

    def _get_formatted_params(self):
        """
        Formats the parameters from the validation results into a list of dictionaries.

        Returns:
            list: List of formatted parameter dictionaries.
        """
        formatted_params = []

        for entry in self.validation_results:
            params = entry['params']
            instruments = ", ".join(params.get('instruments', []))
            aggregation_configs = params.get('aggregations_configs', [])

            formatted_entry = {
                'instruments': instruments,
                'training_window': params.get('training_window'),
                'total_folds': params.get('total_folds'),
            }

            # Extract container parameters
            for container_name, container_params in params.get('containers_params', {}).items():
                for param_name, param_value in container_params.items():
                    formatted_entry[f"{container_name}_{param_name}"] = param_value

            # Extract aggregation configurations
            for config in aggregation_configs:
                window_sec = config.get('ohlc', {}).get('window_sec')
                formatted_entry['ohlc_sec'] = window_sec

                for idx, indicator in enumerate(config.get('indicators', [])):
                    class_name = indicator.get('class_name')
                    window_length = indicator.get('parameters', {}).get('window_length')
                    key = f"ohlc_sec_{window_sec}_{class_name}_{idx}_len"
                    formatted_entry[key] = window_length

            formatted_entry['score'] = entry.get('score')
            formatted_params.append(formatted_entry)

        return formatted_params

    def generate(self):
        """
        Generates the report by processing validation results and saving outputs.
        """
        # Format parameters and create a DataFrame
        formatted_params = self._get_formatted_params()
        df = pd.DataFrame(formatted_params)

        # Save formatted parameters to Excel
        params_excel_path = os.path.join(self.output_folder, 'formatted_parameters.xlsx')
        df.to_excel(params_excel_path, index=False)

        # Encode categorical variables
        df_encoded = df.copy()
        label_encoders = {}

        for col in df_encoded.columns:
            if df_encoded[col].dtype == 'object':
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                label_encoders[col] = le

        # Prepare data for modeling
        X = df_encoded.drop('score', axis=1)
        y = df_encoded['score']

        # Train Random Forest Regressor
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Calculate feature importances
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Parameter': X.columns,
            'Importance': importances
        }).sort_values('Importance', ascending=False)

        # Save feature importances to Excel
        importances_excel_path = os.path.join(self.output_folder, 'feature_importances.xlsx')
        feature_importance_df.to_excel(importances_excel_path, index=False)

        # Plot feature importances
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Importance', y='Parameter', data=feature_importance_df)
        plt.title('Parameter Importance for Score')
        plt.tight_layout()
        importances_plot_path = os.path.join(self.output_folder, 'feature_importances.png')
        plt.savefig(importances_plot_path)
        plt.close()

        # Compute correlations with score
        corr_with_score = df_encoded.corr()['score'].sort_values(ascending=False)
        corr_excel_path = os.path.join(self.output_folder, 'features_correlation_with_score.xlsx')
        corr_with_score.to_excel(corr_excel_path)

        # Plot correlations with score
        plt.figure(figsize=(12, 8))
        sns.barplot(x=corr_with_score.values, y=corr_with_score.index)
        plt.title('Correlation of Parameters with Score')
        plt.xlabel('Correlation')
        plt.ylabel('Parameter')
        plt.tight_layout()
        corr_plot_path = os.path.join(self.output_folder, 'features_correlation_with_score.png')
        plt.savefig(corr_plot_path)
        plt.close()

        # Analyze individual parameter values
        self._analyze_parameter_values(df)

    def _analyze_parameter_values(self, df):
        """
        Generates scatter plots and box plots for parameter values against score.

        Args:
            df (pd.DataFrame): DataFrame containing the formatted parameters and scores.
        """
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if 'score' in numeric_cols:
            numeric_cols.remove('score')

        # Plot numeric columns against score
        for col in numeric_cols:
            plt.figure(figsize=(12, 6))
            sns.scatterplot(x=col, y='score', data=df)
            plt.title(f'Score vs {col}')
            plt.tight_layout()
            filename = f"{col}_vs_score.png"
            plt.savefig(os.path.join(self.output_folder, filename))
            plt.close()

        # Plot categorical columns against score
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        for col in categorical_cols:
            plt.figure(figsize=(12, 6))
            sns.boxplot(x=col, y='score', data=df)
            plt.title(f'Score Distribution by {col}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            filename = f"{col}_boxplot.png"
            plt.savefig(os.path.join(self.output_folder, filename))
            plt.close()

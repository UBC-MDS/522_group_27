# shooting_hand_classifier.py
# author: Dominic Lam
# created date: 2024-12-05
# last modified date: 2024-12-16

# This script is responsible for carrying out our
# classification as well as reporting the results. Model classification
# is done using a logistic regression model.

# Usage:
'''
python scripts/shooting_hand_classifier.py \
    --training-data=data/processed/roster_train.csv \
    --test-data=data/processed/roster_test.csv \
    --preprocessor=results/models/roster_preprocessor.pickle \
    --pipeline-to=results/models \
    --plot-to=results/figures \
    --results-to=results/tables
'''

# Imports
import click
import pandas as pd
import pickle
import os
import sys
from deepchecks.tabular.checks import FeatureLabelCorrelation
from deepchecks.tabular import Dataset
from sklearn import set_config
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import ConfusionMatrixDisplay
import warnings
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.fit_and_evaluate_model import fit_and_evaluate_model

# Silence warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="deepchecks")

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_data_and_preprocessor(training_data, test_data, preprocessor_path):
    """Load training and test data, as well as the preprocessor object."""
    try:
        train_df = pd.read_csv(training_data)
        test_df = pd.read_csv(test_data)
        with open(preprocessor_path, "rb") as f:
            preprocessor = pickle.load(f)
        logging.info("Data and preprocessor loaded successfully.")
        return train_df, test_df, preprocessor
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}") from e


def check_data_quality(train_df):
    """Perform data quality checks on the training data."""
    # Check target distribution
    target_counts = train_df["shoots_left"].value_counts().to_dict()
    left_count = target_counts.get(True, 0)
    right_count = target_counts.get(False, 0)

    if left_count <= right_count:
        logging.warning("There should be more left-handed shooters than right-handed shooters.")

    # Feature-label correlation check
    train_ds = Dataset(train_df, label="shoots_left", cat_features=[])
    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.9)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset=train_ds)

    if not check_feat_lab_corr_result.passed_conditions():
        raise ValueError("Feature-label correlation exceeds the maximum acceptable threshold.")
    logging.info("Data quality checks passed successfully.")


def save_outputs(logreg_fit, accuracy, results_to, pipeline_to, plot_to, X_test, y_test):
    """Save test scores, pipeline object, and confusion matrix."""
    # Ensure directories exist
    os.makedirs(results_to, exist_ok=True)
    os.makedirs(pipeline_to, exist_ok=True)
    os.makedirs(plot_to, exist_ok=True)

    # Save accuracy scores
    test_scores = pd.DataFrame({'accuracy': [accuracy]})
    test_scores.to_csv(os.path.join(results_to, "test_scores.csv"), index=False)
    logging.info("Test scores saved.")

    # Save the pipeline
    with open(os.path.join(pipeline_to, "shooter_pipeline.pickle"), 'wb') as f:
        pickle.dump(logreg_fit, f)
    logging.info("Pipeline saved.")

    # Generate and save confusion matrix
    cm = ConfusionMatrixDisplay.from_estimator(
        logreg_fit,
        X_test,
        y_test,
        values_format="d",
        display_labels=["Shoots Right", "Shoots Left"]
    )
    # Add a title to the confusion matrix
    cm.ax_.set_title("Confusion Matrix for Shooting Hand Classification")
    cm.ax_.set_xlabel("Predicted Class")
    cm.ax_.set_ylabel("Actual Class")
    
    cm.figure_.tight_layout()
    cm.figure_.savefig(os.path.join(plot_to, "confusion_matrix.png"), dpi=300)
    logging.info("Confusion matrix saved.")


@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--test-data', type=str, help="Path to test data")
@click.option('--preprocessor', type=str, help="Path to preprocessor object")
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--results-to', type=str, help="Path to directory where the scores will be written to")
def main(training_data, test_data, preprocessor, pipeline_to, plot_to, results_to):
    """
    Main function to train a logistic regression model on shooting hand data.
    """
    set_config(transform_output="pandas")

    # Load data and preprocessor
    train_df, test_df, preprocessor = load_data_and_preprocessor(training_data, test_data, preprocessor)

    # Check data quality
    check_data_quality(train_df)

    # Prepare data
    X_train = train_df.drop(columns=["shoots_left"])
    X_test = test_df.drop(columns=["shoots_left"])
    y_train = train_df["shoots_left"]
    y_test = test_df["shoots_left"]

    # Fit and evaluate model
    logreg_fit, accuracy = fit_and_evaluate_model(X_train, y_train, X_test, y_test, preprocessor)

    # Save outputs
    save_outputs(logreg_fit, accuracy, results_to, pipeline_to, plot_to, X_test, y_test)


if __name__ == '__main__':
    main()
'''
python scripts/shooting_hand_classifier.py \
    --training-data=data/processed/roster_train.csv \
    --test-data=data/processed/roster_test.csv \
    --preprocessor=results/models/roster_preprocessor.pickle \
    --pipeline-to=results/models \
    --plot-to=results/figures \
    --results-to=results/tables
'''

import click
import pandas as pd
import pickle
import os
from deepchecks.tabular.checks import FeatureLabelCorrelation
from deepchecks.tabular import Dataset
from sklearn import set_config
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import ConfusionMatrixDisplay
import warnings


warnings.filterwarnings("ignore", category=FutureWarning, module="deepchecks")


@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--test-data', type=str, help="Path to test data")
@click.option('--preprocessor', type=str, help="Path to preprocessor object")
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--results-to', type=str, help="Path to directory where the scores will be written to")
def main(training_data, test_data, preprocessor, pipeline_to, plot_to, results_to):
    '''Fits a shooting hand classifier to the training data
    and saves the pipeline object.'''
    set_config(transform_output="pandas")

    # read in data & preprocessor
    train_df = pd.read_csv(training_data)
    test_df = pd.read_csv(test_data)
    preprocessor = pickle.load(open(preprocessor, "rb"))
    
    # No anomalous correlations between target/response variable and features/explanatory variables
    # No anomalous correlations between features/explanatory variables
    train_ds = Dataset(train_df, label="shoots_left", cat_features=[])
    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.9)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset=train_ds)

    assert check_feat_lab_corr_result.passed_conditions(), "Feature-Label correlation exceeds the maximum acceptable threshold."
    
    # Check that target distribution follows expected values
    # For example, there should not be more right handed than left handed shooters given that
    # left handedness in shooting is the more common trait.

    target_dict = train_df["shoots_left"].value_counts().to_dict()
    left_count = target_dict[True]
    right_count = target_dict[False]

    assert left_count > right_count, "There should be more left handed shooters than right handed shooters"    

    # Create X and y data frames for train and test data
    X_train = train_df.drop(columns=["shoots_left"])
    X_test = test_df.drop(columns=["shoots_left"])
    y_train = train_df["shoots_left"]
    y_test = test_df["shoots_left"]

    # Create the logistic regression model pipeline and fit on the training data
    logreg = make_pipeline(
        preprocessor,
        LogisticRegression(random_state=123, class_weight="balanced")
    )
    logreg_fit = logreg.fit(X_train, y_train);

    # Score the logistic regression model on the test data
    accuracy = logreg_fit.score(X_test, y_test)

    # Create folders if it doesn't exist
    os.makedirs(results_to, exist_ok=True)
    os.makedirs(pipeline_to, exist_ok=True)
    os.makedirs(plot_to, exist_ok=True)
    
    test_scores = pd.DataFrame({'accuracy': [accuracy]})
    test_scores.to_csv(os.path.join(results_to, "test_scores.csv"), index=False)

    # Write and save the pipeline
    with open(os.path.join(pipeline_to, "shooter_pipeline.pickle"), 'wb') as f:
        pickle.dump(logreg_fit, f)

    # Display confusion matrix for model performance on test set
    cm = ConfusionMatrixDisplay.from_estimator(
        logreg,
        X_test,
        y_test,
        values_format="d",
    )

    # Modify tick labels
    cm.ax_.set_xticklabels(["Shoots Right", "Shoots Left"])
    cm.ax_.set_yticklabels(["Shoots Right", "Shoots Left"])
    
    # Add a title and axis labels
    cm.ax_.set_title("Confusion Matrix for Shooting Hand Prediction")
    cm.ax_.set_xlabel("Predicted Class")
    cm.ax_.set_ylabel("Actual Class")
    
    # Display the plot
    cm.figure_.tight_layout()

    # Save the plot
    cm.figure_.savefig(os.path.join(plot_to, "confusion_matrix.png"), dpi=300)  


if __name__ == '__main__':
    main()
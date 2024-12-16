import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator
from typing import Tuple


def fit_and_evaluate_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    preprocessor: BaseEstimator
) -> Tuple[BaseEstimator, float]:
    """
    Function to fit a logistic regression pipeline on training data,
    evaluate its performance on test data, and return the trained
    pipeline and accuracy score.

    Parameters
    ----------
    X_train : pd.DataFrame
        Feature data for training.
    y_train : pd.Series
        Target labels for training.
    X_test : pd.DataFrame
        Feature data for testing.
    y_test : pd.Series
        Target labels for testing.
    preprocessor : sklearn.base.BaseEstimator
        Preprocessing pipeline to be applied to the data.

    Returns
    -------
    pipeline : sklearn.pipeline.Pipeline
        Trained pipeline with preprocessing and logistic regression.
    accuracy : float
        Accuracy score of the model on the test set.

    Raises
    ------
    TypeError
        If any input data is not of type pandas DataFrame/Series.
    ValueError
        If any input data is empty or if the number of features in
        X_train and X_test does not match.
    """
    # Input type validation
    if not isinstance(X_train, pd.DataFrame):
        raise TypeError("X_train must be a pandas DataFrame.")
    if not isinstance(X_test, pd.DataFrame):
        raise TypeError("X_test must be a pandas DataFrame.")
    if not isinstance(y_train, pd.Series):
        raise TypeError("y_train must be a pandas Series.")
    if not isinstance(y_test, pd.Series):
        raise TypeError("y_test must be a pandas Series.")

    # Input value validation
    if X_train.empty or y_train.empty:
        raise ValueError("X_train and y_train cannot be empty.")
    if X_test.empty or y_test.empty:
        raise ValueError("X_test and y_test cannot be empty.")
    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError("The number of features in X_train and X_test must match.")

    # Create pipeline and fit the model
    pipeline = make_pipeline(preprocessor, LogisticRegression(random_state=123, class_weight="balanced"))
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    accuracy = pipeline.score(X_test, y_test)

    return pipeline, accuracy
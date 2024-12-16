import pytest
import pandas as pd
import numpy as np
import sys
import os
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.fit_and_evaluate_model import fit_and_evaluate_model


@pytest.fixture
def sample_data():
    """Fixture to create sample training and test datasets."""
    train_data = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [5, 4, 3, 2, 1],
        "shoots_left": [True, False, True, False, True]
    })

    test_data = pd.DataFrame({
        "feature1": [6, 7],
        "feature2": [0, -1],
        "shoots_left": [True, False]
    })

    return train_data, test_data


@pytest.fixture
def mock_preprocessor():
    """Fixture to create a mock preprocessor pipeline."""
    return make_pipeline(StandardScaler())


def test_fit_and_evaluate_model_valid_input(sample_data, mock_preprocessor):
    """Test fit_and_evaluate_model with valid inputs."""
    train_df, test_df = sample_data

    # Separate features and target
    X_train = train_df.drop(columns=["shoots_left"])
    y_train = train_df["shoots_left"]
    X_test = test_df.drop(columns=["shoots_left"])
    y_test = test_df["shoots_left"]

    # Call the function
    pipeline, accuracy = fit_and_evaluate_model(X_train, y_train, X_test, y_test, mock_preprocessor)

    # Check that pipeline is returned
    assert pipeline is not None, "Pipeline should not be None."
    assert isinstance(pipeline, make_pipeline().__class__), "Pipeline should be a scikit-learn pipeline."

    # Check that accuracy is within the valid range
    assert 0 <= accuracy <= 1, "Accuracy should be between 0 and 1."


def test_fit_and_evaluate_model_invalid_input_type(sample_data, mock_preprocessor):
    """Test fit_and_evaluate_model with invalid input types."""
    train_df, test_df = sample_data

    # Invalid types for X and y
    invalid_X = "invalid"
    invalid_y = "invalid"

    with pytest.raises(TypeError, match="X_train must be a pandas DataFrame."):
        fit_and_evaluate_model(invalid_X, invalid_y, invalid_X, invalid_y, mock_preprocessor)


def test_fit_and_evaluate_model_empty_data(mock_preprocessor):
    """Test fit_and_evaluate_model with empty data."""
    # Empty DataFrames
    X_train = pd.DataFrame()
    y_train = pd.Series(dtype=bool)
    X_test = pd.DataFrame()
    y_test = pd.Series(dtype=bool)

    with pytest.raises(ValueError, match="X_train and y_train cannot be empty."):
        fit_and_evaluate_model(X_train, y_train, X_test, y_test, mock_preprocessor)


def test_fit_and_evaluate_model_no_features(sample_data, mock_preprocessor):
    """Test fit_and_evaluate_model with missing features."""
    train_df, test_df = sample_data

    # Remove features
    X_train = train_df.drop(columns=["feature1", "feature2"])
    y_train = train_df["shoots_left"]
    X_test = test_df.drop(columns=["feature1", "feature2"])
    y_test = test_df["shoots_left"]

    with pytest.raises(ValueError, match="The number of features in X_train and X_test must match."):
        fit_and_evaluate_model(X_train, y_train, X_test, y_test, mock_preprocessor)
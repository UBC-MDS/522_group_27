import pytest
import sys
import os
import pandas as pd

# Import the write_csv function from the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.write_csv import write_csv


# Create test dataframe
@pytest.fixture
def test_df():
    return pd.DataFrame({
        "shoots_left": [0, 1, 0],
        "weight_in_kilograms": [70, 80, 60],
        "height_in_centimeters": [180, 185, 190],
    })

# Create temporary directory path
@pytest.fixture
def tmp_dir(tmp_path):
    return tmp_path

# Test for correct write without index
def test_write_csv_success(test_df, tmp_dir):
    file_name = "test_df.csv"

    # Call function
    write_csv(test_df, tmp_dir, file_name)
    
    file_path = os.path.join(tmp_dir, file_name)

    # Check that file exists
    assert os.path.isfile(file_path)

    caclulated_df = pd.read_csv(file_path)
    expected_df = test_df.reset_index(drop=True)

    # Confirm that contents of CSV match the original dataframe
    pd.testing.assert_frame_equal(caclulated_df, expected_df)

# Test for correct write with index
def test_write_csv_index(test_df, tmp_dir):
    file_name = "test_index.csv"

    # Call function
    write_csv(test_df, tmp_dir, file_name, keep_index=True)
    
    file_path = os.path.join(tmp_dir, file_name)
    
    # Check that the file exists
    assert os.path.isfile(file_path)

    caclulated_df = pd.read_csv(file_path, index_col=0)
    expected_df = test_df

    # Confirm that contents of CSV match the original dataframe
    pd.testing.assert_frame_equal(caclulated_df, expected_df)

# Test for incorrect input
def test_write_csv_bad_input_type(tmp_dir):
    bad_df = "This is not a DataFrame"
    file_name = "test_df.csv"
    
    with pytest.raises(TypeError, match="The input must be of type Pandas DataFrame."):
        write_csv(bad_df, tmp_dir, file_name)

# Test for missing directory
def test_write_csv_nonexistent_directory(test_df):
    bad_dir = "/this_does_not_exist"
    file_name = "test_df.csv"
    
    with pytest.raises(FileNotFoundError, match="Directory does not exist."):
        write_csv(test_df, bad_dir, file_name)

# Test for correct error handling for incorrect file name
def test_write_csv_bad_filename(test_df, tmp_dir):
    bad_file_name = "test.ipynb"
    
    with pytest.raises(ValueError, match="Filename must end with '.csv'."):
        write_csv(test_df, tmp_dir, bad_file_name)

# Test for correct error handling for an empty DataFrame
def test_write_csv_empty_dataframe(tmp_dir):
    empty_df = pd.DataFrame()
    file_name = "test_df.csv"
    
    with pytest.raises(ValueError, match="Dataframe must have records."):
        write_csv(empty_df, tmp_dir, file_name)
import pytest
import sys
import os
import pandas as pd

# Import the write_csv function from the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.check_eda import check_eda

# Create temporary directory path
@pytest.fixture
def tmp_dir(tmp_path):
    return tmp_path

# Create test dataframe
@pytest.fixture
def test_df():
    return pd.DataFrame({
        "shoots_left": [1, 2, 3, 4],
        "age": [60, 50, 80, 100]
    })

# Tests main function
def test_check_eda(test_df, tmp_dir):
    
    check_eda(test_df, str(tmp_dir))

    describe = os.path.join(tmp_dir, 'df_describe.csv') 
    head = os.path.join(tmp_dir, 'df_head.csv') 
    info = os.path.join(tmp_dir, 'df_info.csv') 

    # Check if all files exist
    assert os.path.isfile(describe)
    assert os.path.isfile(head)
    assert os.path.isfile(info)

# Test for bad dataframe
def test_check_eda_dataframe(tmp_dir):
    bad_df = 'hello'
    with pytest.raises(TypeError, match="Inputs must be a dataframe and a string."):
        check_eda(bad_df, str(tmp_dir))

# Test for bad file path
def test_check_eda_file_path(test_df, tmp_dir):
    bad_df = test_df
    with pytest.raises(TypeError, match="Inputs must be a dataframe and a string."):
        check_eda(bad_df, tmp_dir)

# Test for edgecase, empty dataframes created
def test_write_csv_empty_dataframe(tmp_dir):
    df = pd.DataFrame()
    
    describe = os.path.join(tmp_dir, 'df_describe.csv') 
    head = os.path.join(tmp_dir, 'df_head.csv') 
    info = os.path.join(tmp_dir, 'df_info.csv') 

    with pytest.raises(ValueError, match="Cannot describe a DataFrame without columns"):
        check_eda(df, str(describe))
        check_eda(df, str(head))
        check_eda(df, str(info))
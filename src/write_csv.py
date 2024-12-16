import os
import pandas as pd


def write_csv(
    df: pd.DataFrame,
    directory: str,
    filename: str,
    keep_index: bool = False
):
    """Function to write a DataFrame object as a CSV file to a specified
    location. Takes in an optional argument to specifiy if the index
    column should be saved or not.

    Parameters
    ----------
    df : pd.DataFrame
        The Pandas DataFrame to save to a CSV.
    directory : str
        The location to save the CSV to.
    filename : str
        The desired filename for the newly created CSV file.
    keep_index : bool, optional
        Boolean to indicate whether to keep the index column
        from the DataFrame, by default False

    Raises
    ------
    TypeError
        The input is not a Pandas DataFrame
    FileNotFoundError
        The directory cannot be found
    ValueError
        The output file name does not end with .csv
    ValueError
        The input DataFrame is empty
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The input must be of type Pandas DataFrame.")
    if not os.path.exists(directory):
        raise FileNotFoundError("Directory does not exist.")
    if not filename.endswith(".csv"):
        raise ValueError("Filename must end with '.csv'.")
    if df.empty:
        raise ValueError("Dataframe must have records.")

    full_path = os.path.join(directory, filename)
    df.to_csv(full_path, index=keep_index)

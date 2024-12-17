import os
import pandas as pd


def check_eda(train_df, path_for_tables):
    """Function reads in data, creates 3 tables of EDA (info, describe, head)
    and saves tables as CSVs in specified directory.

    Parameters
    ----------
    train_df : pd.Dataframe
        Pandas dataframe.
    path_for_tables : str
        The location to save the CSVs to.
        
    Raises
    ------
    TypeError
        Either input is not a string
    FileNotFoundError
        The directory doesnt exist
    ValueError
        Created dataframes are empty
    """
    
    if not isinstance(train_df, pd.DataFrame) or not isinstance(path_for_tables, str):
        raise TypeError("Inputs must be a dataframe and a string.")
    
    # Create info lookalike dataframe
    info = pd.DataFrame({
        "name": train_df.columns,
        "non-nulls": len(train_df)-train_df.isnull().sum().values,
        "nulls": train_df.isnull().sum().values,
        "type": train_df.dtypes.values
    })
    describe = train_df.describe()
    head = train_df.head()
    
    if not os.path.exists(path_for_tables):
        raise FileNotFoundError("Directory does not exist.")
    
    if info.empty or describe.empty or head.empty:
        raise ValueError("Cannot describe a DataFrame without columns")

    info.to_csv(os.path.join(path_for_tables, 'df_info.csv'))
    describe.to_csv(os.path.join(path_for_tables, 'df_describe.csv'))
    head.to_csv(os.path.join(path_for_tables, 'df_head.csv'))
    
    return train_df

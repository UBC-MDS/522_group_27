# preprocess_and_validate.py
# author: Michael Gelfand
# date: 2024-12-15

# This script reads in the raw NHL roster data stored in the data folder and
# performs the cleaning and preprocessing necessary for the data to be read
# in to the EDA and model scripts. It saves the train and test splits of the
# data as well as the preprocessor to be used in the model training.

'''
Usage: python scripts/preprocess_and_validate.py \
    --raw-data=data/raw/nhl_rosters.csv \
    --data-to=data/processed \
    --preprocessor-to=results/models
'''

# Imports
import click
import json
import logging
import os
import pandas as pd
import pandera as pa
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer


@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
def main(raw_data, data_to, preprocessor_to):
    """Main function to execute preprocessing and cleaning"""
    set_config(transform_output="pandas")

    column_names = [
        'team_code',
        'season',
        'position_type',
        'player_id',
        'headshot',
        'first_name',
        'last_name',
        'sweater_number',
        'position_code',
        'shoots_catches',
        'height_in_inches',
        'weight_in_pounds',
        'height_in_centimeters',
        'weight_in_kilograms',
        'birth_date',
        'birth_city',
        'birth_country',
        'birth_state_province'
    ]

    # Read in raw data
    rosters = pd.read_csv(raw_data)

    # Data Validation: Check if column names are correct
    for column in rosters.columns:
        assert column in column_names, "Data Validation: Incorrect column names"

    # Data wrangling and cleanup
    # Drop NA records
    rosters_clean = rosters.drop_duplicates()
    if rosters_clean.duplicated().any():
        raise ValueError("Duplicate rows found in the rosters_clean DataFrame")

    rosters_clean = rosters_clean[[
        "weight_in_kilograms",
        "height_in_centimeters",
        "shoots_catches"
    ]]
    rosters_clean = rosters_clean.dropna()

    # Data Validation: Check for Empty Observations
    assert not rosters_clean.isnull().values.any(), "Data Validation: There are empty observations!"

    # Convert target column to binary with shoots left as 1 and shoots right as 0
    rosters_clean["shoots_left"] = rosters_clean["shoots_catches"].replace({
        'L': True,
        'R': False
    }).astype(bool)
    rosters_clean = rosters_clean.drop("shoots_catches", axis=1)

    # Data Validation with Pandera:
    schema = pa.DataFrameSchema(
        {
            "weight_in_kilograms": pa.Column(float, pa.Check.between(55, 125), nullable=False),
            "height_in_centimeters": pa.Column(float, pa.Check.between(155, 210), nullable=False),
            "shoots_left": pa.Column(bool, pa.Check.isin([True, False]), nullable=False)
        }
    )

    # Initialize error cases DataFrame
    error_cases = pd.DataFrame()
    data = rosters_clean.copy()

    # Validate data and handle errors
    try:
        validated_data = schema.validate(data, lazy=True)
    except pa.errors.SchemaErrors as e:
        error_cases = e.failure_cases

        # Convert the error message to a JSON string
        error_message = json.dumps(e.message, indent=2)
        logging.error("\n" + error_message)

    # Filter out invalid rows based on the error cases
    if not error_cases.empty:
        invalid_indices = error_cases["index"].dropna().unique()
        validated_data = (
            data.drop(index=invalid_indices)
            .reset_index(drop=True)
            .drop_duplicates()
            .dropna(how="all")
        )
    else:
        validated_data = data

    # Split into train and test
    train_df, test_df = train_test_split(rosters_clean, test_size=0.3, random_state=123)

    # Create processed data folder if it doesn't exist
    os.makedirs(data_to, exist_ok=True)

    train_df.to_csv(os.path.join(data_to, "roster_train.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "roster_test.csv"), index=False)

    # Lists of feature names
    numeric_features = ["weight_in_kilograms", "height_in_centimeters"]

    # Create the column transformer
    roster_preprocessor = make_column_transformer(
        (StandardScaler(), numeric_features),  # scaling on numeric features
    )

    # Create model directory if does not exist
    os.makedirs(preprocessor_to, exist_ok=True)

    pickle.dump(roster_preprocessor, open(os.path.join(preprocessor_to, "roster_preprocessor.pickle"), "wb"))


if __name__ == '__main__':
    main()

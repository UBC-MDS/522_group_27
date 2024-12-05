# download_data.py
# author: Michael Gelfand
# date: 2024-12-05

# This script will download the NHL roster information from the provided URL
# and save it in to the raw data folder in the repository.

# Usage
# python scripts/download_data.py \
#   --url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/refs/heads/main/data/2024/2024-01-09/nhl_rosters.csv" \
#   --write_to=data/raw

# Imports
import click
import os
import requests
import pandas as pd


def read_zip(url, directory):
    """
    Read a csv file from the given URL and extract its contents to the specified directory.

    Parameters:
    ----------
    url : str
        The URL of the csv file to be read.
    directory : str
        The directory where the contents of the zip file will be extracted.

    Returns:
    -------
    None
    """
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    # check if URL exists, if not raise an error
    if request.status_code != 200:
        raise ValueError('The URL provided does not exist.')

    # check if the directory exists, if not raise an error
    if not os.path.isdir(directory):
        raise ValueError('The directory provided does not exist.')

    # Read csv file in to a DataFrame
    df = pd.read_csv(url)

    # Write the DataFrame to a CSV file
    path_to_file = os.path.join(directory, filename_from_url)
    df.to_csv(path_to_file, index=False)


@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write_to', type=str, help="Path to directory where raw data is written")
def main(url, write_to):
    """Downloads csv data from the web to a local filepath and extracts it"""
    try:
        read_zip(url, write_to)
    except:
        os.makedirs(write_to)
        read_zip(url, write_to)

# Call main function
if __name__ == '__main__':
    main()
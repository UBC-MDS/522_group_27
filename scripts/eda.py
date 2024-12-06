# eda.py
# author: Jay Mangat
# date: december 5, 2024

# This script reads takes the processed data from the previous script and performs
# EDA on it (info, describe, head) and saves the outputs as csv files in the results folder.
# The script also creates a altair figure comparing the distribution of values within 
# the processed data and saves the figure as a png within results.

'''
Usage: python scripts/eda.py \
    --processed-training-data=data/processed/roster_train.csv \
    --plot-to=results
'''

# import libraries/packages
import click
import os
import altair as alt
import numpy as np
import pandas as pd
import vl_convert as vlc        #needed for saving graph as png

# parse/define command line arguments here
@click.command()
@click.option('--processed-training-data', type=str, help="Path to processed training data")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")

# code for other functions
def main(processed_training_data, plot_to):
    '''Plots the densities of each feature in the processed training data
        by class and displays them as a grid of plots. Also saves the plot.'''

    df = pd.read_csv(processed_training_data)

    summary = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.count(),
        "Data Type": df.dtypes
    })

    summary.to_csv(os.path.join(plot_to, 'tables/df_info.csv'), index=False)

    describe = df.describe()
    describe.to_csv(os.path.join(plot_to, 'tables/df_describe.csv'))

    head = df.head()
    head.to_csv(os.path.join(plot_to, 'tables/df_head.csv'))

    weight_chart = alt.Chart(df).mark_bar().encode(
        alt.X("weight_in_kilograms:Q", title="Weight (kg)").bin(),
        alt.Y("count()", title="Number of Players"),
        alt.Color("shoots_left", title="Shoots Left")
        ).properties(
            title="Distribution of Player Weight by Shooting Hand",
            height=300,
            width=200
        ).facet(
            "shoots_left",
            )
        
    height_chart = alt.Chart(df).mark_bar().encode(
        alt.X("height_in_centimeters:Q", title="Height (cm)").bin(),
        alt.Y("count()", title="Number of Players"),
        alt.Color("shoots_left", title="Shoots Left")
        ).properties(
            title="Distribution of Player Height by Shooting Hand",
            height=300,
            width=200
        ).facet(
            "shoots_left",
        )
        
    combined_chart = alt.vconcat(weight_chart, height_chart).properties(
        title="Distribution of Player Height by Shooting Hand"
    )
    combined_chart.save(os.path.join(plot_to, "figures/combined_chart.png"))


if __name__ == '__main__':
    main()







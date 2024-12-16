# eda.py
# author: Jay Mangat
# date: december 5, 2024

# This script will will perform exploratory data analysis on the
# cleaned up training data. It will create tables and figures
# associated with this EDA process.

# Usage
'''
python scripts/eda.py \
    --processed-training-data=data/processed/roster_train.csv \
    --tables-to=results/tables \
    --plot-to=results/figures
'''

# import libraries/packages
import click
import os
import altair as alt
import pandas as pd

@click.command()
@click.option('--processed-training-data', type=str, help="Path to processed training data")
@click.option('--tables-to', type=str, help="Path to directory where the table will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
def main(processed_training_data, tables_to, plot_to):
    '''Plots the densities of each feature in the processed training data
        by class and displays them as a grid of plots. Also saves the plot.'''

    # read in training data
    train_df = pd.read_csv("data/processed/roster_train.csv")

    # Create processed data folder if it doesn't exist
    os.makedirs(plot_to, exist_ok=True)
    os.makedirs(tables_to, exist_ok=True)

    # Create info lookalike dataframe
    info = pd.DataFrame({
        "name": train_df.columns,
        "non-nulls": len(train_df)-train_df.isnull().sum().values,
        "nulls": train_df.isnull().sum().values,
        "type": train_df.dtypes.values
    })
    info.to_csv(os.path.join(tables_to, 'df_info.csv'))

    describe = train_df.describe()
    describe.to_csv(os.path.join(tables_to, 'df_describe.csv'))

    head = train_df.head()
    head.to_csv(os.path.join(tables_to, 'df_head.csv'))

    weight_chart = alt.Chart(train_df).mark_bar().encode(
        alt.X("weight_in_kilograms:Q", title="Weight (kg)").bin(),
        alt.Y("count()", title="Number of Players"),
        alt.Color("shoots_left", title="Shoots Left")
        ).properties(
            height=300,
            width=200,
            title="Distribution of Player Weights by Shooting Hand"
        ).facet(
            alt.Facet("shoots_left:N", title="Shoots Left or Not")
            )

    # Height distribution bar chart
    height_chart = alt.Chart(train_df).mark_bar().encode(
        alt.X("height_in_centimeters:Q", title="Height (cm)").bin(),
        alt.Y("count()", title="Number of Players"),
        alt.Color("shoots_left", title="Shoots Left")
        ).properties(
            height=300,
            width=200,
            title="Distribution of Player Heights by Shooting Hand"
        ).facet(
            alt.Facet("shoots_left:N", title="Shoots Left or Not")
        )

    combined_chart = alt.vconcat(weight_chart, height_chart).properties(
    title="Distribution of Player Weights and Heights by Shooting Hand"
    )
    combined_chart.save(os.path.join(plot_to, "combined_chart.png"))

# Call main function
if __name__ == '__main__':
    main()

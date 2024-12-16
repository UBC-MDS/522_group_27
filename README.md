# NHL player Shooting Hand Predictor
Authors: Dominic Lam, Michael Gelfand, Yunke Zhang, Jay Mangat

Demo of a data analysis project for DSCI 522 (Data Science workflows); a
course in the Master of Data Science program at the University of
British Columbia.

## About

This project aims to create a logistic regression model to aid in our 
analysis of whether a Canadian National Hockey League (NHL) player's height
and weight have any bearing on whether their shooting hand is left or
right. We used player data from the 1917 season NHL up to the 2023 season NHL 
season. One's shooting preference is the hand that is lower on the hockey 
stick so if your left hand is on the top of the stick and your right hand
is towards the bottom this is a right handed shot. Based on some exploratory 
data analysis, there is a overwhelming majority of left handed shooters even
though most players are right handed. We trained our model on this data and our
final classifier returned a score of 0.51. This follows our hypothesis that 
a NHL player's height and weight are not strong indicators of their shooting
preference.

We obtained the `nhl_rosters.csv` data set from [here](https://github.com/rfordatascience/tidytuesday/tree/master/data/2024/2024-01-09).
The data set is a part of 2024-01-09 release of tidytuesday, a weekly data 
science project available on GitHub. Each row represents a single player's
information including their height, weight, and shooting preference during
any given season with these players repeating over seasons if they were still
in the league.

## Report

The final report can be found
[here](https://github.com/UBC-MDS/522_group_27/blob/main/report/shooting_hand_predictor.pdf)

## Usage

### Setup

> Ensure Docker desktop application is running first

1. Clone this GitHub repository.

### Running the analysis

1. Navigate to the root of this project on your computer using the
   command line and enter the following command:

``` 
docker compose up
```

2. In the terminal, look for a URL that starts with 
`http://127.0.0.1:8888/lab?token=`
and copy that URL in to your web browser and go to the page.

3. To run the analysis,
open a terminal and run the following commands:
```
python scripts/download_data.py \
   --url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/refs/heads/main/data/2024/2024-01-09/nhl_rosters.csv" \
   --write_to=data/raw

python scripts/preprocess_and_validate.py \
   --raw-data=data/raw/nhl_rosters.csv \
   --data-to=data/processed \
   --preprocessor-to=results/models

python scripts/eda.py \
   --processed-training-data=data/processed/roster_train.csv \
   --tables-to=results/tables \
   --plot-to=results/figures

python scripts/shooting_hand_classifier.py \
   --training-data=data/processed/roster_train.csv \
   --test-data=data/processed/roster_test.csv \
   --preprocessor=results/models/roster_preprocessor.pickle \
   --pipeline-to=results/models \
   --plot-to=results/figures \
   --results-to=results/tables

quarto render report/shooting_hand_predictor.qmd --to html
quarto render report/shooting_hand_predictor.qmd --to pdf
```

### Clean up

1. To shut down the container and clean up the resources, 
type `Ctrl` + `C` in the terminal
where you launched the container, and then type `docker compose rm`

## Dependencies

- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)
- `jupyterlab` (version 4.0.0 or higher)
- `nb_conda_kernels` (version 2.3.1 or higher)
- Python and packages listed in [`environment.yml`](environment.yml)

### Adding a new dependency

1. Add the dependency to the `environment.yml` file on a new branch.

2. Run `conda-lock -k explicit --file environment.yml -p linux-64` to update the `conda-linux-64.lock` file.

2. Re-build the Docker image locally to ensure it builds and runs properly.

3. Push the changes to GitHub. A new Docker
   image will be built and pushed to Docker Hub automatically.

5. Send a pull request to merge the changes into the `main` branch. 

## License

The NHL player Shooting Hand Predictor roject report is licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/) and the software
is licensed under the [MIT license](https://opensource.org/license/MIT).
See [the license file](LICENSE.md) for more information on either of these
licenses. If re-using/re-mixing please provide attribution and link 
to this webpage.

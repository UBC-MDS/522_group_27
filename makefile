# Makefile
# Jay mangat, dec 2024

# This driver script creates a report of
# the shooting habits of NHL players and performs a analysis 
# on whether a player's body composition influences their shooting hand. 
# This script takes no arguments.

# example usage:
# make all

.PHONY: all clean

# run entire analysis
all: report/shooting_hand_predictor.html report/shooting_hand_predictor.pdf

data/raw/nhl_rosters.csv : scripts/download_data.py
	python scripts/download_data.py \
  --url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/refs/heads/main/data/2024/2024-01-09/nhl_rosters.csv" \
  --write_to=data/raw

data/processed/roster_train.csv data/processed/roster_test.csv results/models/roster_preprocessor.pickle: scripts/preprocess.py data/raw/nhl_rosters.csv
	python scripts/preprocess.py \
    --raw-data=data/raw/nhl_rosters.csv \
    --data-to=data/processed \
    --preprocessor-to=results/models

results/figures/combined_chart.png results/figures/confusion_matrix.png results/tables/df_describe.csv results/tables/df_head.csv results/tables/df_info.csv: scripts/eda.py data/processed/roster_train.csv data/processed/roster_test.csv results/models/roster_preprocessor.pickle
	python scripts/eda.py \
		--processed-training-data=data/processed/roster_train.csv \
		--tables-to=results/tables \
		--plot-to=results/figures

results/figures/confusion_matrix.png results/tables/test_scores.csv results/models/shooter_pipeline.pickle: scripts/shooting_hand_classifier.py results/figures/combined_chart.png results/figures/confusion_matrix.png results/tables/df_describe.csv results/tables/df_head.csv results/tables/df_info.csv
	python scripts/shooting_hand_classifier.py \
		--training-data=data/processed/roster_train.csv \
		--test-data=data/processed/roster_test.csv \
		--preprocessor=results/models/roster_preprocessor.pickle \
		--pipeline-to=results/models \
		--plot-to=results/figures \
		--results-to=results/tables

# write the report
report/shooting_hand_predictor.html report/shooting_hand_predictor.pdf: report/shooting_hand_predictor.qmd results/figures/confusion_matrix.png results/tables/test_scores.csv results/models/shooter_pipeline.pickle report/references.bib
	quarto render report/shooting_hand_predictor.qmd --to html
	quarto render report/shooting_hand_predictor.qmd --to pdf


clean :
	rm -f data/raw/nhl_rosters.csv \
		data/processed/roster_train.csv \
		data/processed/roster_test.csv \
		results/models/roster_preprocessor.pickle \
		results/figures/combined_chart.png \
		results/figures/confusion_matrix.png \
		results/tables/df_describe.csv \
		results/tables/df_head.csv \
		results/tables/df_info.csv \
		results/figures/confusion_matrix.png \
		results/tables/test_scores.csv \
		results/models/shooter_pipeline.pickle \
	rm -rf report/shooting_hand_predictor.pdf \
		report/shooting_hand_predictor.html \
		report/shooting_hand_predictor_files
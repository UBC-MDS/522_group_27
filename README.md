# NHL player Shooting Hand Predictor
Authors: Dominic Lam, Michael Gelfand, Yunke Zhang, Jay Mangat

In the main README.md file for this project you should include:
 - the project title 
 - the list of contributors/authors 
 Authors: Dominic lam, Michael gelfand, Yunke zhang, Jay mangat
 - a short summary of the project (view from 10,000 feet) 
 - how to run your data analysis 
 - a list of the dependencies needed to run your analysis 
 - the names of the licenses contained in LICENSE.md


Demo of a data analysis project for DSCI 522 (Data Science workflows); a
course in the Master of Data Science program at the University of
British Columbia.

## About

This project aims to create a logistic regression model to aid in our 
analysis of whether a Canadian National Hockey League (NHL) player's height
and weight have any bearing on whether their shooting hand is left or
right. We used player data from the 1999 season NHL up to the 2023 season NHL 
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
[here](missing)

## Usage

Install this environment as "YOURENV" with:
```bash
conda-lock install -n YOURENV conda-lock.yml
```

Run the analysis root of this repository:
``` bash
jupyter lab 
```

Open `nhl_shooting_report.ipynb` and choose
the following python kernal:
"Python [conda env:YOURENV]".

Select "Restart Kernel and Run All Cells..." under 
"Kernel" to ensure all cells are working correctly.

## Dependencies

- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)
- `jupyterlab` (version 4.0.0 or higher)
- `nb_conda_kernels` (version 2.3.1 or higher)
- Python and packages listed in [`environment.yml`](environment.yml)

## License

The Breast Cancer Predictor report contained herein are licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
See [the license file](LICENSE.md) for more information. . If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.

## References

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.”
University of California, Irvine, School of Information; Computer
Sciences. <http://archive.ics.uci.edu/ml>.

Street, W. Nick, W. H. Wolberg, and O. L. Mangasarian. 1993. “Nuclear
feature extraction for breast tumor diagnosis.” In *Biomedical Image
Processing and Biomedical Visualization*, edited by Raj S. Acharya and
Dmitry B. Goldgof, 1905:861–70. International Society for Optics;
Photonics; SPIE. <https://doi.org/10.1117/12.148698>.
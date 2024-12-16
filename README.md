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

3. Open a new terminal inside of Jupyter and enter the following command to reset the project to its initial state:
```
make clean
```

4. To run the analysis, enter the following command in the terminal:
```
make all
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
- [Docker](https://www.docker.com/)

### Adding a new dependency

1. Add the dependency to the `environment.yml` file on a new branch.

2. Run `conda-lock -k explicit --file environment.yml -p linux-64` to update the `conda-linux-64.lock` file.

2. Re-build the Docker image locally to ensure it builds and runs properly.

3. Push the changes to GitHub. A new Docker
   image will be built and pushed to Docker Hub automatically.

5. Send a pull request to merge the changes into the `main` branch. 

## Testing

### Running tests

To run the developer function tests, run the commands above to start the docker container and open the Jupyter Lab terminal. Then, ensure you are in the project root directory and run the `pytest` command in terminal.

## Support

If you have any questions, issues, or feedback regarding this project, feel free to reach out to us:

- **GitHub Issues**: For bug reports, feature requests, or general inquiries, please open an issue in this repository [here](https://github.com/UBC-MDS/522_group_27/issues).
- **Email**: You can email the project team at [thlam0519@gmail.com](mailto:thlam0519@gmail.com).
- **Discussions**: Join our GitHub Discussions [here](https://github.com/UBC-MDS/522_group_27/discussions) to engage with the community and share ideas.

We are here to help and value your contributions!

## License

The NHL player Shooting Hand Predictor roject report is licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/) and the software
is licensed under the [MIT license](https://opensource.org/license/MIT).
See [the license file](LICENSE.md) for more information on either of these
licenses. If re-using/re-mixing please provide attribution and link 
to this webpage.

# Belly Rubb documentation!

## Description

This data science project analyzes customer ordering patterns at a local restaurant using data collected through Square. The goal is to uncover key behavioral trends and build a predictive model to forecast daily sales. The project simulates a real-world workflow by incorporating automated data pipelines, feature engineering, machine learning modeling, and dashboard reporting.

## Project Objectives

- Analyze customer behavior to understand why sales are higher on certain days or during specific time periods.
- Identify patterns related to day of week, time of day, promotions, or external factors (e.g. holidays, weather).
- Build a predictive model to forecast daily sales volume.
- Create a lightweight automated pipeline for continuous model updates and insights delivery.
- Develop an interactive dashboard for non-technical stakeholders.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

## Project Organization

```
├── LICENSE                     <- Open-source license if one is chosen
|
├── Makefile                    <- Makefile with convenience commands.
|
├── README.md                   <- The top-level README for developers using this project.
|
├── data
│   ├── external                <- Data from third party sources.
│   ├── interim                 <- Intermediate data that has been transformed.
│   ├── processed               <- The final, canonical data sets for modeling.
│   └── raw                     <- The original, immutable data dump.
|
│── app
|   ├── config.py               <- Store useful variables and configuration.
|   ├── db_models.py            <- ORM model for 'access_tokens' table.
|   ├── db.py                   <- SQLAlchemy database engine setup.
|   ├── pkce_flow.py            <- OAUTH2 PKCE flow.
│   └── templates
|       ├── callback.html       <- HTML template for callback success page.
|       └── home.html           <- HTML template for homepage.
|
├── docs                        <- A default mkdocs project; see www.mkdocs.org for details
│
├── models                      <- Trained and serialized models.
│
├── notebooks                   <- Jupyter notebooks.
│
├── pyproject.toml              <- Project configuration file with package metadata.
│
├── references                  <- Data dictionaries, manuals, and other explanatory materials.
│
├── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures                 <- Generated graphics and figures to be used in reporting.
│
├── environment.yml             <- The environment file for reproducing the analysis environment.
│
├── setup.cfg                   <- Configuration file for flake8.
│
└── belly_rubb                  <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes belly_rubb a Python module.
    │
    ├── config.py               <- Store useful variables and configuration.
    │
    ├── dataset.py              <- Scripts to download or generate data.
    │
    ├── features.py             <- Code to create features for modeling.
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```
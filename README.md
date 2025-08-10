# Belly Rubb

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This data science project analyzes customer ordering patterns at a local restaurant using data collected through Square. The goal is to uncover key behavioral trends and build a predictive model to forecast daily sales. The project simulates a real-world workflow by incorporating automated data pipelines, feature engineering, machine learning modeling, and dashboard reporting.

## 🔍 Project Objectives

- Analyze customer behavior to understand why sales are higher on certain days or during specific time periods.
- Identify patterns related to day of week, time of day, promotions, or external factors (e.g. holidays, weather).
- Build a predictive model to forecast daily sales volume.
- Create a lightweight automated pipeline for continuous model updates and insights delivery.
- Develop an interactive dashboard for non-technical stakeholders.

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
---

## ⚙️ Features & Tools

| Component              | Tool / Library                      |
|------------------------|-------------------------------------|
| Data Source            | Square (CSV/API)                    |
| Language               | Python                              |
| Data Storage           | SQLite                              |
| Data Pipeline          |                                     |
| EDA & Visualization    | pandas, matplotlib, seaborn         |
| Machine Learning       | scikit-learn                        |
| Deployment             |                                     |
| Version Control        | Git + GitHub                        |

---

## 📈 Key Insights

*Note: Insights will be shared after model evaluation is complete.*

---

## ✅ Project Development Checklist
- ✅ Determine data mining goals.
- ✅ Establish OAuth flow and connection to Square API.
- ☐ Collect and clean data.
- ☐ Perform exploratory data analysis (EDA) to gain insights and assess the business problem and context.
- ☐ Transform data and engineer features to prepare for modeling.
- ☐ Develop a model to address project's objectives.
- ☐ Evaluate model performance.
- ☐ Deploy model.

---

## 🚀 How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/ajamkotc/belly_rubb
    cd belly_rubb
    ```
2. Set up the Python virtual environment:
    ```bash
    conda env create -f environment.yml
    conda activate belly_rubb
    ```
3. Set up the `.env` file:
    ```bash
    SQUARE_APPLICATION_ID=your_square_application_id
    SQUARE_APPLICATION_SECRET=your_square_application_secret
    REDIRECT_URI=http://localhost:5000/callback
    ```
    - `SQUARE_APPLICATION_ID` and `SQUARE_APPLICATION_SECRET` can be obtained from your [Square Developer Dashboard](https://developer.squareup.com/docs/devtools/developer-dashboard).
    - `REDIRECT_URI` should match the redirect URL configured in your Square application settings.
    - For local development use `http://localhost:5000/callback`.
    - NEVER commit `.env` files to version control. Use `.gitignore` to exclude them.
3. Run the Pipeline
   ```bash
    # Run data processing scripts
    python src/data/dataset.py

    # Train the model
    python src/models/train_model.py
    ```
4. Launch the Dashboard

### ⚠️ Access Disclaimer

> This project demonstrates how to authenticate with the Square API and store access tokens securely using OAuth 2.0.
>
> You must use your own Square application credentials to run this app. Access to restaurant data requires permission from the account owner and valid API credentials.
>
> **Do not share or commit any real Square secrets or tokens.**
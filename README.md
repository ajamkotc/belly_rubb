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
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         belly_rubb and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── belly_rubb   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes belly_rubb a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
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
| Data Storage           | SQLite (optionally PostgreSQL/Supabase) |
| Data Pipeline          | `schedule`, `cron`, or `Airflow`    |
| EDA & Visualization    | pandas, matplotlib, seaborn         |
| Machine Learning       | scikit-learn, XGBoost               |
| Deployment             | Streamlit                           |
| Version Control        | Git + GitHub                        |

---

## 📈 Key Insights (Preview)

- Sales peak on [X] and dip on [Y].
- Average order value increases during [time period].
- [Specific product or category] drives the most consistent revenue.
- Predictive model achieves an MAE of [value], helping forecast sales with [accuracy]%.

*Note: Final insights will be shared after model evaluation is complete.*

---

## 🚀 How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/restaurant-sales-prediction.git
    cd restaurant-sales-prediction
    ```
2. Set up the Environment:
    ```bash
    conda env create -f environment.yml
    conda activate belly_rubb
    ```
3. Run the Pipeline
   ```bash
    # Run data processing scripts
    python src/data/dataset.py

    # Train the model
    python src/models/train_model.py
    ```
4. Launch the Dashboard
    
--------


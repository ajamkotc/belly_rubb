Getting started
===============

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

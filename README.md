# AI Data Analytics & Prediction Dashboard

A Streamlit dashboard for uploading CSV data, inspecting data quality, creating interactive charts, and generating a simple linear trend forecast.

## Features
- CSV upload and preview
- Row, column, and missing-value metrics
- Descriptive statistics
- Interactive scatter plot
- Basic linear trend forecast

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Forecast assumptions
The baseline forecast uses row position as the independent variable. It assumes rows are already ordered chronologically and extrapolates a straight line. It is not suitable for seasonal, irregular, or highly nonlinear time series without additional modeling and validation.

## Suggested extensions
- Add data cleaning and type inference.
- Add time-series models with train/test evaluation.
- Add natural-language questions over the dataset.
- Add downloadable charts and analysis reports.

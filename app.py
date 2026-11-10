import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Data Analytics", page_icon="📊", layout="wide")
st.title("📊 AI Data Analytics & Prediction Dashboard")
st.caption("Explore CSV data, visualize numeric columns, and run a simple trend forecast.")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded:
    try:
        df = pd.read_csv(uploaded)
        st.subheader("Dataset overview")
        a, b, c = st.columns(3)
        a.metric("Rows", f"{len(df):,}")
        b.metric("Columns", len(df.columns))
        c.metric("Missing cells", int(df.isna().sum().sum()))
        st.dataframe(df.head(100), use_container_width=True)
        with st.expander("Descriptive statistics"):
            st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

        numeric = df.select_dtypes(include="number").columns.tolist()
        if numeric:
            st.subheader("Interactive visualization")
            x_options = ["(row index)"] + df.columns.tolist()
            x_col = st.selectbox("X-axis", x_options)
            y_col = st.selectbox("Numeric Y-axis", numeric)
            plot_df = df.copy()
            if x_col == "(row index)":
                plot_df["row_index"] = range(len(plot_df))
                x_use = "row_index"
            else:
                x_use = x_col
            fig = px.scatter(plot_df, x=x_use, y=y_col, title=f"{y_col} by {x_col}", trendline="ols" if len(plot_df) > 2 else None)
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Simple linear trend forecast")
            st.caption("Uses row order as time. Only meaningful when rows are already chronologically ordered.")
            target = st.selectbox("Column to forecast", numeric, key="forecast")
            periods = st.slider("Future rows", 1, 30, 5)
            if st.button("Generate forecast"):
                clean = df[target].dropna().reset_index(drop=True)
                if len(clean) < 3:
                    st.error("At least three non-missing numeric values are required.")
                else:
                    import numpy as np
                    x = np.arange(len(clean))
                    slope, intercept = np.polyfit(x, clean.to_numpy(), 1)
                    future_x = np.arange(len(clean), len(clean) + periods)
                    pred = slope * future_x + intercept
                    forecast_df = pd.DataFrame({"Future row": range(1, periods + 1), "Predicted value": pred})
                    st.dataframe(forecast_df, use_container_width=True)
                    st.line_chart(pd.DataFrame({"Observed": clean.to_numpy(), "Fitted": slope*x + intercept}))
        else:
            st.warning("No numeric columns found. Upload a dataset with numeric values to create charts.")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
else:
    st.info("Upload a CSV to explore the dataset. Try a sample sales, finance, or sensor dataset.")

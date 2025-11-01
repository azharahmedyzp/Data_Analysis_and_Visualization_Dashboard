import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# App Configuration
st.set_page_config(page_title="Data Analysis and Visualization Dashboard", layout="wide")
st.title("📊 Data Analysis and Visualization Dashboard")

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Upload Dataset", "Data Summary", "Visualization", "Missing Data", "Download Report", "About"]
)

# Session State for Data
if 'df' not in st.session_state:
    st.session_state.df = None

# Upload Section
if menu == "Upload Dataset":
    st.header("Upload Your CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success("✅ File uploaded successfully!")

            st.subheader("Dataset Preview")
            st.write(df.head())

            st.markdown(f"**Rows:** {df.shape[0]}  |  **Columns:** {df.shape[1]}")
            st.write(df.dtypes)
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Data Summary
elif menu == "Data Summary":
    st.header("📈 Data Summary")
    df = st.session_state.df

    if df is not None:
        st.subheader("Descriptive Statistics")
        st.write(df.describe())

        st.subheader("Numeric Analysis (NumPy)")
        numeric_cols = df.select_dtypes(include=np.number).columns
        if len(numeric_cols) > 0:
            summary_data = {
                'Mean': df[numeric_cols].mean(),
                'Median': df[numeric_cols].median(),
                'Std Dev': df[numeric_cols].std()
            }
            st.dataframe(pd.DataFrame(summary_data))
        else:
            st.warning("No numeric columns available.")
    else:
        st.warning("Please upload a dataset first.")

# Visualization Section
elif menu == "Visualization":
    st.header("📊 Data Visualization")
    df = st.session_state.df

    if df is not None:
        st.sidebar.subheader("Visualization Options")
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Bar Chart", "Box Plot", "Heatmap", "Scatter Plot", "Pairplot"])

        if plot_type == "Histogram":
            col = st.selectbox("Select numeric column", df.select_dtypes(include=np.number).columns)
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

        elif plot_type == "Bar Chart":
            col = st.selectbox("Select categorical column", df.select_dtypes(exclude=np.number).columns)
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind='bar', ax=ax)
            st.pyplot(fig)

        elif plot_type == "Box Plot":
            col = st.selectbox("Select numeric column", df.select_dtypes(include=np.number).columns)
            fig, ax = plt.subplots()
            sns.boxplot(x=df[col], ax=ax)
            st.pyplot(fig)

        elif plot_type == "Heatmap":
            fig, ax = plt.subplots()
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

        elif plot_type == "Scatter Plot":
            x_col = st.selectbox("X-axis", df.select_dtypes(include=np.number).columns)
            y_col = st.selectbox("Y-axis", df.select_dtypes(include=np.number).columns)
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
            st.pyplot(fig)

        elif plot_type == "Pairplot":
            fig = sns.pairplot(df.select_dtypes(include=np.number))
            st.pyplot(fig)
    else:
        st.warning("Please upload a dataset first.")

# Missing Data Section
elif menu == "Missing Data":
    st.header("🩹 Missing Data Handling")
    df = st.session_state.df

    if df is not None:
        st.subheader("Missing Values Overview")
        missing = df.isnull().sum()
        st.write(missing[missing > 0])

        if missing.sum() > 0:
            fig, ax = plt.subplots()
            sns.heatmap(df.isnull(), cbar=False, ax=ax)
            st.pyplot(fig)

            action = st.radio("Select an action", ["None", "Drop missing rows", "Fill missing with mean"])

            if action == "Drop missing rows":
                df.dropna(inplace=True)
                st.session_state.df = df
                st.success("✅ Missing rows dropped.")

            elif action == "Fill missing with mean":
                df.fillna(df.mean(numeric_only=True), inplace=True)
                st.session_state.df = df
                st.success("✅ Missing values filled with column means.")
        else:
            st.info("No missing data found.")
    else:
        st.warning("Please upload a dataset first.")

# Download Report Section
elif menu == "Download Report":
    st.header("📥 Download Descriptive Report")
    df = st.session_state.df

    if df is not None:
        desc = df.describe()
        csv = desc.to_csv().encode('utf-8')
        st.download_button(
            label="Download Summary CSV",
            data=csv,
            file_name='summary_report.csv',
            mime='text/csv'
        )
    else:
        st.warning("Please upload and analyze a dataset first.")

# About Section
elif menu == "About":
    st.header("ℹ️ About This Project")
    st.write("""
    **Data Analysis and Visualization Dashboard**

    This interactive dashboard is built using:
    - **Pandas** and **NumPy** for data processing
    - **Matplotlib** and **Seaborn** for visualizations
    - **Streamlit** for the user interface

    Features:
    - Upload and explore datasets
    - View summary statistics
    - Create interactive visualizations
    - Handle missing data
    - Download reports

    Developed as a **Python Mini Project** for demonstrating data analytics workflows.
    """)


# python -m streamlit run Data_Analysis_and_Visualization_Dashboard.py
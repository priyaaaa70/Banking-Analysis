
import streamlit as st
import pandas as pd
from utils import (
    load_data,
    calculate_pivot_tables,
    plot_age_distribution,
    plot_avg_call_duration_by_marital,
    plot_age_boxplot_by_job,
)

st.set_page_config(page_title="Banking Data Analysis", layout="wide")
st.title("Banking Dataset Exploration, Pivot Tables & Visualization")

# Load dataset
df = load_data('data/bank.csv')
results = calculate_pivot_tables(df)

# Create tabs for better organization
tab_data, tab_insights, tab_viz = st.tabs(["📋 Data Preview", "📊 Key Insights", "📈 Visualizations"])

# --- Tab 1: Data Preview ---
with tab_data:
    st.header("Dataset Preview")
    st.dataframe(df.head())

    # Download dataset as CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Dataset as CSV",
        data=csv,
        file_name="bank_data.csv",
        mime="text/csv",
    )

# --- Tab 2: Key Insights ---
with tab_insights:
    st.header("Key Insights")

    # KPI cards in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Clients Attracted (Subscribed)",
            value=f"{results['attracted_share'].get('yes', 0)*100:.2f}%",
            delta=f"{(results['attracted_share'].get('yes', 0) - results['attracted_share'].get('no', 0))*100:.2f}% vs Not Subscribed",
        )
        st.caption("Percentage of clients who subscribed to the term deposit.")

    with col2:
        st.metric(
            label="Avg Call Duration (Attracted Clients)",
            value=f"{results['avg_call_duration']:.2f} seconds",
        )
        st.caption("Average duration of calls for clients who subscribed.")

    with col3:
        st.metric(
            label="Avg Age (Attracted & Unmarried)",
            value=f"{results['avg_age_unmarried']:.2f} years",
        )
        st.caption("Average age of attracted clients who are single.")

    st.markdown("---")

    # Mean numerical features table with gradient
    st.subheader("Mean Numerical Features Among Attracted Clients")
    mean_df = (
        pd.Series(results['mean_numerical'])
        .to_frame(name="Mean Value")
        .style.background_gradient(cmap="Blues")
        .format("{:.2f}")
    )
    st.dataframe(mean_df, height=200)

    st.markdown("---")

    # Average age and call duration by job type with explanation
    st.subheader("Average Age and Call Duration by Job Type")
    st.write(
        "This table shows how client age and call duration vary across different employment types. "
        "Use this insight to tailor marketing campaigns."
    )
    st.dataframe(results['avg_by_job'].style.format("{:.2f}"), height=300)

# --- Tab 3: Visualizations ---
with tab_viz:
    st.header("Visualizations")

    with st.expander("Age Distribution by Subscription Status"):
        fig1 = plot_age_distribution(df)
        st.pyplot(fig1)

    with st.expander("Average Call Duration by Marital Status"):
        fig2 = plot_avg_call_duration_by_marital(df)
        st.pyplot(fig2)

    with st.expander("Age Distribution by Job Type"):
        fig3 = plot_age_boxplot_by_job(df)
        st.pyplot(fig3)


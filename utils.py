import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    # Dataset uses ';' as separator
    df = pd.read_csv("data/bank.csv")
    return df



def calculate_pivot_tables(df):
    # Share of clients attracted (subscribed)
    attracted_share = df['deposit'].value_counts(normalize=True).to_dict()

    # Mean numerical features among attracted clients
    attracted_clients = df[df['deposit'] == 'yes']
    mean_numerical = attracted_clients.select_dtypes(include=np.number).mean().to_dict()

    # Average call duration for attracted clients
    avg_call_duration = attracted_clients['duration'].mean()

    # Average age among attracted and unmarried clients
    unmarried_attracted = attracted_clients[attracted_clients['marital'] == 'single']
    avg_age_unmarried = unmarried_attracted['age'].mean()

    # Average age and call duration for different types of client employment
    avg_by_job = df.groupby('job')[['age', 'duration']].mean()

    return {
        'attracted_share': attracted_share,
        'mean_numerical': mean_numerical,
        'avg_call_duration': avg_call_duration,
        'avg_age_unmarried': avg_age_unmarried,
        'avg_by_job': avg_by_job
    }

def plot_age_distribution(df):
    plt.figure(figsize=(8,5))
    sns.histplot(data=df, x='age', hue='deposit', multiple='stack', palette='Set2')
    plt.title('Age Distribution by Subscription Status')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.tight_layout()
    return plt.gcf()

def plot_avg_call_duration_by_marital(df):
    plt.figure(figsize=(6,4))
    avg_duration = df.groupby('marital')['duration'].mean().reset_index()
    sns.barplot(data=avg_duration, x='marital', y='duration', palette='Set1')
    plt.title('Average Call Duration by Marital Status')
    plt.ylabel('Duration (seconds)')
    plt.tight_layout()
    return plt.gcf()

def plot_age_boxplot_by_job(df):
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='job', y='age', palette='Set3')
    plt.xticks(rotation=45)
    plt.title('Age Distribution by Job Type')
    plt.tight_layout()
    return plt.gcf()

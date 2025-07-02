"""
NYC Taxi Data Exploratory Data Analysis (EDA) Module

This module performs comprehensive exploratory data analysis on cleaned NYC taxi data.
It generates statistical summaries, distribution plots, and relationship visualizations
to understand patterns in taxi usage, fare structures, and temporal trends.

Features:
- Data quality assessment (types, nulls, basic statistics)
- Distribution analysis (distance, duration, fare amounts)
- Relationship analysis (fare vs distance)
- Temporal pattern analysis (hourly, daily trends)
- Categorical data exploration (payment types, locations)

Author: NYC Taxi Project
Date: 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

# Configure plot style for consistent, professional visualizations
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)  # Default figure size

def run_eda(db_path: str):
    """
    Perform comprehensive exploratory data analysis on NYC taxi data.
    
    This function loads data from SQLite database and generates:
    - Statistical summaries and data quality reports
    - Distribution plots for key numerical variables
    - Scatter plots to explore relationships
    - Time-based analysis for usage patterns
    - Categorical variable analysis
    
    Args:
        db_path (str): Path to SQLite database containing cleaned taxi data
    
    Returns:
        None: Generates plots saved as PNG files in current directory
    """
    # Data Loading and Initial Assessment
    print("🔌 Connecting to database...")
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql("SELECT * FROM trips", engine)
    print(f"📊 Loaded {len(df):,} rows for analysis\n")

    # === DATA QUALITY ASSESSMENT ===
    print("=" * 50)
    print("📋 DATA TYPES ASSESSMENT")
    print("=" * 50)
    print(df.dtypes)
    
    print("\n" + "=" * 50)
    print("🔍 MISSING VALUES ANALYSIS")
    print("=" * 50)
    null_summary = df.isnull().sum()
    null_percentage = (null_summary / len(df) * 100).round(2)
    null_report = pd.DataFrame({
        'Missing Count': null_summary,
        'Missing Percentage': null_percentage
    })
    print(null_report[null_report['Missing Count'] > 0])
    
    print("\n" + "=" * 50)
    print("📈 DESCRIPTIVE STATISTICS")
    print("=" * 50)
    print(df.describe())

    # === DATA RANGE AND UNIT VALIDATION ===
    print("\n" + "=" * 50)
    print("🎯 DATA RANGE VALIDATION")
    print("=" * 50)
    print(f"Trip distance: {df['trip_distance'].min():.2f} - {df['trip_distance'].max():.2f} miles")
    print(f"Trip duration: {df['duration_minutes'].min():.2f} - {df['duration_minutes'].max():.2f} minutes")
    print(f"Fare amount: ${df['fare_amount'].min():.2f} - ${df['fare_amount'].max():.2f}")
    print(f"Passenger count: {df['passenger_count'].min()} - {df['passenger_count'].max()} passengers")

    # === DISTRIBUTION ANALYSIS ===
    print("\n" + "=" * 50)
    print("📊 GENERATING DISTRIBUTION PLOTS")
    print("=" * 50)
    
    # Trip Distance Distribution
    print("📏 Analyzing trip distance distribution...")
    plt.figure(figsize=(12, 6))
    sns.histplot(df['trip_distance'], bins=50, kde=True, alpha=0.7)
    plt.title("Trip Distance Distribution", fontsize=16, fontweight='bold')
    plt.xlabel("Distance (Miles)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.axvline(df['trip_distance'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df["trip_distance"].mean():.2f} miles')
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_trip_distance.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Trip Duration Distribution
    print("⏱️ Analyzing trip duration distribution...")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=df['duration_minutes'])
    plt.title("Trip Duration Distribution (Box Plot)", fontsize=16, fontweight='bold')
    plt.xlabel("Duration (Minutes)", fontsize=12)
    plt.tight_layout()
    plt.savefig("plot_duration_boxplot.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Fare Amount Distribution
    print("💰 Analyzing fare amount distribution...")
    plt.figure(figsize=(12, 6))
    sns.histplot(df['fare_amount'], bins=50, kde=True, alpha=0.7)
    plt.title("Fare Amount Distribution", fontsize=16, fontweight='bold')
    plt.xlabel("Fare Amount (USD)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.axvline(df['fare_amount'].mean(), color='red', linestyle='--',
                label=f'Mean: ${df["fare_amount"].mean():.2f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_fare_amount.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # === RELATIONSHIP ANALYSIS ===
    print("\n" + "=" * 50)
    print("🔗 ANALYZING VARIABLE RELATIONSHIPS")
    print("=" * 50)
    
    print("📈 Examining fare vs distance relationship...")
    plt.figure(figsize=(12, 8))
    # Sample data for plotting if dataset is large (performance optimization)
    plot_df = df.sample(n=min(5000, len(df)), random_state=42)
    sns.scatterplot(data=plot_df, x='trip_distance', y='fare_amount', alpha=0.6)
    plt.title("Fare Amount vs. Trip Distance", fontsize=16, fontweight='bold')
    plt.xlabel("Distance (Miles)", fontsize=12)
    plt.ylabel("Fare Amount (USD)", fontsize=12)
    
    # Add correlation coefficient to plot
    correlation = df['trip_distance'].corr(df['fare_amount'])
    plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
             transform=plt.gca().transAxes, fontsize=12,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    plt.tight_layout()
    plt.savefig("plot_fare_vs_distance.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # === TEMPORAL PATTERN ANALYSIS ===
    print("\n" + "=" * 50)
    print("⏰ ANALYZING TEMPORAL PATTERNS")
    print("=" * 50)
    
    # Prepare datetime features for temporal analysis
    print("🕐 Extracting time-based features...")
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['weekday'] = df['pickup_datetime'].dt.dayofweek  # 0=Monday, 6=Sunday

    # Hourly Distribution Analysis
    print("📅 Analyzing hourly trip patterns...")
    plt.figure(figsize=(14, 6))
    hourly_counts = df['hour'].value_counts().sort_index()
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette='viridis')
    plt.title("Trip Distribution by Hour of Day", fontsize=16, fontweight='bold')
    plt.xlabel("Hour of Day", fontsize=12)
    plt.ylabel("Number of Trips", fontsize=12)
    # Add peak hour annotation
    peak_hour = hourly_counts.idxmax()
    plt.axvline(peak_hour, color='red', linestyle='--', alpha=0.7,
                label=f'Peak Hour: {peak_hour}:00')
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_hourly_distribution.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Weekly Distribution Analysis
    print("📆 Analyzing weekly trip patterns...")
    plt.figure(figsize=(12, 6))
    weekday_counts = df['weekday'].value_counts().sort_index()
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sns.barplot(x=[weekday_names[i] for i in weekday_counts.index], 
                y=weekday_counts.values, palette='Set2')
    plt.title("Trip Distribution by Day of Week", fontsize=16, fontweight='bold')
    plt.xlabel("Day of Week", fontsize=12)
    plt.ylabel("Number of Trips", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plot_weekday_distribution.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # === CATEGORICAL DATA ANALYSIS ===
    print("\n" + "=" * 50)
    print("🏷️ CATEGORICAL DATA EXPLORATION")
    print("=" * 50)
    
    print("💳 Payment type distribution:")
    payment_dist = df['payment_type'].value_counts()
    print(payment_dist)
    print(f"Payment type percentages:")
    print((payment_dist / len(df) * 100).round(2))

    print("\n🗺️ Top 10 pickup locations by frequency:")
    location_dist = df['PULocationID'].value_counts().head(10)
    print(location_dist)

    print("\n" + "=" * 50)
    print("✅ EDA COMPLETED SUCCESSFULLY")
    print("=" * 50)
    print("📁 Generated visualization files:")
    plot_files = [
        "plot_trip_distance.png",
        "plot_duration_boxplot.png", 
        "plot_fare_amount.png",
        "plot_fare_vs_distance.png",
        "plot_hourly_distribution.png",
        "plot_weekday_distribution.png"
    ]
    for plot_file in plot_files:
        if os.path.exists(plot_file):
            print(f"  ✅ {plot_file}")
        else:
            print(f"  ❌ {plot_file} (failed to generate)")

if __name__ == "__main__":
    """
    Main execution block for standalone EDA script usage.
    Runs complete exploratory data analysis on NYC taxi database.
    """
    run_eda("db/nyc_taxi.db")

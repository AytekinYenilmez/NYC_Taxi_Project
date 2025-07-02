"""
NYC Taxi EDA Report Generator

This module generates comprehensive HTML reports for NYC taxi data analysis.
It creates self-contained HTML reports with embedded visualizations that are
optimized for PDF conversion without external dependencies.

Key Features:
- Base64 image embedding for PDF compatibility
- Professional HTML templating with Jinja2
- Statistical summaries and data quality assessment
- Self-contained reports (no external CSS/JS dependencies)

The module addresses common PDF generation issues by:
- Embedding images as base64 data URLs
- Using inline CSS instead of external stylesheets
- Avoiding external resource dependencies

Author: NYC Taxi Project
Date: 2025
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from jinja2 import Environment, FileSystemLoader
import os
import base64

def generate_eda_report(db_path: str, output_html: str = "reports/eda_report.html"):
    """
    Generate a comprehensive HTML report with embedded visualizations.
    
    This function creates a self-contained HTML report that includes:
    - Dataset overview (shape, data types, missing values)
    - Descriptive statistics
    - Embedded visualization plots (as base64 data URLs)
    
    The report is designed to be PDF-friendly by avoiding external dependencies
    and embedding all images directly in the HTML.
    
    Args:
        db_path (str): Path to SQLite database containing processed taxi data
        output_html (str): Output path for HTML report. Defaults to "reports/eda_report.html"
    
    Returns:
        None: Generates HTML file at specified output path
    """
    print("🔌 Connecting to database for report generation...")
    
    # Load data from SQLite database
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql("SELECT * FROM trips", engine)
    print(f"📊 Loaded {len(df):,} records for analysis")

    # Prepare datetime features for temporal analysis
    print("⏰ Preparing temporal features...")
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['weekday'] = df['pickup_datetime'].dt.day_name()

    # Ensure output directories exist
    os.makedirs("plots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Generate visualization plots
    print("📈 Generating visualization plots...")
    
    # Plot 1: Trip Distance Distribution
    print("  📏 Trip distance distribution...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['trip_distance'], bins=50, kde=True)
    plt.title("Trip Distance Distribution")
    plt.xlabel("Distance (Miles)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("plots/trip_distance.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Plot 2: Trip Duration Distribution
    print("  ⏱️ Trip duration distribution...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['duration_minutes'], bins=50, kde=True)
    plt.title("Trip Duration Distribution")
    plt.xlabel("Duration (Minutes)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("plots/duration_distribution.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Plot 3: Fare vs Distance Relationship
    print("  💰 Fare vs distance analysis...")
    plt.figure(figsize=(10, 6))
    # Sample data for performance if dataset is large
    plot_sample = df.sample(n=min(5000, len(df)), random_state=42)
    sns.scatterplot(x='trip_distance', y='fare_amount', data=plot_sample, alpha=0.5)
    plt.title("Fare vs Distance")
    plt.xlabel("Distance (Miles)")
    plt.ylabel("Fare Amount (USD)")
    plt.tight_layout()
    plt.savefig("plots/fare_vs_distance.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Plot 4: Hourly Trip Distribution
    print("  🕐 Hourly trip patterns...")
    plt.figure(figsize=(12, 6))
    sns.countplot(x='hour', data=df, palette='viridis')
    plt.title("Trips by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Trips")
    plt.tight_layout()
    plt.savefig("plots/hourly_distribution.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Plot 5: Weekly Trip Distribution
    print("  📅 Weekly trip patterns...")
    plt.figure(figsize=(12, 6))
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sns.countplot(x='weekday', data=df, order=weekday_order, palette='Set2')
    plt.title("Trips by Weekday")
    plt.xlabel("Day of Week")
    plt.ylabel("Number of Trips")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/weekday_distribution.png", dpi=300, bbox_inches='tight')
    plt.clf()

    # Load Jinja2 template
    print("📝 Loading HTML template...")
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    # Prepare plot data for embedding
    print("🖼️ Embedding images as base64 for PDF compatibility...")
    plots = [
        "plots/trip_distance.png",
        "plots/duration_distribution.png",
        "plots/fare_vs_distance.png",
        "plots/hourly_distribution.png",
        "plots/weekday_distribution.png"
    ]
    
    # Convert images to base64 data URLs for embedded HTML
    embedded_plots = []
    for plot in plots:
        abs_path = os.path.abspath(plot)
        if os.path.exists(abs_path):
            try:
                with open(abs_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    # Create data URL for embedding in HTML (PDF-safe)
                    data_url = f"data:image/png;base64,{img_data}"
                    embedded_plots.append({
                        'name': plot.split("/")[-1].replace("_", " ").replace(".png", "").title(),
                        'data': data_url
                    })
                    print(f"  ✅ Embedded {plot}")
            except Exception as e:
                print(f"  ❌ Failed to embed {plot}: {e}")
        else:
            print(f"  ⚠️ Plot file not found: {abs_path}")

    # Render HTML template with data
    print("🎨 Rendering HTML report...")
    html_output = template.render(
        shape=f"{df.shape[0]:,} rows × {df.shape[1]} columns",
        dtypes=df.dtypes.to_string(),
        nulls=df.isnull().sum().to_string(),
        describe=df.describe().to_html(classes="table table-striped", table_id="stats-table"),
        plots=embedded_plots
    )

    # Save HTML report
    print(f"💾 Saving HTML report to {output_html}...")
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"✅ EDA report successfully generated: {output_html}")
    print(f"📊 Report includes {len(embedded_plots)} embedded visualizations")
    print(f"📁 Report size: {os.path.getsize(output_html):,} bytes")

"""
NYC Taxi Data Pipeline - Prefect Workflow

This module implements a complete data pipeline using Prefect for workflow orchestration.
The pipeline performs ETL operations, exploratory data analysis, and automated report 
generation with HTML and PDF outputs.

Pipeline Stages:
1. ETL Task: Extract, transform, and load taxi data from parquet to SQLite
2. EDA Task: Generate exploratory data analysis visualizations
3. Report Task: Create HTML report with embedded analytics
4. PDF Conversion Task: Convert HTML report to PDF with fallback options

Key Features:
- Prefect workflow orchestration with logging
- Robust error handling and fallback mechanisms
- PDF generation with multiple engine support (wkhtmltopdf, weasyprint)
- Base64 image embedding for self-contained reports
- Windows-optimized PDF generation settings

Author: NYC Taxi Project
Date: 2025
"""

from prefect import flow, task, get_run_logger
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pdfkit
import sys

# 🔧 Add project root to module path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.eda_report_generator import generate_eda_report

# Configure plot style for consistent visualizations
sns.set_theme(style="whitegrid")

@task
def etl_task(parquet_path: str, db_path: str, sample_size: int = 10000) -> str:
    """
    Extract, Transform, and Load NYC taxi data from parquet to SQLite.
    
    This task performs comprehensive data cleaning and transformation:
    - Loads raw parquet data
    - Filters invalid records (zero passengers/distance)
    - Converts datetime columns to proper format
    - Calculates trip duration metrics
    - Applies optional sampling for performance
    - Saves cleaned data to SQLite database
    
    Args:
        parquet_path (str): Path to input parquet file
        db_path (str): Path for output SQLite database
        sample_size (int): Number of rows to sample (None for full dataset)
    
    Returns:
        str: Path to created database file
    """
    logger = get_run_logger()
    logger.info(f"🚀 Starting ETL process - Loading data from {parquet_path}")
    
    # Extract: Load raw data from parquet file
    df = pd.read_parquet(parquet_path)
    logger.info(f"📊 Initial dataset shape: {df.shape}")

    # Transform: Apply data quality filters
    logger.info("🧹 Applying data cleaning transformations...")
    
    # Remove records with invalid passenger count
    initial_count = len(df)
    df = df[df['passenger_count'] > 0]
    logger.info(f"   ✅ Removed {initial_count - len(df)} records with zero passengers")
    
    # Remove records with invalid trip distance
    initial_count = len(df)
    df = df[df['trip_distance'] > 0]
    logger.info(f"   ✅ Removed {initial_count - len(df)} records with zero distance")

    # Convert datetime columns for temporal analysis
    logger.info("📅 Converting datetime columns...")
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # Calculate trip duration in minutes
    logger.info("⏱️ Calculating trip duration metrics...")
    df['duration_minutes'] = (
        df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    ).dt.total_seconds() / 60

    # Remove trips with invalid duration
    initial_count = len(df)
    df = df[df['duration_minutes'] > 0]
    logger.info(f"   ✅ Removed {initial_count - len(df)} records with invalid duration")

    # Apply sampling if specified (for performance optimization)
    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)
        logger.info(f"🎯 Sampled dataset to {sample_size} rows for performance")

    # Load: Save to SQLite database with chunked processing
    logger.info(f"💾 Saving cleaned data to SQLite database: {db_path}")
    engine = create_engine(f"sqlite:///{db_path}")
    
    try:
        df.to_sql(
            'trips',                    # Table name
            engine,                     # Database connection
            if_exists='replace',        # Replace existing table
            index=False,                # Don't save DataFrame index
            method='multi',             # Multi-row INSERT for performance
            chunksize=500              # Chunk size to avoid SQLite limits
        )
        logger.info(f"✅ ETL complete: {len(df):,} rows saved to SQLite database")
    except Exception as e:
        logger.error(f"❌ Database save failed: {e}")
        raise
    
    return db_path


@task
def eda_task(db_path: str):
    """
    Perform exploratory data analysis and generate visualization plots.
    
    This task connects to the SQLite database, loads the cleaned data,
    and generates a comprehensive set of visualizations including:
    - Trip distance distribution
    - Trip duration distribution  
    - Fare vs distance scatter plot
    - Hourly trip distribution
    - Weekly trip distribution
    
    All plots are saved to the 'plots' directory for use in reporting.
    
    Args:
        db_path (str): Path to SQLite database containing cleaned data
    
    Returns:
        None: Saves plots as PNG files to plots/ directory
    """
    logger = get_run_logger()
    logger.info(f"📊 Loading data from {db_path} for EDA")
    
    # Load data from SQLite database
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql("SELECT * FROM trips", engine)

    # Prepare datetime features for temporal analysis
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['weekday'] = df['pickup_datetime'].dt.day_name()  # Monday, Tuesday...

    # Ensure plots directory exists
    os.makedirs("plots", exist_ok=True)

    # Generate Trip Distance Distribution
    logger.info("📏 Plotting trip distance histogram")
    sns.histplot(df['trip_distance'], bins=50, kde=True)
    plt.title("Trip Distance Distribution")
    plt.xlabel("Miles")
    plt.savefig("plots/trip_distance.png")
    plt.clf()

    # Generate Trip Duration Distribution
    logger.info("⏱️ Plotting trip duration distribution")
    sns.histplot(df['duration_minutes'], bins=50, kde=True)
    plt.title("Trip Duration Distribution")
    plt.xlabel("Minutes")
    plt.savefig("plots/duration_distribution.png")
    plt.clf()

    # Generate Fare vs Distance Scatter Plot
    logger.info("💰 Plotting fare vs distance scatterplot")
    sns.scatterplot(x='trip_distance', y='fare_amount', data=df, alpha=0.5)
    plt.title("Fare vs. Trip Distance")
    plt.xlabel("Distance (miles)")
    plt.ylabel("Fare (USD)")
    plt.savefig("plots/fare_vs_distance.png")
    plt.clf()

    # Generate Hourly Distribution Plot
    logger.info("🕐 Plotting hourly distribution")
    sns.countplot(x='hour', data=df)
    plt.title("Trips by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Trip Count")
    plt.savefig("plots/hourly_distribution.png")
    plt.clf()

    # Generate Weekly Distribution Plot
    logger.info("📅 Plotting weekday distribution")
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sns.countplot(x='weekday', data=df, order=weekday_order)
    plt.title("Trips by Weekday")
    plt.xlabel("Weekday")
    plt.ylabel("Trip Count")
    plt.savefig("plots/weekday_distribution.png")
    plt.clf()

    logger.info("✅ EDA complete. Plots saved in /plots folder.")

@task
def report_task(db_path: str):
    """
    Generate HTML report with embedded visualizations and analysis.
    
    This task uses the EDA report generator to create a comprehensive
    HTML report containing:
    - Dataset overview and statistics
    - Data quality assessment
    - Embedded visualizations (base64 encoded for PDF compatibility)
    
    Args:
        db_path (str): Path to SQLite database containing analyzed data
        
    Returns:
        None: Generates HTML report at reports/eda_report.html
    """
    logger = get_run_logger()
    logger.info("📄 Generating comprehensive HTML report...")
    generate_eda_report(db_path)
    logger.info("✅ EDA report generated at reports/eda_report.html")


@task
def convert_html_to_pdf_task(html_path: str, output_pdf_path: str):
    """
    Convert HTML report to PDF format with robust error handling.
    
    This task attempts to convert the HTML report to PDF using wkhtmltopdf
    as the primary engine, with weasyprint as a fallback option. The task
    includes Windows-specific optimizations and handles common PDF generation
    issues like external resource loading and image embedding.
    
    Args:
        html_path (str): Path to input HTML file
        output_pdf_path (str): Path for output PDF file
        
    Returns:
        None: Creates PDF file or logs fallback message
    """
    logger = get_run_logger()
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    # Windows-optimized wkhtmltopdf configuration
    # These options resolve common issues with PDF generation on Windows
    options = {
        'page-size': 'A4',                    # Standard page size
        'margin-top': '0.75in',              # Consistent margins
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",                  # Handle special characters
        'no-outline': None,                   # Disable PDF outline
        'enable-local-file-access': None,     # Allow local file access
        'disable-external-links': None,       # Disable external links
        'print-media-type': None,             # Use print CSS styles
        'disable-smart-shrinking': None,      # Prevent content shrinking
        'zoom': 1.0,                         # No zoom scaling
        'dpi': 300,                          # High resolution
        'image-quality': 100,                # Maximum image quality
        'disable-javascript': None,           # Disable JS for stability
        'load-error-handling': 'ignore',     # Ignore loading errors
        'load-media-error-handling': 'ignore' # Ignore media errors
    }
    
    try:
        # Primary PDF generation using wkhtmltopdf
        logger.info("🔄 Converting HTML to PDF using wkhtmltopdf...")
        pdfkit.from_file(html_path, output_pdf_path, options=options)
        logger.info(f"✅ PDF successfully generated at {output_pdf_path}")
        
        # Verify the PDF was created and has content
        if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
            logger.info(f"✅ PDF file verified: {os.path.getsize(output_pdf_path):,} bytes")
        else:
            logger.error("❌ PDF file was not created or is empty")
            
    except Exception as e:
        logger.error(f"❌ PDF generation failed: {str(e)}")
        
        # Fallback: Try alternative PDF generation using weasyprint
        try:
            logger.info("🔄 Attempting alternative PDF generation with weasyprint...")
            import weasyprint
            
            # Read HTML content
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Generate PDF with weasyprint (better CSS support)
            html_doc = weasyprint.HTML(
                string=html_content, 
                base_url=os.path.dirname(os.path.abspath(html_path))
            )
            html_doc.write_pdf(output_pdf_path)
            logger.info(f"✅ PDF successfully generated using weasyprint at {output_pdf_path}")
            
        except ImportError:
            logger.warning("⚠️  weasyprint not available. Install with: pip install weasyprint")
            logger.info("📝 HTML report is available at: " + html_path)
        except Exception as e2:
            logger.error(f"❌ Alternative PDF generation also failed: {str(e2)}")
            logger.info("📝 HTML report is available at: " + html_path)

@flow(name="NYC Taxi ETL + EDA Flow")
def taxi_pipeline():
    """
    Main Prefect workflow orchestrating the entire NYC taxi data pipeline.
    
    This flow coordinates all pipeline tasks in the correct sequence:
    1. ETL Task: Cleans and loads raw taxi data into SQLite
    2. EDA Task: Generates exploratory visualizations
    3. Report Task: Creates comprehensive HTML report
    4. PDF Task: Converts HTML to PDF format
    
    The flow uses Prefect's dependency management to ensure proper
    task execution order and error handling.
    
    Returns:
        None: Orchestrates pipeline execution and logging
    """
    logger = get_run_logger()
    logger.info("🚀 Starting NYC Taxi Data Pipeline")
    
    # Define file paths for pipeline artifacts
    parquet_path = "data/yellow_tripdata_2023-01.parquet"
    db_path = "db/nyc_taxi.db"
    html_path = "reports/eda_report.html"
    pdf_path = "reports/eda_report.pdf"
    
    # Task 1: ETL - Extract, Transform, Load data
    logger.info("📊 Phase 1: ETL Processing")
    db_result = etl_task(parquet_path, db_path, sample_size=10000)
    
    # Task 2: EDA - Generate visualizations (depends on ETL completion)
    logger.info("📈 Phase 2: Exploratory Data Analysis")
    eda_task(db_result)
    
    # Task 3: Report Generation (depends on EDA completion)
    logger.info("📄 Phase 3: Report Generation")
    report_task(db_result)
    
    # Task 4: PDF Conversion (depends on report completion)
    logger.info("📋 Phase 4: PDF Conversion")
    convert_html_to_pdf_task(html_path, pdf_path)
    
    logger.info("🎉 NYC Taxi Data Pipeline completed successfully!")


if __name__ == "__main__":
    """
    Direct script execution entry point.
    Runs the complete NYC taxi data pipeline when executed as a standalone script.
    """
    taxi_pipeline()

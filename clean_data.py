"""
NYC Taxi Data ETL Pipeline - Data Cleaning Module

This module handles the Extract, Transform, Load (ETL) process for NYC taxi data.
It reads parquet files, applies data cleaning transformations, and saves the 
cleaned data to a SQLite database for further analysis.

Author: NYC Taxi Project
Date: 2025
"""

import pandas as pd
from sqlalchemy import create_engine

def run_etl(parquet_path: str, db_path: str, sample_size: int = 10000):
    """
    Extract, Transform, and Load NYC taxi data from parquet to SQLite database.
    
    This function performs comprehensive data cleaning including:
    - Filtering out invalid records (zero passengers, zero distance)
    - Converting datetime columns to proper format
    - Calculating trip duration in minutes
    - Optional sampling for performance
    - Saving to SQLite database with proper chunking
    
    Args:
        parquet_path (str): Path to the input parquet file
        db_path (str): Path where SQLite database will be created/updated
        sample_size (int, optional): Number of rows to sample. Defaults to 10000.
                                   Set to None to process full dataset.
    
    Returns:
        None: Data is saved to SQLite database
    """
    print(f"Loading data from {parquet_path}...")
    
    # Extract: Load data from parquet file
    df = pd.read_parquet(parquet_path)
    print(f"Initial shape: {df.shape}")

    # Transform: Basic data cleaning operations
    print("Applying data quality filters...")
    
    # Remove records with zero or negative passenger count (invalid trips)
    df = df[df['passenger_count'] > 0]
    
    # Remove records with zero or negative trip distance (invalid trips)
    df = df[df['trip_distance'] > 0]

    # Ensure datetime columns are properly formatted for time-based analysis
    print("Converting datetime columns...")
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # Calculate trip duration in minutes for analysis
    print("Calculating trip duration...")
    df['duration_minutes'] = (
        df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    ).dt.total_seconds() / 60

    # Remove trips with negative or zero duration (data quality issue)
    df = df[df['duration_minutes'] > 0]
    print(f"After cleaning: {df.shape}")

    # Optional sampling for performance optimization on large datasets
    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)  # Fixed seed for reproducibility
        print(f"Sampled to {sample_size} rows for performance")

    # Load: Save cleaned data to SQLite database
    print(f"Saving to SQLite DB at {db_path}...")
    engine = create_engine(f"sqlite:///{db_path}")

    try:
        # Use chunked writing to avoid memory issues with large datasets
        df.to_sql(
            'trips',                    # Table name
            engine,                     # Database connection
            if_exists='replace',        # Replace existing table
            index=False,                # Don't save DataFrame index
            method='multi',             # Use multi-row INSERT for speed
            chunksize=500              # Process in chunks to avoid SQLite limits
        )
        print(f"✅ Successfully saved {len(df)} rows to 'trips' table.")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        raise

if __name__ == "__main__":
    """
    Main execution block for standalone script usage.
    Processes NYC taxi data with default parameters.
    """
    run_etl(
        parquet_path="data/yellow_tripdata_2023-01.parquet",  # Input data file
        db_path="db/nyc_taxi.db",                             # Output database
        sample_size=10000  # Adjust or set to None for full dataset
    )



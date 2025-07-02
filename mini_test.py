"""
NYC Taxi Database Connection Test

A simple test script to verify database connectivity and data availability.
This script performs a quick sanity check on the processed taxi data by
retrieving and displaying a small sample of records.

Purpose:
- Validate SQLite database connection
- Confirm data exists in the 'trips' table
- Display sample records for manual verification

Author: NYC Taxi Project
Date: 2025
"""

from sqlalchemy import create_engine
import pandas as pd

def test_database_connection():
    """
    Test database connectivity and display sample records.
    
    This function connects to the NYC taxi SQLite database and retrieves
    a small sample of records to verify that:
    1. Database file exists and is accessible
    2. The 'trips' table contains data
    3. Data format appears correct
    
    Returns:
        None: Prints sample data to console
    """
    try:
        # Create database connection
        print("🔌 Connecting to NYC Taxi database...")
        engine = create_engine('sqlite:///db/nyc_taxi.db')
        
        # Query for sample records
        print("📊 Retrieving sample records...")
        query = "SELECT * FROM trips LIMIT 5"
        df = pd.read_sql(query, engine)
        
        # Display results
        print("✅ Connection successful! Sample data:")
        print("=" * 80)
        print(df.to_string(index=False))
        print("=" * 80)
        print(f"📈 Database contains {len(pd.read_sql('SELECT COUNT(*) as count FROM trips', engine).iloc[0, 0]):,} total records")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure to run the ETL pipeline first to create the database.")

if __name__ == "__main__":
    """
    Main execution block for database testing.
    """
    test_database_connection()

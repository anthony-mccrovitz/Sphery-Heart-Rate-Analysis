#!/usr/bin/env python3
"""
Script to update the master CSV with all current station data peaks CSV files.
This script will combine all individual user station data peaks CSV files into the master CSV.
"""

import pandas as pd
import os
import glob
from pathlib import Path

def update_master_csv():
    """Update the master CSV with all current station data peaks CSV files."""
    
    # Define paths
    processed_dir = Path("output/processed")
    master_csv_path = processed_dir / "MASTER_sphere_heart_rate_data.csv"
    
    # Find all station data peaks CSV files
    station_csv_pattern = processed_dir / "*_station_data_peaks.csv"
    station_csv_files = glob.glob(str(station_csv_pattern))
    
    print(f"Found {len(station_csv_files)} station data peaks CSV files:")
    for file in station_csv_files:
        print(f"  - {os.path.basename(file)}")
    
    # Read and combine all station data peaks CSV files
    all_dataframes = []
    
    for csv_file in station_csv_files:
        try:
            df = pd.read_csv(csv_file)
            all_dataframes.append(df)
            print(f"Successfully read {os.path.basename(csv_file)} with {len(df)} rows")
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    
    if not all_dataframes:
        print("No valid CSV files found!")
        return
    
    # Combine all dataframes
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    print(f"\nCombined data has {len(combined_df)} total rows")
    
    # Sort by user_id and station_number for better organization
    combined_df = combined_df.sort_values(['user_id', 'station_number'])
    
    # Save the updated master CSV
    combined_df.to_csv(master_csv_path, index=False)
    print(f"\nUpdated master CSV saved to: {master_csv_path}")
    print(f"Total rows in master CSV: {len(combined_df)}")
    
    # Print summary by user
    print("\nSummary by user:")
    user_counts = combined_df['user_id'].value_counts().sort_index()
    for user_id, count in user_counts.items():
        print(f"  User {user_id}: {count} stations")

if __name__ == "__main__":
    update_master_csv() 
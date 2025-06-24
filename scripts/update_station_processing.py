#!/usr/bin/env python
"""
Script to update station processing logic in all user data exploration notebooks.
This script fixes the following issues:
1. Updates process_station_data function to properly handle station 3 data
2. Ensures station durations are calculated correctly from timestamps
3. Adds debug information to verify correct station durations
4. Copies the fixed process_station_data function to save_station_data and DataFrame inspection cells
"""

import os
import re
import json
import glob
import nbformat
from nbformat.v4 import new_notebook, new_code_cell

def fix_process_station_data(cell_source, user_id):
    """Fix the process_station_data function in a cell."""
    # Replace the segment definition for station cutoffs
    pattern1 = r"segment = df\[\(df\['elapsed_min'\] >= start_min\) & \(df\['elapsed_min'\] < end_min\)\]"
    replacement1 = """# For station 3, ensure we use the full range to the end of the session
        if i == 3:
            segment = df[(df['elapsed_min'] >= start_min)]
        else:
            # For other stations, use the defined cutoffs
            segment = df[(df['elapsed_min'] >= start_min) & (df['elapsed_min'] <= end_min)]"""
    cell_source = re.sub(pattern1, replacement1, cell_source)
    
    # Add debug information after the segment definition
    pattern2 = r"if segment\.empty:\s+print\(f\"Warning: No data found for Station \{i\}\"\)\s+continue\s+"
    replacement2 = """if segment.empty:
            print(f"Warning: No data found for Station {i}")
            continue
        
        # Debug information to verify station duration calculation
        actual_duration = (segment['timestamp'].iloc[-1] - segment['timestamp'].iloc[0]).total_seconds() / 60
        cutoff_duration = end_min - start_min
        print(f"Station {i} - Cutoff duration: {cutoff_duration:.2f} min, Actual data duration: {actual_duration:.2f} min")
        print(f"  First point: {segment['elapsed_min'].iloc[0]:.2f} min, Last point: {segment['elapsed_min'].iloc[-1]:.2f} min")
            
        # Calculate the exact duration from the timestamp difference for all stations
        station_duration = (segment['timestamp'].iloc[-1] - segment['timestamp'].iloc[0]).total_seconds() / 60
        if i == 3:
            print(f"  Station {i} exact duration: {station_duration:.2f} minutes")
            """
    cell_source = re.sub(pattern2, replacement2, cell_source)
    
    # Replace the station_duration_min calculation
    pattern3 = r"'station_duration_min': \(segment\['timestamp'\]\.iloc\[-1\] - segment\['timestamp'\]\.iloc\[0\]\)\.total_seconds\(\) / 60,"
    replacement3 = "'station_duration_min': station_duration,"
    cell_source = re.sub(pattern3, replacement3, cell_source)
    
    # Replace the user_id if needed
    if user_id:
        pattern_user = r"'user_id': \d+,"
        replacement_user = f"'user_id': {user_id},"
        cell_source = re.sub(pattern_user, replacement_user, cell_source)
    
    return cell_source

def create_fixed_process_station_data(user_id):
    """Create a fixed version of the process_station_data function for a specific user."""
    return f"""# Copy the process_station_data function here to ensure it's available
def process_station_data():
    station_rows = []
    
    for i, (start_min, end_min) in enumerate(cutoffs, 1):
        # For station 3, ensure we use the full range to the end of the session
        if i == 3:
            segment = df[(df['elapsed_min'] >= start_min)]
        else:
            # For other stations, use the defined cutoffs
            segment = df[(df['elapsed_min'] >= start_min) & (df['elapsed_min'] <= end_min)]
        
        if segment.empty:
            print(f"Warning: No data found for Station {{i}}")
            continue
        
        # Debug information to verify station duration calculation
        actual_duration = (segment['timestamp'].iloc[-1] - segment['timestamp'].iloc[0]).total_seconds() / 60
        cutoff_duration = end_min - start_min
        print(f"Station {{i}} - Cutoff duration: {{cutoff_duration:.2f}} min, Actual data duration: {{actual_duration:.2f}} min")
        print(f"  First point: {{segment['elapsed_min'].iloc[0]:.2f}} min, Last point: {{segment['elapsed_min'].iloc[-1]:.2f}} min")
            
        # Calculate the exact duration from the timestamp difference for all stations
        station_duration = (segment['timestamp'].iloc[-1] - segment['timestamp'].iloc[0]).total_seconds() / 60
        if i == 3:
            print(f"  Station {{i}} exact duration: {{station_duration:.2f}} minutes")
            
        station_row = {{
            # User and session info
            'user_id': {user_id},
            'gender': 'NA',
            'circuit_type': 'NA',
            
            # Station info
            'station_number': i,
            'station_name': 'NA',
            
            # Session timing and HR data
            'session_start_time': df['timestamp'].iloc[0],
            'session_end_time': df['timestamp'].iloc[-1],
            'session_duration_min': session_duration_min,
            'session_avg_hr': sessions_avg_hr,
            'session_max_hr': session_max_hr,
            
            # Station timing and HR data
            'station_start_time': segment['timestamp'].iloc[0],
            'station_end_time': segment['timestamp'].iloc[-1],
            'station_duration_min': station_duration,
            'station_avg_hr': segment['heart_rate'].mean(),
            'station_max_hr': segment['heart_rate'].max(),
            
            # Per-station ratings
            'motivation': 'NA',  # 1-5 scale
            'enjoyment': 'NA',   # 1-5 scale (previously 'fun')
            'team_experience': 'NA',  # 1-5 scale (only for exergame duos)
            'subjective_physical_exertion': 'NA',  # Borg RPE 1-10 scale
            'subjective_cognitive_exertion': 'NA',  # 1-5 scale
            
            # Final evaluation (same for all stations of a user)
            'overall_experience': 'NA',  # 1-5 scale
            'overall_motivation': 'NA',  # 1-5 scale
            'feedback': 'NA',  # Free text
            
            # Additional data
            'sports_exp': 'NA',
            'gaming_exp': 'NA',
            'data_quality': 'Good',
            'notes': ''
        }}
        station_rows.append(station_row)
    
    # Create and display DataFrame
    station_df = pd.DataFrame(station_rows)
    display(station_df)
    
    # Return the DataFrame for further use
    return station_df"""

def fix_save_station_data(cell_source, user_id):
    """Fix the save_station_data function by adding the fixed process_station_data function."""
    # Add the fixed process_station_data function
    fixed_func = create_fixed_process_station_data(user_id)
    
    # Replace "# Function to save station data to CSV" with the fixed function
    pattern = r"# STEP 7: Save processed data to CSV\s+# Function to save station data to CSV"
    replacement = f"# STEP 7: Save processed data to CSV\n\n{fixed_func}\n\n# Function to save station data to CSV"
    cell_source = re.sub(pattern, replacement, cell_source)
    
    # Update the comment in the save_station_data function
    pattern2 = r"# Get the latest station data"
    replacement2 = "# Get the latest station data using the local process_station_data function"
    cell_source = re.sub(pattern2, replacement2, cell_source)
    
    # Update the output path if needed
    if user_id:
        pattern3 = r"output_path = 'output/processed/user_\d+_station_data\.csv'"
        replacement3 = f"output_path = 'output/processed/user_{user_id}_station_data.csv'"
        cell_source = re.sub(pattern3, replacement3, cell_source)
    
    return cell_source

def fix_dataframe_inspection(cell_source, user_id):
    """Fix the DataFrame inspection cell by adding the fixed process_station_data function."""
    # Add the fixed process_station_data function
    fixed_func = create_fixed_process_station_data(user_id)
    
    # Replace "# First, get the latest processed data" with the fixed function
    pattern = r"# Display full DataFrame for inspection\s+# This will show all columns and rows without truncation\s+\n# First, get the latest processed data"
    replacement = f"# Display full DataFrame for inspection\n# This will show all columns and rows without truncation\n\n{fixed_func}\n\n# First, get the latest processed data"
    cell_source = re.sub(pattern, replacement, cell_source)
    
    return cell_source

def update_notebook(notebook_path):
    """Update a single notebook with the fixed station processing logic."""
    print(f"Processing {notebook_path}...")
    
    # Extract user ID from the filename
    filename = os.path.basename(notebook_path)
    match = re.search(r'user_(\d+)_data_exploration', filename)
    if not match:
        print(f"  Warning: Could not extract user ID from {filename}, skipping")
        return False
    
    user_id = int(match.group(1))
    print(f"  User ID: {user_id}")
    
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Process each cell
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            # Fix process_station_data function
            if "def process_station_data():" in cell.source and "segment = df[(df['elapsed_min'] >= start_min) & (df['elapsed_min']" in cell.source:
                print(f"  Fixing process_station_data in cell {i}")
                cell.source = fix_process_station_data(cell.source, user_id)
            
            # Fix save_station_data function
            elif "def save_station_data():" in cell.source and "# Get the latest station data" in cell.source:
                print(f"  Fixing save_station_data in cell {i}")
                cell.source = fix_save_station_data(cell.source, user_id)
            
            # Fix DataFrame inspection cell
            elif "# Display full DataFrame for inspection" in cell.source and "inspection_df = process_station_data()" in cell.source:
                print(f"  Fixing DataFrame inspection in cell {i}")
                cell.source = fix_dataframe_inspection(cell.source, user_id)
    
    # Save the updated notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print(f"  Updated {notebook_path}")
    return True

def main():
    """Main function to update all user data exploration notebooks."""
    # Find all user data exploration notebooks
    notebooks = glob.glob("notebooks/user_*_data_exploration.ipynb")
    
    if not notebooks:
        print("No user data exploration notebooks found.")
        return
    
    print(f"Found {len(notebooks)} notebooks to update.")
    
    # Update each notebook
    updated_count = 0
    for notebook in notebooks:
        if update_notebook(notebook):
            updated_count += 1
    
    print(f"Updated {updated_count} out of {len(notebooks)} notebooks.")

if __name__ == "__main__":
    main() 
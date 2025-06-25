#!/usr/bin/env python3
"""
Script to update all notebooks to include user metadata and calories burned.

This script modifies all user_*_data_exploration.ipynb files to:
1. Load user metadata (age, gender, height, weight, champ_number)
2. Handle the updated TCX parser that now returns calories
3. Include these fields in the output CSVs

Run this after filling in the metadata/user_metadata.csv file.
"""

import os
import json
import glob
import re
from pathlib import Path

def update_metadata_fields():
    """Update all notebooks to use USER_ID for metadata loading and print statements."""
    # Find all user notebooks
    notebook_pattern = "notebooks/user_*_data_exploration.ipynb"
    notebooks = glob.glob(notebook_pattern)
    
    # Filter out any checkpoint files or backups
    notebooks = [nb for nb in notebooks if 
                '.ipynb_checkpoints' not in nb and 
                not nb.endswith('.bak')]
    
    # Remove duplicates and sort
    notebooks = sorted(set(notebooks))
    
    if not notebooks:
        print(f"No notebooks found matching {notebook_pattern}")
        return False
    
    print(f"Found {len(notebooks)} notebooks to update")
    
    # Process each notebook
    for notebook_path in notebooks:
        print(f"\nProcessing {notebook_path}...")
        
        # Extract user ID from filename
        user_id = os.path.basename(notebook_path).split('_')[1]
        
        try:
            # Load the notebook
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
            
            # Create backup
            backup_path = f"{notebook_path}.metadata.bak"
            print(f"  Creating backup at {backup_path}")
            with open(backup_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            
            # Track changes
            changes_made = False
            
            # 1. Add metadata loading code after USER_ID definition
            user_id_cell_idx = None
            has_metadata_loading = False
            
            # 2. Update TCX parser call to handle calories
            tcx_parser_cell_idx = None
            has_calories_variable = False
            
            # 3. Find process_station_data function to update
            process_data_cell_idx = None
            
            # First pass: analyze notebook structure
            for i, cell in enumerate(notebook_data['cells']):
                if cell['cell_type'] == 'code':
                    cell_source = ''.join(cell['source'])
                    
                    # Check for USER_ID definition
                    if "USER_ID = " in cell_source or f"user_id': {user_id}" in cell_source:
                        user_id_cell_idx = i
                    
                    # Check if metadata loading is already present
                    if "metadata = pd.read_csv" in cell_source and "user_metadata.csv" in cell_source:
                        has_metadata_loading = True
                    
                    # Find TCX parser call
                    if "parse_tcx_to_df" in cell_source and "df, session_total_sec" in cell_source:
                        tcx_parser_cell_idx = i
                    
                    # Check if calories variable exists
                    if "calories_burned" in cell_source:
                        has_calories_variable = True
                    
                    # Find process_station_data function
                    if "def process_station_data" in cell_source:
                        process_data_cell_idx = i
            
            # Make necessary changes
            
            # 1. Add metadata loading if not present
            if not has_metadata_loading and user_id_cell_idx is not None:
                print("  Adding metadata loading code")
                
                # Create metadata loading cell
                metadata_cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Load user metadata\n",
                        "import pandas as pd\n",
                        "try:\n",
                        "    metadata_df = pd.read_csv('metadata/user_metadata.csv')\n",
                        f"    user_meta = metadata_df[metadata_df['user_id'] == USER_ID]\n",
                        "    if not user_meta.empty:\n",
                        "        user_meta = user_meta.iloc[0]\n",
                        "        age = user_meta['age'] if not pd.isna(user_meta['age']) else None\n",
                        "        gender = user_meta['gender'] if not pd.isna(user_meta['gender']) else None\n",
                        "        height_cm = user_meta['height_cm'] if not pd.isna(user_meta['height_cm']) else None\n",
                        "        weight_kg = user_meta['weight_kg'] if not pd.isna(user_meta['weight_kg']) else None\n",
                        "        champ_number = user_meta['champ_number'] if not pd.isna(user_meta['champ_number']) else None\n",
                        "        print(f\"Loaded metadata for user {USER_ID}: age={age}, gender={gender}, height={height_cm}cm, weight={weight_kg}kg, champ={champ_number}\")\n",
                        "    else:\n",
                        "        print(f\"No metadata found for user {USER_ID}\")\n",
                        "        age = gender = height_cm = weight_kg = champ_number = None\n",
                        "except Exception as e:\n",
                        "    print(f\"Error loading metadata: {e}\")\n",
                        "    age = gender = height_cm = weight_kg = champ_number = None\n"
                    ],
                    "outputs": []
                }
                
                # Insert cell after USER_ID definition
                notebook_data['cells'].insert(user_id_cell_idx + 1, metadata_cell)
                changes_made = True
                print("  Added metadata loading code")
                
                # Adjust indices for other cells that come after
                if tcx_parser_cell_idx and tcx_parser_cell_idx > user_id_cell_idx:
                    tcx_parser_cell_idx += 1
                if process_data_cell_idx and process_data_cell_idx > user_id_cell_idx:
                    process_data_cell_idx += 1
            
            # 2. Update TCX parser call to handle calories
            if tcx_parser_cell_idx is not None:
                cell = notebook_data['cells'][tcx_parser_cell_idx]
                cell_source = ''.join(cell['source'])
                
                if "df, session_total_sec, sessions_avg_hr, session_max_hr = parse_tcx_to_df" in cell_source:
                    print("  Updating TCX parser call to handle calories")
                    
                    # Update parser call to include calories
                    updated_source = cell_source.replace(
                        "df, session_total_sec, sessions_avg_hr, session_max_hr = parse_tcx_to_df",
                        "df, session_total_sec, sessions_avg_hr, session_max_hr, calories_burned = parse_tcx_to_df"
                    )
                    
                    # Add print statement for calories
                    if "print(f\"Average HR:" in updated_source:
                        updated_source = updated_source.replace(
                            "print(f\"Average HR: {sessions_avg_hr:.1f} bpm, Maximum HR: {session_max_hr} bpm\")",
                            "print(f\"Average HR: {sessions_avg_hr:.1f} bpm, Maximum HR: {session_max_hr} bpm, Calories: {calories_burned}\")"
                        )
                    
                    # Update the cell
                    notebook_data['cells'][tcx_parser_cell_idx]['source'] = updated_source.split('\n')
                    # Add newline to each line except the last
                    for j in range(len(notebook_data['cells'][tcx_parser_cell_idx]['source']) - 1):
                        notebook_data['cells'][tcx_parser_cell_idx]['source'][j] += '\n'
                    
                    changes_made = True
                    print("  Updated TCX parser call to include calories")
            
            # 3. Update process_station_data function to include metadata fields
            if process_data_cell_idx is not None:
                cell = notebook_data['cells'][process_data_cell_idx]
                cell_source = ''.join(cell['source'])
                
                # Check if we need to update the function
                if "'user_id'" in cell_source and not "'age'" in cell_source:
                    print("  Updating process_station_data function")
                    
                    # Find where user info is added to the station_row dictionary
                    if "'user_id':" in cell_source:
                        # Split at the user_id line
                        parts = cell_source.split("'user_id':", 1)
                        if len(parts) == 2:
                            # Find the end of the user section (usually after circuit_type)
                            user_section = parts[1].split("'station_number':", 1)
                            if len(user_section) == 2:
                                # Add metadata fields after user_id and before station_number
                                updated_source = parts[0] + "'user_id':" + user_section[0]
                                
                                # Add the new fields
                                metadata_fields = """
            # User metadata
            'age': age,
            'gender': gender,
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'champ_number': champ_number,
            'calories_burned': calories_burned,
            
            """
                                
                                # Insert the metadata fields before station_number
                                updated_source += metadata_fields + "'station_number':" + user_section[1]
                                
                                # Update the cell
                                notebook_data['cells'][process_data_cell_idx]['source'] = updated_source.split('\n')
                                # Add newline to each line except the last
                                for j in range(len(notebook_data['cells'][process_data_cell_idx]['source']) - 1):
                                    notebook_data['cells'][process_data_cell_idx]['source'][j] += '\n'
                                
                                changes_made = True
                                print("  Updated process_station_data function to include metadata fields")
            
            # Save the notebook if changes were made
            if changes_made:
                with open(notebook_path, 'w') as f:
                    json.dump(notebook_data, f, indent=1)
                print(f"  Saved changes to {notebook_path}")
            else:
                print(f"  No changes needed for {notebook_path}")
                
        except Exception as e:
            print(f"  ERROR processing {notebook_path}: {str(e)}")
    
    return True

if __name__ == "__main__":
    update_metadata_fields()
    print("\nFinished updating notebooks with metadata fields") 
#!/usr/bin/env python3
"""
Script to fix alignment parameters in all user data exploration notebooks.
This ensures that the alignment parameters set in the interactive tool
are carried over to the station cutoffs visualization function.
"""

import os
import sys
import json
import re
import glob
from pathlib import Path

def fix_alignment_parameters():
    """Update all notebooks to pass alignment parameters between functions."""
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
        print(f"Processing {notebook_path}...")
        
        # Load the notebook
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
        
        # Create backup
        backup_path = f"{notebook_path}.alignment.bak"
        print(f"  Creating backup at {backup_path}")
        with open(backup_path, 'w') as f:
            json.dump(notebook_data, f, indent=1)
        
        # Find and update the cells
        updated = False
        
        # First, add global variables after the imports
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code' and "# STEP 1: Setup and imports" in ''.join(cell['source']):
                # Create a new cell for global variables
                global_vars_cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Global variables to store alignment parameters\n",
                        "# These will be set by the interactive alignment tool and used by the station visualization\n",
                        "global_x_offset = 0\n",
                        "global_x_scale = 1\n",
                        "global_y_min = 0\n",
                        "global_y_max = 200\n",
                        "global_alpha = 0.5\n"
                    ],
                    "outputs": []
                }
                
                # Insert the new cell after the imports
                notebook_data['cells'].insert(i+1, global_vars_cell)
                updated = True
                print("  Added global variables cell")
                break
        
        # Update the alignment function to store parameters in global variables
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Update the update_alignment function
                if "def update_alignment" in cell_source and "interact(" in cell_source:
                    # Add code to store parameters in global variables
                    updated_source = cell_source.replace(
                        "def update_alignment(x_offset=0, x_scale=1, y_min=0, y_max=200, alpha=0.5):",
                        "def update_alignment(x_offset=0, x_scale=1, y_min=0, y_max=200, alpha=0.5):\n    global global_x_offset, global_x_scale, global_y_min, global_y_max, global_alpha\n    \n    # Store parameters in global variables\n    global_x_offset = x_offset\n    global_x_scale = x_scale\n    global_y_min = y_min\n    global_y_max = y_max\n    global_alpha = alpha"
                    )
                    
                    # Split the source back into lines
                    notebook_data['cells'][i]['source'] = updated_source.split('\n')
                    # Add newline character at the end of each line except the last one
                    for j in range(len(notebook_data['cells'][i]['source']) - 1):
                        notebook_data['cells'][i]['source'][j] += '\n'
                    
                    updated = True
                    print("  Updated alignment function to store parameters globally")
                
                # Update the station visualization function to use global parameters
                elif "def visualize_with_stations" in cell_source and "# Function to visualize stations with current cutoffs" in cell_source:
                    # Update the function to use global parameters
                    if "def visualize_with_stations(station_cutoffs, x_offset=0, x_scale=1, y_min=0, y_max=200, alpha=0.5):" in cell_source:
                        updated_source = cell_source.replace(
                            "def visualize_with_stations(station_cutoffs, x_offset=0, x_scale=1, y_min=0, y_max=200, alpha=0.5):",
                            "def visualize_with_stations(station_cutoffs, x_offset=None, x_scale=None, y_min=None, y_max=None, alpha=None):\n    # Use global parameters if not explicitly provided\n    global global_x_offset, global_x_scale, global_y_min, global_y_max, global_alpha\n    \n    # Use global values as defaults if parameters are not provided\n    if x_offset is None: x_offset = global_x_offset\n    if x_scale is None: x_scale = global_x_scale\n    if y_min is None: y_min = global_y_min\n    if y_max is None: y_max = global_y_max\n    if alpha is None: alpha = global_alpha"
                        )
                        
                        # Split the source back into lines
                        notebook_data['cells'][i]['source'] = updated_source.split('\n')
                        # Add newline character at the end of each line except the last one
                        for j in range(len(notebook_data['cells'][i]['source']) - 1):
                            notebook_data['cells'][i]['source'][j] += '\n'
                        
                        updated = True
                        print("  Updated station visualization function to use global parameters")
        
        if updated:
            # Save the updated notebook
            with open(notebook_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            print(f"  Successfully updated {notebook_path}")
        else:
            print(f"  No updates made to {notebook_path}")
    
    return True

if __name__ == "__main__":
    fix_alignment_parameters()
    print("Finished updating notebooks") 
#!/usr/bin/env python3
"""
Script to ensure all notebooks have the necessary global alignment variables defined.

This fixes the NameError: name 'current_x_offset' is not defined issue that occurs
when visualize_with_stations() is called before alignment parameters are properly set.
"""

import os
import json
import glob
import re
from pathlib import Path

def fix_alignment_globals():
    """Add missing global alignment variables to all notebooks."""
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
    
    print(f"Found {len(notebooks)} notebooks to check")
    
    # Process each notebook
    for notebook_path in notebooks:
        print(f"Processing {notebook_path}...")
        
        # Load the notebook
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
        
        # Create backup
        backup_path = f"{notebook_path}.globals.bak"
        print(f"  Creating backup at {backup_path}")
        with open(backup_path, 'w') as f:
            json.dump(notebook_data, f, indent=1)
        
        # Check for current_* variables
        has_current_vars = False
        plots_dir_cell_index = None
        
        # Find the plots_dir cell to add our variables after it
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                if "plots_dir = " in cell_source:
                    plots_dir_cell_index = i
                if "current_x_offset" in cell_source:
                    has_current_vars = True
                    print("  Notebook already has current_* variables defined")
                    break
        
        # If variables not found and we found the plots_dir cell, add them
        if not has_current_vars and plots_dir_cell_index is not None:
            print("  Adding current_* variables after plots_dir cell")
            
            # Extract user ID from filename
            user_id = os.path.basename(notebook_path).split('_')[1]
            
            # Create a new cell with the global variables
            globals_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Initialize global alignment parameters\n",
                    "# These will be updated by the interactive alignment tool\n",
                    "current_x_offset = -0.8  # Default starting values\n",
                    "current_x_scale = 1.0\n",
                    "current_y_min = 90\n",
                    "current_y_max = 190\n",
                    "current_alpha = 0.6\n"
                ],
                "outputs": []
            }
            
            # Insert the new cell after the plots_dir cell
            notebook_data['cells'].insert(plots_dir_cell_index + 1, globals_cell)
            
            # Save the modified notebook
            with open(notebook_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            print(f"  Saved updated notebook with alignment variables")
        elif not has_current_vars:
            print(f"  WARNING: Could not find plots_dir cell to add variables after")
        
    return True

if __name__ == "__main__":
    fix_alignment_globals()
    print("Finished fixing alignment variables in notebooks") 
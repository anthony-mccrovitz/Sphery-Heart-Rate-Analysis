#!/usr/bin/env python3
"""
Script to fix plots_dir variable issue in notebooks.
This ensures that all notebooks have the plots_dir variable defined before using it.
"""

import os
import sys
import json
import glob
from pathlib import Path

def fix_plots_dir_issue():
    """Update all notebooks to ensure plots_dir is defined."""
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
        
        # Extract user ID from filename
        user_id = os.path.basename(notebook_path).split('_')[1]
        
        # Load the notebook
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
        
        # Create backup
        backup_path = f"{notebook_path}.plots_dir_fix.bak"
        print(f"  Creating backup at {backup_path}")
        with open(backup_path, 'w') as f:
            json.dump(notebook_data, f, indent=1)
        
        # Check if plots_dir is defined in any cell
        plots_dir_defined = False
        for cell in notebook_data['cells']:
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                if "plots_dir = " in cell_source:
                    plots_dir_defined = True
                    print("  plots_dir already defined in notebook")
                    break
        
        # If plots_dir is not defined, add it
        if not plots_dir_defined:
            # Find the cell with imports
            for i, cell in enumerate(notebook_data['cells']):
                if cell['cell_type'] == 'code' and "import " in ''.join(cell['source']):
                    # Create a new cell for plots_dir
                    plots_dir_cell = {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "source": [
                            "# Create output directories for plots\n",
                            "import os\n",
                            f"plots_dir = f'output/plots/user_{user_id}'\n",
                            "os.makedirs(plots_dir, exist_ok=True)\n",
                            "print(f\"Created plots directory: {plots_dir}\")\n"
                        ],
                        "outputs": []
                    }
                    
                    # Insert the new cell after the imports
                    notebook_data['cells'].insert(i+1, plots_dir_cell)
                    print("  Added plots_dir definition cell")
                    
                    # Save the updated notebook
                    with open(notebook_path, 'w') as f:
                        json.dump(notebook_data, f, indent=1)
                    print(f"  Successfully updated {notebook_path}")
                    break
            else:
                print(f"  Could not find a suitable place to add plots_dir in {notebook_path}")
        
    return True

if __name__ == "__main__":
    # Create the main plots directory if it doesn't exist
    os.makedirs("output/plots", exist_ok=True)
    print("Created main plots directory")
    
    fix_plots_dir_issue()
    print("Finished checking notebooks") 
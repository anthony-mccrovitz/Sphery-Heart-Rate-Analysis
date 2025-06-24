#!/usr/bin/env python3
"""
Script to add plot saving functionality to all user data exploration notebooks.
This ensures that plots are saved to user-specific folders in the plots directory.
"""

import os
import sys
import json
import re
import glob
from pathlib import Path

def add_plot_saving():
    """Update all notebooks to add plot saving functionality."""
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
        
        # Extract user ID from filename
        user_id = os.path.basename(notebook_path).split('_')[1]
        
        # Create backup
        backup_path = f"{notebook_path}.plot_saving.bak"
        print(f"  Creating backup at {backup_path}")
        with open(backup_path, 'w') as f:
            json.dump(notebook_data, f, indent=1)
        
        # Find and update the cells
        updated = False
        
        # First, add the directory creation cell after the imports
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code' and "# STEP 1: Setup and imports" in ''.join(cell['source']):
                # Create a new cell for directory creation
                dir_creation_cell = {
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
                notebook_data['cells'].insert(i+1, dir_creation_cell)
                updated = True
                print("  Added directory creation cell")
                break
        
        # Update the visualization cells to save plots
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Update the basic heart rate visualization (STEP 2)
                if "# STEP 2: Visualize heart rate data" in cell_source and "plt.figure(figsize=(14,5))" in cell_source:
                    # Add plot saving code
                    updated_source = cell_source.replace(
                        "plt.show()",
                        "plt.tight_layout()\n# Save the plot\nplt.savefig(f'{plots_dir}/heart_rate_over_time.png', dpi=300, bbox_inches='tight')\nplt.show()"
                    )
                    
                    # Split the source back into lines
                    notebook_data['cells'][i]['source'] = updated_source.split('\n')
                    # Add newline character at the end of each line except the last one
                    for j in range(len(notebook_data['cells'][i]['source']) - 1):
                        notebook_data['cells'][i]['source'][j] += '\n'
                    
                    updated = True
                    print("  Updated basic heart rate visualization to save plot")
                
                # Update the alignment visualization (STEP 3)
                elif "def update_alignment" in cell_source and "interact(" in cell_source:
                    # Add plot saving code to the update_alignment function
                    updated_source = cell_source.replace(
                        "plt.tight_layout()\n    plt.show()",
                        "plt.tight_layout()\n    # Save the plot\n    plt.savefig(f'{plots_dir}/aligned_hr_data.png', dpi=300, bbox_inches='tight')\n    plt.show()"
                    )
                    
                    # Split the source back into lines
                    notebook_data['cells'][i]['source'] = updated_source.split('\n')
                    # Add newline character at the end of each line except the last one
                    for j in range(len(notebook_data['cells'][i]['source']) - 1):
                        notebook_data['cells'][i]['source'][j] += '\n'
                    
                    updated = True
                    print("  Updated alignment visualization to save plot")
                
                # Update the station boundaries visualization (STEP 4)
                elif "def visualize_with_stations" in cell_source and "# Function to visualize stations with current cutoffs" in cell_source:
                    # Add plot saving code
                    updated_source = cell_source.replace(
                        "plt.tight_layout()\n    plt.show()",
                        "plt.tight_layout()\n    # Save the plot\n    plt.savefig(f'{plots_dir}/heart_rate_with_stations.png', dpi=300, bbox_inches='tight')\n    plt.show()"
                    )
                    
                    # Split the source back into lines
                    notebook_data['cells'][i]['source'] = updated_source.split('\n')
                    # Add newline character at the end of each line except the last one
                    for j in range(len(notebook_data['cells'][i]['source']) - 1):
                        notebook_data['cells'][i]['source'][j] += '\n'
                    
                    updated = True
                    print("  Updated station boundaries visualization to save plot")
                
                # Update the HR patterns analysis visualization (STEP 8)
                elif "def analyze_hr_patterns" in cell_source and "# Find high heart rate periods that might indicate stations" in cell_source:
                    # Add plot saving code
                    updated_source = cell_source.replace(
                        "plt.tight_layout()\n        plt.show()",
                        "plt.tight_layout()\n        # Save the plot\n        plt.savefig(f'{plots_dir}/high_hr_periods.png', dpi=300, bbox_inches='tight')\n        plt.show()"
                    )
                    
                    # Split the source back into lines
                    notebook_data['cells'][i]['source'] = updated_source.split('\n')
                    # Add newline character at the end of each line except the last one
                    for j in range(len(notebook_data['cells'][i]['source']) - 1):
                        notebook_data['cells'][i]['source'][j] += '\n'
                    
                    updated = True
                    print("  Updated HR patterns analysis to save plot")
        
        if updated:
            # Save the updated notebook
            with open(notebook_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            print(f"  Successfully updated {notebook_path}")
        else:
            print(f"  No updates made to {notebook_path}")
    
    return True

if __name__ == "__main__":
    # Create the main plots directory if it doesn't exist
    os.makedirs("output/plots", exist_ok=True)
    print("Created main plots directory")
    
    add_plot_saving()
    print("Finished updating notebooks") 
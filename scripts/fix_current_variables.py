#!/usr/bin/env python3
"""
Script to fix the 'current_x_offset is not defined' error in all notebooks.

This script ensures that:
1. All notebooks have the global alignment variables initialized
2. These variables are properly updated in the interactive tools
3. All necessary global statements are added

This fixes the common NameError that occurs when visualize_with_stations() 
tries to access the current_* variables before they're properly defined.
"""

import os
import json
import glob
import re
from pathlib import Path

def fix_current_variables():
    """Fix missing current_* variables in all notebooks."""
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
        print(f"\nProcessing {notebook_path}...")
        
        # Extract user ID from filename
        user_id = os.path.basename(notebook_path).split('_')[1]
        
        try:
            # Load the notebook
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
            
            # Create backup
            backup_path = f"{notebook_path}.vars.bak"
            print(f"  Creating backup at {backup_path}")
            with open(backup_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            
            # Track variables and locations
            plots_dir_cell_idx = None
            has_current_vars_defined = False
            update_plot_cell_idx = None
            update_alignment_cell_idx = None
            
            # First pass: analyze notebook structure
            for i, cell in enumerate(notebook_data['cells']):
                if cell['cell_type'] == 'code':
                    cell_source = ''.join(cell['source'])
                    
                    # Check for plots_dir cell
                    if "plots_dir = " in cell_source:
                        plots_dir_cell_idx = i
                    
                    # Check if current_* variables are already defined
                    if "current_x_offset =" in cell_source and not "def " in cell_source:
                        has_current_vars_defined = True
                    
                    # Find update_plot function
                    if "def update_plot" in cell_source:
                        update_plot_cell_idx = i
                    
                    # Find update_alignment function
                    if "def update_alignment" in cell_source:
                        update_alignment_cell_idx = i
            
            # Make necessary changes
            changes_made = False
            
            # 1. Add current_* variables if missing
            if not has_current_vars_defined and plots_dir_cell_idx is not None:
                print("  Adding current_* variables after plots_dir cell")
                
                # Create variables cell
                vars_cell = {
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
                
                # Insert cell after plots_dir cell
                notebook_data['cells'].insert(plots_dir_cell_idx + 1, vars_cell)
                changes_made = True
                print("  Added current_* variables initialization")
                
                # Adjust indices for other cells that come after
                if update_plot_cell_idx and update_plot_cell_idx > plots_dir_cell_idx:
                    update_plot_cell_idx += 1
                if update_alignment_cell_idx and update_alignment_cell_idx > plots_dir_cell_idx:
                    update_alignment_cell_idx += 1
            
            # 2. Fix update_plot function if present
            if update_plot_cell_idx is not None:
                cell = notebook_data['cells'][update_plot_cell_idx]
                cell_source = ''.join(cell['source'])
                
                # Check if the function already has global statement
                if "global current_x_offset" not in cell_source:
                    print("  Fixing update_plot function")
                    
                    # Add global statement after function definition
                    cell_source = cell_source.replace(
                        "def update_plot(b):",
                        "def update_plot(b):\n    global current_x_offset, current_x_scale, current_y_min, current_y_max, current_alpha"
                    )
                    
                    # Add variable assignments after slider values are captured
                    if "current_x_offset = " not in cell_source:
                        # Find where slider values are captured
                        parts = cell_source.split("alpha = alpha_slider.value", 1)
                        if len(parts) == 2:
                            cell_source = parts[0] + "alpha = alpha_slider.value\n    \n    # Update global variables\n    current_x_offset = x_offset\n    current_x_scale = x_scale\n    current_y_min = y_min\n    current_y_max = y_max\n    current_alpha = alpha" + parts[1]
                    
                    # Fix indentation for plt.savefig call if needed
                    if "    plt.savefig" not in cell_source and "plt.savefig" in cell_source:
                        cell_source = cell_source.replace(
                            "plt.savefig",
                            "        plt.savefig"
                        )
                    
                    # Update the cell
                    notebook_data['cells'][update_plot_cell_idx]['source'] = cell_source.split('\n')
                    # Add newline to each line except the last
                    for j in range(len(notebook_data['cells'][update_plot_cell_idx]['source']) - 1):
                        notebook_data['cells'][update_plot_cell_idx]['source'][j] += '\n'
                    
                    changes_made = True
                    print("  Updated update_plot function")
            
            # 3. Fix update_alignment function if present
            if update_alignment_cell_idx is not None:
                cell = notebook_data['cells'][update_alignment_cell_idx]
                cell_source = ''.join(cell['source'])
                
                # Check if the function already has global statement
                if "global current_x_offset" not in cell_source:
                    print("  Fixing update_alignment function")
                    
                    # Add global statement and variable assignments
                    cell_source = re.sub(
                        r"def update_alignment\([^)]*\):",
                        r"def update_alignment(x_offset=-0.8, x_scale=1.0, y_min=90, y_max=190, alpha=0.6):\n    global current_x_offset, current_x_scale, current_y_min, current_y_max, current_alpha\n    current_x_offset = x_offset\n    current_x_scale = x_scale\n    current_y_min = y_min\n    current_y_max = y_max\n    current_alpha = alpha",
                        cell_source
                    )
                    
                    # Update the cell
                    notebook_data['cells'][update_alignment_cell_idx]['source'] = cell_source.split('\n')
                    # Add newline to each line except the last
                    for j in range(len(notebook_data['cells'][update_alignment_cell_idx]['source']) - 1):
                        notebook_data['cells'][update_alignment_cell_idx]['source'][j] += '\n'
                    
                    changes_made = True
                    print("  Updated update_alignment function")
            
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
    fix_current_variables()
    print("\nFinished fixing current_* variables in notebooks") 
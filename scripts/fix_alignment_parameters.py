#!/usr/bin/env python3
"""
Script to fix alignment parameter issues in notebooks.

This script:
1. Ensures all notebooks have the necessary global alignment variables defined
2. Makes sure the update function correctly sets these globals
3. Ensures the visualize_with_stations function correctly uses these globals

This fixes issues like:
- NameError: name 'current_x_offset' is not defined
- Misalignment of station boundaries with HR data
"""

import os
import json
import glob
import re
from pathlib import Path

def fix_alignment_parameters():
    """Fix alignment parameter issues in all notebooks."""
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
        
        # Load the notebook
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
        
        # Create backup
        backup_path = f"{notebook_path}.align.bak"
        print(f"  Creating backup at {backup_path}")
        with open(backup_path, 'w') as f:
            json.dump(notebook_data, f, indent=1)
        
        # Track what changes we need to make
        needs_globals_cell = True
        needs_update_function_fix = False
        needs_visualize_function_fix = False
        update_function_cell_idx = None
        visualize_function_cell_idx = None
        plots_dir_cell_idx = None
        
        # First pass: analyze notebook structure
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Find plots_dir cell
                if "plots_dir = " in cell_source:
                    plots_dir_cell_idx = i
                
                # Check if globals are already defined
                if "current_x_offset" in cell_source and "current_x_scale" in cell_source:
                    needs_globals_cell = False
                
                # Find update function cell
                if ("def update_alignment" in cell_source or "def update_plot" in cell_source) and "interact(" in cell_source:
                    update_function_cell_idx = i
                    if "global current_x_offset" not in cell_source:
                        needs_update_function_fix = True
                
                # Find visualize_with_stations function cell
                if "def visualize_with_stations" in cell_source:
                    visualize_function_cell_idx = i
                    # Check if it's accessing globals correctly
                    if "global current_x_offset" not in cell_source and "current_x_offset =" in cell_source:
                        needs_visualize_function_fix = True
        
        # Now make the necessary changes
        changes_made = False
        
        # 1. Add global variables if needed
        if needs_globals_cell and plots_dir_cell_idx is not None:
            print("  Adding global alignment variables after plots_dir cell")
            
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
            notebook_data['cells'].insert(plots_dir_cell_idx + 1, globals_cell)
            changes_made = True
            # Adjust other cell indices since we inserted a cell
            if update_function_cell_idx is not None and update_function_cell_idx > plots_dir_cell_idx:
                update_function_cell_idx += 1
            if visualize_function_cell_idx is not None and visualize_function_cell_idx > plots_dir_cell_idx:
                visualize_function_cell_idx += 1
        
        # 2. Fix update function to properly set globals
        if needs_update_function_fix and update_function_cell_idx is not None:
            print("  Fixing update function to properly set global variables")
            
            cell = notebook_data['cells'][update_function_cell_idx]
            cell_source = ''.join(cell['source'])
            
            # Different fixes based on the type of update function
            if "def update_alignment" in cell_source:
                # This function already sets globals, make sure it's properly indented
                if "global current_x_offset" not in cell_source:
                    # Add global statement at the beginning of the function
                    cell_source = cell_source.replace(
                        "def update_alignment",
                        "def update_alignment(x_offset=-0.8, x_scale=1.0, y_min=90, y_max=190, alpha=0.6):\n    global current_x_offset, current_x_scale, current_y_min, current_y_max, current_alpha\n    current_x_offset = x_offset\n    current_x_scale = x_scale\n    current_y_min = y_min\n    current_y_max = y_max\n    current_alpha = alpha"
                    )
            elif "def update_plot" in cell_source:
                # This is the button-based implementation
                if "global current_x_offset" not in cell_source:
                    # Add global statement after function definition
                    cell_source = cell_source.replace(
                        "def update_plot(b):",
                        "def update_plot(b):\n    global current_x_offset, current_x_scale, current_y_min, current_y_max, current_alpha"
                    )
                    # Make sure variables are being set
                    if "current_x_offset = " not in cell_source:
                        lines = cell_source.split('\n')
                        new_lines = []
                        slider_values_captured = False
                        for line in lines:
                            new_lines.append(line)
                            if not slider_values_captured and "alpha = alpha_slider.value" in line:
                                # Add variable assignments after slider values are captured
                                new_lines.append("    ")
                                new_lines.append("    # Update global variables")
                                new_lines.append("    current_x_offset = x_offset")
                                new_lines.append("    current_x_scale = x_scale")
                                new_lines.append("    current_y_min = y_min")
                                new_lines.append("    current_y_max = y_max")
                                new_lines.append("    current_alpha = alpha")
                                new_lines.append("    ")
                                slider_values_captured = True
                        cell_source = '\n'.join(new_lines)
            
            # Update the cell source
            notebook_data['cells'][update_function_cell_idx]['source'] = cell_source.split('\n')
            # Add newline character at the end of each line except the last one
            for j in range(len(notebook_data['cells'][update_function_cell_idx]['source']) - 1):
                notebook_data['cells'][update_function_cell_idx]['source'][j] += '\n'
            
            changes_made = True
        
        # 3. Fix visualize_with_stations function to properly use globals
        if needs_visualize_function_fix and visualize_function_cell_idx is not None:
            print("  Fixing visualize_with_stations function to properly use global variables")
            
            cell = notebook_data['cells'][visualize_function_cell_idx]
            cell_source = ''.join(cell['source'])
            
            # Fix function to correctly access globals
            if "global current_x_offset" not in cell_source:
                # Add global statement after parameter declaration
                if "def visualize_with_stations(" in cell_source:
                    # This uses a more complex regex to match the function definition line
                    cell_source = re.sub(
                        r"(def visualize_with_stations\([^\)]*\):)",
                        r"\1\n    # Use stored alignment parameters if not specified\n    global current_x_offset, current_x_scale, current_y_min, current_y_max, current_alpha",
                        cell_source
                    )
            
            # Update the cell source
            notebook_data['cells'][visualize_function_cell_idx]['source'] = cell_source.split('\n')
            # Add newline character at the end of each line except the last one
            for j in range(len(notebook_data['cells'][visualize_function_cell_idx]['source']) - 1):
                notebook_data['cells'][visualize_function_cell_idx]['source'][j] += '\n'
            
            changes_made = True
        
        # Save the notebook if changes were made
        if changes_made:
            with open(notebook_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            print(f"  Saved updated notebook with alignment parameter fixes")
        else:
            print(f"  No changes needed - alignment parameters are correctly set")
    
    return True

if __name__ == "__main__":
    fix_alignment_parameters()
    print("\nFinished fixing alignment parameters in notebooks") 
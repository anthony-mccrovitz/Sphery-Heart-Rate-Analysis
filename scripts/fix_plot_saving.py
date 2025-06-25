#!/usr/bin/env python3
"""
Script to ensure all three key plots are properly saved in each user's data exploration notebook:
1. Heart Rate Over Time
2. Aligned HR Data
3. Heart Rate with Station Boundaries

This script will modify all user_*_data_exploration.ipynb files in the notebooks directory.

=== Purpose and Importance ===

This script ensures consistency across all user notebooks by making sure:

1. Every notebook has a plots_dir variable properly defined and pointing to the 
   correct user-specific directory (output/plots/user_XX/)

2. Every notebook saves the three standard visualizations:
   - Heart rate over time plot: Basic visualization of heart rate data
   - Aligned HR data with Garmin chart: Overlay of parsed HR data on the Garmin chart image
   - Heart rate with station boundaries: Visualization showing station start/end markers

3. All plot saving code follows the same pattern:
   - Uses plt.tight_layout() for better spacing
   - Saves with high resolution (dpi=300)
   - Uses consistent file naming convention
   - Uses consistent plot formatting

This standardization ensures that:
- Researchers can easily find and compare visualizations across users
- All data analyses maintain the same visual outputs
- The project maintains a consistent organizational structure
- Future analyses can rely on the presence of these standard outputs

=== Usage ===

Run this script after any new notebooks are added to the project or if
plot saving functionality needs to be updated:

```
python scripts/fix_plot_saving.py
```

The script creates backups of all notebooks before modifying them.
"""

import os
import sys
import json
import glob
import re
from pathlib import Path

def fix_plot_saving():
    """Update all notebooks to ensure proper plot saving."""
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
        
        # Extract user ID from filename
        user_id = os.path.basename(notebook_path).split('_')[1]
        
        # Load the notebook
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
        
        # Create backup
        backup_path = f"{notebook_path}.plot_fix.bak"
        print(f"  Creating backup at {backup_path}")
        with open(backup_path, 'w') as f:
            json.dump(notebook_data, f, indent=1)
        
        # First, ensure plots_dir is defined
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
                    plots_dir_defined = True
                    print("  Added plots_dir definition cell")
                    break
        
        # Flag to track if any changes were made
        any_changes = plots_dir_defined and not plots_dir_defined  # This is always False, let's fix it
        any_changes = False  # Initialize properly
        
        # Update heart rate over time plot
        hr_plot_updated = False
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Look for the basic heart rate visualization
                if ("STEP 2: Visualize" in cell_source or "Heart Rate Over Time" in cell_source) and "plt.figure" in cell_source:
                    if "plt.figure(figsize=" in cell_source and "plt.show()" in cell_source:
                        # Check if the plot saving is already there
                        if "plt.savefig(f'{plots_dir}/heart_rate_over_time.png'" not in cell_source:
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
                            
                            hr_plot_updated = True
                            any_changes = True
                            print("  Updated heart rate over time plot to save")
        
        # Update alignment visualization - look for update_alignment OR update_plot function
        alignment_updated = False
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Look for the alignment visualization functions
                if ("def update_alignment" in cell_source or "def update_plot" in cell_source) and "plt.show()" in cell_source:
                    # Check if plot saving is already there
                    if "plt.savefig(f'{plots_dir}/aligned_hr_data.png'" not in cell_source:
                        # First try with regex pattern for standard indentation
                        pattern = r"(\s+plt\.tight_layout\(\)\s+)(plt\.show\(\))"
                        if re.search(pattern, cell_source):
                            updated_source = re.sub(
                                pattern,
                                r"\1# Save the plot\n    plt.savefig(f'{plots_dir}/aligned_hr_data.png', dpi=300, bbox_inches='tight')\n    \2",
                                cell_source
                            )
                        # If first pattern didn't match, try another pattern without tight_layout
                        elif "plt.show()" in cell_source:
                            updated_source = cell_source.replace(
                                "plt.show()",
                                "plt.tight_layout()\n        # Save the plot\n        plt.savefig(f'{plots_dir}/aligned_hr_data.png', dpi=300, bbox_inches='tight')\n        plt.show()"
                            )
                        else:
                            # Skip if we can't find a reliable pattern
                            continue
                        
                        # Split the source back into lines
                        notebook_data['cells'][i]['source'] = updated_source.split('\n')
                        # Add newline character at the end of each line except the last one
                        for j in range(len(notebook_data['cells'][i]['source']) - 1):
                            notebook_data['cells'][i]['source'][j] += '\n'
                        
                        alignment_updated = True
                        any_changes = True
                        print("  Updated alignment visualization to save plot")
        
        # Update station boundaries visualization
        stations_updated = False
        for i, cell in enumerate(notebook_data['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Look for various forms of station visualization functions
                if "def visualize_with_stations" in cell_source or "Function to visualize stations" in cell_source or "station boundaries" in cell_source.lower():
                    # Check if plot saving is already there
                    if "plt.savefig(f'{plots_dir}/heart_rate_with_stations.png'" not in cell_source and "plt.show()" in cell_source:
                        # Add plot saving code using different patterns
                        if re.search(r"(\s+plt\.tight_layout\(\)\s+)(plt\.show\(\))", cell_source):
                            updated_source = re.sub(
                                r"(\s+plt\.tight_layout\(\)\s+)(plt\.show\(\))",
                                r"\1# Save the plot\n    plt.savefig(f'{plots_dir}/heart_rate_with_stations.png', dpi=300, bbox_inches='tight')\n    \2",
                                cell_source
                            )
                        elif "plt.show()" in cell_source:
                            # Try to determine indentation level
                            if "    plt.show()" in cell_source:
                                updated_source = cell_source.replace(
                                    "    plt.show()",
                                    "    plt.tight_layout()\n    # Save the plot\n    plt.savefig(f'{plots_dir}/heart_rate_with_stations.png', dpi=300, bbox_inches='tight')\n    plt.show()"
                                )
                            else:
                                updated_source = cell_source.replace(
                                    "plt.show()",
                                    "plt.tight_layout()\n# Save the plot\nplt.savefig(f'{plots_dir}/heart_rate_with_stations.png', dpi=300, bbox_inches='tight')\nplt.show()"
                                )
                        else:
                            # Skip if we can't find a reliable pattern
                            continue
                        
                        # Split the source back into lines
                        notebook_data['cells'][i]['source'] = updated_source.split('\n')
                        # Add newline character at the end of each line except the last one
                        for j in range(len(notebook_data['cells'][i]['source']) - 1):
                            notebook_data['cells'][i]['source'][j] += '\n'
                        
                        stations_updated = True
                        any_changes = True
                        print("  Updated station boundaries visualization to save plot")
        
        # Save the notebook if changes were made
        if any_changes:
            with open(notebook_path, 'w') as f:
                json.dump(notebook_data, f, indent=1)
            print(f"  Saved updated notebook: {notebook_path}")
        else:
            print(f"  No changes needed for {notebook_path}")
        
    return True

if __name__ == "__main__":
    # Create the main plots directory if it doesn't exist
    os.makedirs("output/plots", exist_ok=True)
    print("Created main plots directory")
    
    fix_plot_saving()
    print("Finished updating notebooks") 
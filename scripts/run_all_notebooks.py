#!/usr/bin/env python3
"""
Script to run all user notebooks and generate plots

This script executes all user_*_data_exploration.ipynb notebooks to ensure
that all plots are generated and saved to their respective directories.

It uses nbconvert to execute each notebook in place, capturing outputs
and generating all visualizations.

Usage:
    python scripts/run_all_notebooks.py [--subset N]

Options:
    --subset N    Run only N notebooks (for testing)
"""

import os
import sys
import glob
import argparse
import subprocess
from pathlib import Path

def run_notebooks(subset=None):
    """
    Run all user notebooks to generate plots
    
    Args:
        subset: If provided, only run this number of notebooks (for testing)
    """
    # Find all user notebooks
    notebook_pattern = "notebooks/user_*_data_exploration.ipynb"
    notebooks = glob.glob(notebook_pattern)
    
    # Filter out any checkpoint files or backups
    notebooks = [nb for nb in notebooks if 
                '.ipynb_checkpoints' not in nb and 
                not nb.endswith('.bak')]
    
    # Remove duplicates and sort
    notebooks = sorted(set(notebooks))
    
    if subset:
        notebooks = notebooks[:subset]
        print(f"Running subset of {subset} notebooks")
    
    if not notebooks:
        print(f"No notebooks found matching {notebook_pattern}")
        return False
    
    print(f"Found {len(notebooks)} notebooks to run")
    
    # Make sure output directories exist
    os.makedirs("output/plots", exist_ok=True)
    
    # Create a list to track successes and failures
    results = []
    
    # Process each notebook
    for i, notebook_path in enumerate(notebooks):
        print(f"[{i+1}/{len(notebooks)}] Running {notebook_path}...")
        
        # Extract user ID from filename
        user_id = os.path.basename(notebook_path).split('_')[1]
        
        # Create user-specific plots directory
        plots_dir = f"output/plots/user_{user_id}"
        os.makedirs(plots_dir, exist_ok=True)
        
        try:
            # Run the notebook using nbconvert
            cmd = [
                "jupyter", "nbconvert", 
                "--to", "notebook", 
                "--execute",
                "--inplace",
                "--ExecutePreprocessor.timeout=300",  # 5 minute timeout
                notebook_path
            ]
            
            # Run the command and capture output
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  ✅ Successfully executed {notebook_path}")
                
                # Check if plots were generated
                expected_plots = [
                    f"{plots_dir}/heart_rate_over_time.png",
                    f"{plots_dir}/aligned_hr_data.png",
                    f"{plots_dir}/heart_rate_with_stations.png"
                ]
                
                missing_plots = [p for p in expected_plots if not os.path.exists(p)]
                
                if missing_plots:
                    print(f"  ⚠️ Warning: The following plots were not generated:")
                    for plot in missing_plots:
                        print(f"    - {plot}")
                    results.append((notebook_path, "warning", f"Missing {len(missing_plots)} plots"))
                else:
                    print(f"  ✅ All plots generated successfully")
                    results.append((notebook_path, "success", "All plots generated"))
            else:
                print(f"  ❌ Failed to execute {notebook_path}")
                print(f"  Error: {result.stderr}")
                results.append((notebook_path, "error", f"Execution failed: {result.stderr[:100]}..."))
                
        except Exception as e:
            print(f"  ❌ Error running {notebook_path}: {str(e)}")
            results.append((notebook_path, "error", str(e)))
    
    # Print summary
    print("\n=== Execution Summary ===")
    print(f"Total notebooks: {len(notebooks)}")
    print(f"Successes: {len([r for r in results if r[1] == 'success'])}")
    print(f"Warnings: {len([r for r in results if r[1] == 'warning'])}")
    print(f"Errors: {len([r for r in results if r[1] == 'error'])}")
    
    print("\nDetails:")
    for notebook, status, message in results:
        status_symbol = "✅" if status == "success" else "⚠️" if status == "warning" else "❌"
        print(f"{status_symbol} {notebook}: {message}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run all user notebooks to generate plots')
    parser.add_argument('--subset', type=int, help='Run only this many notebooks (for testing)')
    args = parser.parse_args()
    
    run_notebooks(subset=args.subset)
    print("Finished running notebooks") 
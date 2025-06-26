#!/usr/bin/env python3
"""
Check completion status for each user in the heart rate analysis project.
This script verifies if users have:
1. A plots folder with required plot files
2. A CSV station data file
3. A data exploration notebook
"""

import os
import glob
from pathlib import Path

def check_user_completion():
    # Get all user IDs from data files
    data_files = glob.glob('data/*-d.tcx')
    user_ids = []
    for file in data_files:
        user_id = os.path.basename(file).split('-')[0]
        user_ids.append(int(user_id))
    
    user_ids.sort()
    
    print("=" * 80)
    print("USER COMPLETION STATUS REPORT")
    print("=" * 80)
    print(f"Total users found: {len(user_ids)}")
    print()
    
    completed_users = []
    incomplete_users = []
    
    for user_id in user_ids:
        print(f"User {user_id}:")
        
        # Check for plots folder
        plots_folder = f'output/plots/user_{user_id}'
        has_plots_folder = os.path.exists(plots_folder)
        
        # Check for required plot files
        required_plots = [
            'aligned_hr_data.png',
            'heart_rate_over_time.png',
            'heart_rate_with_stations.png'
        ]
        
        plot_files_exist = []
        if has_plots_folder:
            for plot_file in required_plots:
                plot_path = os.path.join(plots_folder, plot_file)
                plot_files_exist.append(os.path.exists(plot_path))
        else:
            plot_files_exist = [False] * len(required_plots)
        
        # Check for CSV station data
        csv_file = f'output/processed/user_{user_id}_station_data.csv'
        has_csv = os.path.exists(csv_file)
        
        # Check for notebook
        notebook_file = f'notebooks/user_{user_id}_data_exploration.ipynb'
        has_notebook = os.path.exists(notebook_file)
        
        # Status indicators
        plots_status = "✅" if has_plots_folder and all(plot_files_exist) else "❌"
        csv_status = "✅" if has_csv else "❌"
        notebook_status = "✅" if has_notebook else "❌"
        
        print(f"  📁 Plots folder: {plots_status}")
        if has_plots_folder:
            for i, plot_file in enumerate(required_plots):
                status = "✅" if plot_files_exist[i] else "❌"
                print(f"     - {plot_file}: {status}")
        else:
            print(f"     - Folder missing: {plots_folder}")
            
        print(f"  📊 CSV data: {csv_status}")
        if has_csv:
            # Check CSV file size and content
            try:
                with open(csv_file, 'r') as f:
                    lines = f.readlines()
                    print(f"     - {len(lines)-1} data rows")
            except:
                print(f"     - Error reading CSV")
        else:
            print(f"     - Missing: {csv_file}")
            
        print(f"  📓 Notebook: {notebook_status}")
        
        # Overall completion status
        is_complete = (has_plots_folder and all(plot_files_exist) and 
                      has_csv and has_notebook)
        
        if is_complete:
            completed_users.append(user_id)
            print(f"  🎉 Status: COMPLETE")
        else:
            incomplete_users.append(user_id)
            print(f"  ⚠️  Status: INCOMPLETE")
        
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Completed users ({len(completed_users)}): {completed_users}")
    print(f"❌ Incomplete users ({len(incomplete_users)}): {incomplete_users}")
    print()
    print(f"Completion rate: {len(completed_users)}/{len(user_ids)} ({len(completed_users)/len(user_ids)*100:.1f}%)")
    
    # Detailed breakdown of what's missing
    if incomplete_users:
        print()
        print("MISSING COMPONENTS:")
        print("-" * 40)
        
        missing_plots = []
        missing_csv = []
        missing_notebooks = []
        
        for user_id in incomplete_users:
            plots_folder = f'output/plots/user_{user_id}'
            csv_file = f'output/processed/user_{user_id}_station_data.csv'
            notebook_file = f'notebooks/user_{user_id}_data_exploration.ipynb'
            
            if not os.path.exists(plots_folder) or not all([
                os.path.exists(os.path.join(plots_folder, plot)) 
                for plot in required_plots
            ]):
                missing_plots.append(user_id)
                
            if not os.path.exists(csv_file):
                missing_csv.append(user_id)
                
            if not os.path.exists(notebook_file):
                missing_notebooks.append(user_id)
        
        if missing_plots:
            print(f"📁 Missing plots: {missing_plots}")
        if missing_csv:
            print(f"📊 Missing CSV: {missing_csv}")
        if missing_notebooks:
            print(f"📓 Missing notebooks: {missing_notebooks}")

if __name__ == "__main__":
    check_user_completion() 
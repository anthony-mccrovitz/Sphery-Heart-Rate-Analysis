#!/usr/bin/env python3
"""
Script to update existing user data exploration notebooks with the new format.
This will replace the content of existing notebooks with the template,
while preserving the user ID.
"""

import os
import sys
import json
import glob
import shutil
import argparse
from pathlib import Path

def update_existing_notebooks(force=False, backup=True):
    """Update existing user notebooks with the template code."""
    # Find all existing user notebooks
    notebook_pattern = "notebooks/user_*_data_exploration.ipynb"
    existing_notebooks = glob.glob(notebook_pattern)
    
    # Filter out any checkpoint files or backups
    existing_notebooks = [nb for nb in existing_notebooks if 
                         '.ipynb_checkpoints' not in nb and 
                         not nb.endswith('.bak')]
    
    # Remove duplicates and sort
    existing_notebooks = sorted(set(existing_notebooks))
    
    if not existing_notebooks:
        print(f"No existing notebooks found matching {notebook_pattern}")
        return False
    
    # Load the template notebook (using user_58 as the template)
    template_path = Path("notebooks/user_58_data_exploration.ipynb")
    
    if not template_path.exists():
        print(f"Error: Template notebook not found at {template_path}")
        return False
    
    with open(template_path, 'r') as f:
        template_data = json.load(f)
    
    # Verify that required files exist before processing
    charts_dir = Path("charts_cropped")
    data_dir = Path("data")
    
    # Process each existing notebook
    for notebook_path in existing_notebooks:
        # Skip the template notebook itself
        if notebook_path == str(template_path):
            print(f"Skipping template notebook: {notebook_path}")
            continue
            
        # Extract user ID from filename
        try:
            user_id = int(os.path.basename(notebook_path).split('_')[1])
        except (IndexError, ValueError):
            print(f"Cannot extract user ID from {notebook_path}, skipping...")
            continue
        
        # Verify that the required files exist for this user
        chart_file = charts_dir / f"user_{user_id}.png"
        tcx_file = data_dir / f"{user_id}-d.tcx"
        
        if not chart_file.exists():
            print(f"Warning: Chart file not found for user {user_id}: {chart_file}")
            if not force:
                print(f"Skipping user {user_id}. Use --force to update anyway.")
                continue
        
        if not tcx_file.exists():
            print(f"Warning: TCX file not found for user {user_id}: {tcx_file}")
            if not force:
                print(f"Skipping user {user_id}. Use --force to update anyway.")
                continue
        
        print(f"Processing notebook for User {user_id}: {notebook_path}")
        
        # Create backup if requested
        if backup:
            backup_path = f"{notebook_path}.bak"
            print(f"Creating backup at {backup_path}")
            shutil.copy2(notebook_path, backup_path)
        
        # Clone the template and update with user-specific information
        user_notebook = template_data.copy()
        
        # Update all instances of user 58 with the correct user ID
        for i, cell in enumerate(user_notebook['cells']):
            if cell['cell_type'] == 'code':
                updated_source = []
                for line in cell['source']:
                    # Update the USER_ID line if it exists (not present as a variable, need to check all mentions)
                    if "User 58" in line:
                        updated_source.append(line.replace("User 58", f"User {user_id}"))
                    elif "user_58" in line:
                        updated_source.append(line.replace("user_58", f"user_{user_id}"))
                    elif "58-d.tcx" in line:
                        updated_source.append(line.replace("58-d.tcx", f"{user_id}-d.tcx"))
                    else:
                        updated_source.append(line)
                user_notebook['cells'][i]['source'] = updated_source
            elif cell['cell_type'] == 'markdown':
                updated_source = []
                for line in cell['source']:
                    if "User 58" in line:
                        updated_source.append(line.replace("User 58", f"User {user_id}"))
                    else:
                        updated_source.append(line)
                user_notebook['cells'][i]['source'] = updated_source
        
        # Save the updated notebook
        with open(notebook_path, 'w') as f:
            json.dump(user_notebook, f, indent=1)
        
        print(f"Updated notebook for User {user_id}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Update existing user notebooks with the new format.')
    parser.add_argument('--force', action='store_true', help='Force update even if files are missing')
    parser.add_argument('--no-backup', dest='backup', action='store_false', help='Skip creating backup files')
    parser.add_argument('--list-only', action='store_true', help='Just list notebooks without updating them')
    
    args = parser.parse_args()
    
    if args.list_only:
        # Find all notebooks matching the pattern
        notebook_pattern = "notebooks/user_*_data_exploration.ipynb"
        notebooks = glob.glob(notebook_pattern)
        notebooks = [nb for nb in notebooks if 
                    '.ipynb_checkpoints' not in nb and 
                    not nb.endswith('.bak')]
        notebooks = sorted(set(notebooks))
        
        print(f"Found {len(notebooks)} notebooks:")
        for nb in notebooks:
            user_id = os.path.basename(nb).split('_')[1]
            print(f"  User {user_id}: {nb}")
        return
    
    update_existing_notebooks(force=args.force, backup=args.backup)

if __name__ == "__main__":
    main() 
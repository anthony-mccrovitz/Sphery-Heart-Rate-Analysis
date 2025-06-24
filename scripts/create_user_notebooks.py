#!/usr/bin/env python3
"""
Script to create new user data exploration notebooks from the template.
"""

import os
import sys
import json
import re
import shutil
from pathlib import Path

def create_user_notebooks(user_ids):
    """Create new notebooks for the specified user IDs."""
    # Load the template notebook
    template_path = Path("notebooks/template_data_exploration.ipynb")
    
    if not template_path.exists():
        print(f"Error: Template notebook not found at {template_path}")
        return False
    
    with open(template_path, 'r') as f:
        template_data = json.load(f)
    
    # Process each user ID
    for user_id in user_ids:
        # Define the output notebook path
        output_path = f"notebooks/user_{user_id}_data_exploration.ipynb"
        
        # Skip if the notebook already exists
        if os.path.exists(output_path):
            print(f"Notebook for User {user_id} already exists at {output_path}, skipping...")
            continue
        
        print(f"Creating notebook for User {user_id}: {output_path}")
        
        # Clone the template and update with user-specific information
        user_notebook = template_data.copy()
        
        # Update all instances of USER_ID with the correct user ID
        for i, cell in enumerate(user_notebook['cells']):
            if cell['cell_type'] == 'code':
                cell_source = ''.join(cell['source'])
                
                # Replace USER_ID = 0 with the correct user ID
                cell_source = re.sub(r'USER_ID\s*=\s*\d+', f'USER_ID = {user_id}', cell_source)
                
                # Replace all instances of User followed by any number with User {user_id}
                cell_source = re.sub(r'User\s+\d+', f'User {user_id}', cell_source)
                
                # Replace User {USER_ID} with User {user_id}
                cell_source = re.sub(r'User\s+\{USER_ID\}', f'User {user_id}', cell_source)
                
                # Split the source back into lines
                user_notebook['cells'][i]['source'] = cell_source.split('\n')
                # Add newline character at the end of each line except the last one
                for j in range(len(user_notebook['cells'][i]['source']) - 1):
                    user_notebook['cells'][i]['source'][j] += '\n'
                
            elif cell['cell_type'] == 'markdown':
                cell_source = ''.join(cell['source'])
                
                # Replace all instances of User followed by any number with User {user_id}
                cell_source = re.sub(r'User\s+\d+', f'User {user_id}', cell_source)
                
                # Replace User {USER_ID} with User {user_id}
                cell_source = re.sub(r'User\s+\{USER_ID\}', f'User {user_id}', cell_source)
                
                # Split the source back into lines
                user_notebook['cells'][i]['source'] = cell_source.split('\n')
                # Add newline character at the end of each line except the last one
                for j in range(len(user_notebook['cells'][i]['source']) - 1):
                    user_notebook['cells'][i]['source'][j] += '\n'
        
        # Save the new notebook
        with open(output_path, 'w') as f:
            json.dump(user_notebook, f, indent=1)
        
        print(f"Created notebook for User {user_id}")
    
    return True

if __name__ == "__main__":
    # List of user IDs to create notebooks for
    user_ids = [55, 54, 53, 52, 51, 50, 48, 45, 44, 43, 42, 41, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 27, 26, 24, 20, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    
    create_user_notebooks(user_ids)
    print(f"Finished creating {len(user_ids)} notebooks.") 
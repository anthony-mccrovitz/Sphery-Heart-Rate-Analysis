# Sphere Heart Rate Analysis Scripts

This directory contains utility scripts for the heart rate analysis project.

## parse_tcx.py

Parses Garmin TCX files into pandas DataFrames.

**Usage:**
```python
from parse_tcx import parse_tcx_to_df

# Parse a TCX file
df, session_total_sec, sessions_avg_hr, session_max_hr = parse_tcx_to_df('data/58-d.tcx')
```

## update_notebooks.py

Creates new user-specific notebooks from the template notebook.

**Usage:**
```bash
# Create notebooks for specific users
python scripts/update_notebooks.py 58 59 60

# Force overwrite existing notebooks
python scripts/update_notebooks.py --force 58 59 60
```

## update_existing_notebooks.py

Updates existing user notebooks with the code from user_58 while preserving the user IDs.

**Usage:**
```bash
# Update all existing user notebooks
python scripts/update_existing_notebooks.py

# List notebooks without updating them
python scripts/update_existing_notebooks.py --list-only

# Force update even if TCX or chart files are missing
python scripts/update_existing_notebooks.py --force

# Skip creating backup files
python scripts/update_existing_notebooks.py --no-backup
```

## Workflow

1. Use `parse_tcx.py` to extract heart rate data from TCX files
2. Use `update_notebooks.py` to create new user notebooks from the template
3. Use `update_existing_notebooks.py` to update existing user notebooks with improved code

## Requirements

These scripts require the following Python packages:
- pandas
- numpy
- matplotlib
- ipywidgets 
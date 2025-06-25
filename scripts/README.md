# Scripts Directory

This directory contains scripts for processing and managing the Sphere Heart Rate Analysis project.

## Scripts Overview

- `parse_tcx.py` - Parses TCX files into pandas DataFrames for analysis
- `create_user_notebooks.py` - Creates template notebooks for each user ID
- `update_existing_notebooks.py` - Updates existing user notebooks with new features
- `fix_alignment_parameters.py` - Fixes alignment parameters in notebooks to ensure consistent visualization 
- `fix_plots_dir.py` - Adds plot directory creation to notebooks
- `add_plot_saving.py` - Adds plot saving functionality to notebooks
- `fix_plot_saving.py` - Ensures all three key plots are properly saved in all notebooks
- `update_station_processing.py` - Updates station boundary processing in notebooks

## Usage

### fix_plot_saving.py

This script ensures all three key plots are properly saved in each user's data exploration notebook:
1. Heart Rate Over Time
2. Aligned HR Data with Garmin Chart
3. Heart Rate with Station Boundaries

The script modifies all user_*_data_exploration.ipynb files in the notebooks directory to:
- Ensure plots_dir is properly defined
- Add proper plot saving code for all three visualization types
- Maintain code style consistency

Each modified notebook is backed up before changes are made.

Run the script with:

```bash
python scripts/fix_plot_saving.py
```

### Other Scripts

See individual script comments for usage details.

## parse_tcx.py

Parses Garmin TCX files into pandas DataFrames.

**Usage:**
```
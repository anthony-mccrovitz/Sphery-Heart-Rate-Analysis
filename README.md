# Sphere Heart Rate Analysis

This project analyzes heart rate data from Garmin trackers for the Sphere study, aligning TCX data with Garmin heart rate charts to identify activity stations.

## Project Structure

- **charts_cropped/**: Contains cropped heart rate charts from Garmin for each user
- **data/**: Contains TCX and PDF files from Garmin for each user
- **docs/**: Study design documentation
- **notebooks/**: Jupyter notebooks for data analysis
  - *template_data_exploration.ipynb*: Template notebook with standard analysis workflow
  - *user_XX_data_exploration.ipynb*: User-specific analysis notebooks
- **output/**:
  - **plots/**: Visualizations for each user
    - *user_XX/*: User-specific directories containing standardized plots
  - **processed/**: Contains processed CSV files with station data
- **scripts/**: Utility scripts
  - *parse_tcx.py*: Parses TCX files into pandas DataFrames
  - *create_user_notebooks.py*: Creates user notebooks from template
  - *update_existing_notebooks.py*: Updates existing notebooks
  - *fix_alignment_parameters.py*: Ensures consistent alignment parameters
  - *fix_plots_dir.py*: Adds plot directory creation to notebooks
  - *fix_plot_saving.py*: Ensures all three key plots are saved in notebooks
  - *update_station_processing.py*: Updates station boundary processing

## Getting Started

1. Set up the Python environment:
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r Requirements.txt
   ```

2. Run the Jupyter Lab server:
   ```bash
   jupyter lab
   ```

3. Open and run the user-specific notebooks in the `notebooks/` directory

## Analysis Workflow

Each user notebook follows this workflow:

1. **Load the data**: Parse TCX file for heart rate data
2. **Visualize**: Plot heart rate over time
3. **Align**: Overlay heart rate data with Garmin chart
4. **Adjust**: Fine-tune alignment with interactive sliders
5. **Define stations**: Identify and mark the three stations
6. **Process**: Extract station-specific data
7. **Save**: Export the processed data to CSV
8. **Plot**: Save standardized visualizations to the output/plots directory

## Standard Visualizations

Each notebook now generates and saves three standard visualizations:

1. **Heart Rate Over Time**: Basic time-series plot of heart rate data
2. **Aligned HR Data**: Heart rate data aligned with Garmin chart background
3. **Heart Rate with Stations**: Heart rate data with station boundaries marked

These plots are saved to user-specific directories in `output/plots/user_XX/`.

## Batch Processing

To update all user notebooks with the latest code:

```bash
python scripts/update_existing_notebooks.py
```

To ensure all notebooks have proper plot saving functionality:

```bash
python scripts/fix_plot_saving.py
```

## Requirements

See `Requirements.txt` for a list of dependencies.

## Data Format

The output CSV files contain the following fields:
- User and session info (user_id, gender, circuit_type)
- Station info (number, name)
- Session timing and heart rate data
- Station-specific timing and heart rate data
- Per-station ratings (motivation, enjoyment, team experience)
- Physical/cognitive exertion metrics
- Final evaluation fields 
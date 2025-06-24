# Sphere Heart Rate Analysis

This project analyzes heart rate data from Garmin trackers for the Sphere study, aligning TCX data with Garmin heart rate charts to identify activity stations.

## Project Structure

- **charts_cropped/**: Contains cropped heart rate charts from Garmin for each user
- **data/**: Contains TCX and PDF files from Garmin for each user
- **docs/**: Study design documentation
- **notebooks/**: Jupyter notebooks for data analysis
  - *template_data_exploration.ipynb*: Template notebook with standard analysis workflow
  - *user_XX_data_exploration.ipynb*: User-specific analysis notebooks
- **output/processed/**: Contains processed CSV files with station data
- **scripts/**: Utility scripts
  - *parse_tcx.py*: Parses TCX files into pandas DataFrames
  - *update_notebooks.py*: Creates notebooks from template
  - *update_existing_notebooks.py*: Updates existing notebooks

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

## Batch Processing

To update all user notebooks with the latest code:

```bash
python scripts/update_existing_notebooks.py
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
import xml.etree.ElementTree as ET
import pandas as pd

def parse_tcx_to_df(tcx_file):
    """
    Parses a .tcx file and returns a DataFrame with:
    - timestamp (datetime)
    - heart_rate (BPM)
    - start_time (the first timestamp, same for every row)
    - elapsed_min (minutes since start)
    Also returns total time (sec), average HR, max HR, and calories burned.
    """
    tree = ET.parse(tcx_file)
    root = tree.getroot()
    ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    
    # Extract calories from the Lap element
    calories = 0
    for lap in root.findall('.//ns:Lap', ns):
        cal_elem = lap.find('ns:Calories', ns)
        if cal_elem is not None:
            calories += int(cal_elem.text)
    
    timestamps = []
    heart_rates = []
    for tp in root.findall('.//ns:Trackpoint', ns):
        time = tp.find('ns:Time', ns)
        hr = tp.find('.//ns:Value', ns)
        if time is not None and hr is not None:
            timestamps.append(pd.to_datetime(time.text))
            heart_rates.append(int(hr.text))
    df = pd.DataFrame({'timestamp': timestamps, 'heart_rate': heart_rates})
    if df.empty:
        raise ValueError(f"No heart rate data found in {tcx_file}")
    start_time = df['timestamp'].iloc[0]
    df['start_time'] = start_time
    df['elapsed_min'] = (df['timestamp'] - start_time).dt.total_seconds() / 60
    total_time_sec = (df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]).total_seconds()
    avg_hr = df['heart_rate'].mean()
    max_hr = df['heart_rate'].max()
    return df, total_time_sec, avg_hr, max_hr, calories
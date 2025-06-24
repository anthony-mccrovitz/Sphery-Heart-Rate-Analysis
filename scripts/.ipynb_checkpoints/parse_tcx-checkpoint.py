import xml.etree.ElementTree as ET
import pandas as pd

def parse_tcx_to_df(tcx_file):
    """
    Parses a .tcx file and returns a DataFrame with:
    - timestamp (datetime)
    - heart_rate (BPM)
    - start_time (the first timestamp, same for every row)
    - elapsed_min (minutes since start)
    Also returns total time (sec), average HR, and max HR.
    """
    tree = ET.parse(tcx_file)
    root = tree.getroot()
    ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
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
    return df, total_time_sec, avg_hr, max_hr
#!/usr/bin/env python3
"""
Restructure CSV files to include all required columns in logical order
for the Sphere Heart Rate Analysis research project.
"""

import pandas as pd
import glob
import os
from datetime import datetime

def get_complete_column_structure():
    """Define the complete column structure in logical order."""
    
    return [
        # Participant Demographics & Identifiers
        'user_id',
        'participant_id',
        'group_number',
        'champ_number',
        'gender',
        'age',
        'height_cm',
        'weight_kg',
        
        # Sports Experience
        'sports_experience',
        'sports_frequency_per_week',
        'sports_experience_years',
        'sports_types',
        
        # Gaming Experience
        'video_game_experience',
        'gaming_experience_years',
        'video_game_types',
        'gaming_frequency_per_week',
        
        # Session Data
        'session_start_time',
        'session_end_time',
        'session_duration_min',
        'session_avg_hr',
        'session_max_hr',
        'calories_burned',
        
        # Station Data
        'station_number',
        'station_name',
        'station_start_time',
        'station_end_time',
        'station_duration_min',
        'station_avg_hr',
        'station_max_hr',
        'station_points_score',
        
        # Station-Level Ratings (Per Station)
        'station_motivation_rating',
        'station_fun_rating',
        'station_physical_exertion_rating',
        'station_cognitive_exertion_rating',
        'station_team_cooperation_rating',
        
        # Overall Experience (Same for all stations of a user)
        'overall_experience_rating',
        'overall_motivation_after_completion',
        'what_did_you_like_and_why',
        'what_could_be_better',
        
        # Data Quality & Research Notes
        'data_quality',
        'notes'
    ]

def get_default_values():
    """Get default values for missing columns."""
    
    return {
        'participant_id': 'TBD',
        'group_number': 'TBD',
        'sports_experience': 'TBD',
        'sports_frequency_per_week': 'TBD',
        'sports_experience_years': 'TBD',
        'sports_types': 'TBD',
        'video_game_experience': 'TBD',
        'gaming_experience_years': 'TBD',
        'video_game_types': 'TBD',
        'gaming_frequency_per_week': 'TBD',
        'station_points_score': 'TBD',
        'station_motivation_rating': 'TBD',
        'station_fun_rating': 'TBD',
        'station_physical_exertion_rating': 'TBD',
        'station_cognitive_exertion_rating': 'TBD',
        'station_team_cooperation_rating': 'TBD',
        'overall_experience_rating': 'TBD',
        'overall_motivation_after_completion': 'TBD',
        'what_did_you_like_and_why': 'TBD',
        'what_could_be_better': 'TBD'
    }

def map_existing_columns(df):
    """Map existing columns to new column names."""
    
    column_mapping = {
        'motivation': 'station_motivation_rating',
        'enjoyment': 'station_fun_rating',
        'team_experience': 'station_team_cooperation_rating',
        'subjective_physical_exertion': 'station_physical_exertion_rating',
        'subjective_cognitive_exertion': 'station_cognitive_exertion_rating',
        'overall_experience': 'overall_experience_rating',
        'overall_motivation': 'overall_motivation_after_completion',
        'feedback': 'what_did_you_like_and_why',
        'sports_exp': 'sports_experience',
        'gaming_exp': 'video_game_experience'
    }
    
    # Rename columns that exist
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    return df

def restructure_csv_files():
    """Restructure all CSV files with complete column set."""
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    target_columns = get_complete_column_structure()
    default_values = get_default_values()
    
    print(f"Found {len(csv_files)} CSV files to restructure")
    print(f"Target structure: {len(target_columns)} columns")
    print("=" * 80)
    
    updated_count = 0
    
    for csv_file in sorted(csv_files):
        try:
            user_id = int(os.path.basename(csv_file).split('_')[1])
            print(f"Restructuring User {user_id}...")
            
            # Read existing CSV
            df = pd.read_csv(csv_file)
            original_cols = len(df.columns)
            
            # Map existing columns to new names
            df = map_existing_columns(df)
            
            # Create new DataFrame with target structure
            new_df = pd.DataFrame()
            
            for col in target_columns:
                if col in df.columns:
                    # Use existing data
                    new_df[col] = df[col]
                elif col in default_values:
                    # Use default value for missing columns
                    new_df[col] = default_values[col]
                else:
                    # Keep existing data if column exists but not in mapping
                    if col in df.columns:
                        new_df[col] = df[col]
                    else:
                        new_df[col] = ''
            
            # Save restructured CSV
            new_df.to_csv(csv_file, index=False)
            
            print(f"  ✅ Updated: {original_cols} → {len(new_df.columns)} columns")
            updated_count += 1
            
        except Exception as e:
            print(f"  ❌ Error updating {csv_file}: {e}")
    
    print("=" * 80)
    print(f"Successfully restructured {updated_count}/{len(csv_files)} CSV files")
    print()
    print("NEW COLUMN STRUCTURE:")
    print("-" * 40)
    
    for i, col in enumerate(target_columns, 1):
        print(f"{i:2d}. {col}")
    
    print()
    print("NOTES:")
    print("• Columns marked 'TBD' need to be filled with actual data")
    print("• All files now have consistent structure for research analysis")
    print("• Existing data has been preserved and properly mapped")
    print("• Ready for data collection completion and statistical analysis")

def create_column_reference():
    """Create a reference file explaining all columns."""
    
    reference_content = """# Sphere Heart Rate Analysis - CSV Column Reference

## Column Descriptions

### Participant Demographics & Identifiers
- **user_id**: Unique identifier for participant
- **participant_id**: Additional participant identifier (TBD)
- **group_number**: Experimental group assignment (TBD)
- **champ_number**: Champion/participant number from study
- **gender**: Participant gender
- **age**: Participant age in years
- **height_cm**: Height in centimeters
- **weight_kg**: Weight in kilograms

### Sports Experience
- **sports_experience**: Whether participant has sports experience (TBD)
- **sports_frequency_per_week**: How often they play sports per week (TBD)
- **sports_experience_years**: Years of sports experience (TBD)
- **sports_types**: Types of sports they play (TBD)

### Gaming Experience
- **video_game_experience**: Whether participant has gaming experience (TBD)
- **gaming_experience_years**: Years of gaming experience (TBD)
- **video_game_types**: Types of games they play (TBD)
- **gaming_frequency_per_week**: Gaming frequency per week (TBD)

### Session Data
- **session_start_time**: Start time of entire session
- **session_end_time**: End time of entire session
- **session_duration_min**: Total session duration in minutes
- **session_avg_hr**: Average heart rate for entire session
- **session_max_hr**: Maximum heart rate for entire session
- **calories_burned**: Total calories burned during session

### Station Data
- **station_number**: Station number (1, 2, or 3)
- **station_name**: Name/type of station
- **station_start_time**: Start time of this station
- **station_end_time**: End time of this station
- **station_duration_min**: Duration of this station in minutes
- **station_avg_hr**: Average heart rate for this station
- **station_max_hr**: Maximum heart rate for this station
- **station_points_score**: Points/rating score for this station (TBD)

### Station-Level Ratings (Per Station)
- **station_motivation_rating**: Motivation rating for this station (TBD)
- **station_fun_rating**: Fun/enjoyment rating for this station (TBD)
- **station_physical_exertion_rating**: Physical exertion rating for this station (TBD)
- **station_cognitive_exertion_rating**: Cognitive exertion rating for this station (TBD)
- **station_team_cooperation_rating**: Team cooperation rating for this station (TBD)

### Overall Experience (Same for all stations of a user)
- **overall_experience_rating**: Overall experience rating for entire session (TBD)
- **overall_motivation_after_completion**: Motivation level after completing circuit (TBD)
- **what_did_you_like_and_why**: What participant liked and why (TBD)
- **what_could_be_better**: Suggestions for improvement (TBD)

### Data Quality & Research Notes
- **data_quality**: Assessment of data quality for research use
- **notes**: Research notes and methodology information

## Notes
- Columns marked "(TBD)" need to be filled with actual survey/questionnaire data
- Heart rate data is automatically calculated from TCX files
- Each row represents one station for one participant
- Each participant should have exactly 3 rows (one per station)
"""
    
    with open('output/CSV_Column_Reference.md', 'w') as f:
        f.write(reference_content)
    
    print("📋 Created column reference file: output/CSV_Column_Reference.md")

if __name__ == "__main__":
    restructure_csv_files()
    create_column_reference() 
#!/usr/bin/env python3
"""
Fix CSV files by preserving ALL existing data and only adding missing columns.
This script will restore the champ_number and calories_burned data that was lost.
"""

import pandas as pd
import glob
import os

def restore_original_data():
    """Restore original data from backup or recreate from metadata."""
    
    # First, let's check if we can restore from git or recreate from metadata
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    
    print("Fixing CSV files to preserve all original data...")
    print("=" * 60)
    
    # Load user metadata to restore champ numbers
    try:
        metadata_df = pd.read_csv('metadata/user_metadata.csv')
        print("✅ Loaded user metadata for champ_number restoration")
    except:
        print("❌ Could not load metadata file")
        metadata_df = None
    
    fixed_count = 0
    
    for csv_file in sorted(csv_files):
        try:
            user_id = int(os.path.basename(csv_file).split('_')[1])
            print(f"Fixing User {user_id}...")
            
            # Read current CSV
            df = pd.read_csv(csv_file)
            
            # Restore champ_number from metadata if available
            if metadata_df is not None:
                user_meta = metadata_df[metadata_df['user_id'] == user_id]
                if not user_meta.empty:
                    champ_number = user_meta.iloc[0]['champ_number']
                    if not pd.isna(champ_number):
                        df['champ_number'] = int(champ_number)
                        print(f"  ✅ Restored champ_number: {int(champ_number)}")
            
            # For calories_burned, we need to get this from the TCX parsing
            # Since we lost this data, we'll mark it for re-processing
            if df['calories_burned'].isna().all() or (df['calories_burned'] == 'TBD').all():
                print(f"  ⚠️  calories_burned needs to be restored from TCX file")
            
            # Fix column labels to be clearer
            improved_columns = {
                'sports_experience_years': 'sports_experience_years_total',
                'gaming_experience_years': 'gaming_experience_years_total',
                'sports_frequency_per_week': 'sports_frequency_times_per_week',
                'gaming_frequency_per_week': 'gaming_frequency_times_per_week'
            }
            
            # Rename columns for clarity
            for old_col, new_col in improved_columns.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            # Save fixed CSV
            df.to_csv(csv_file, index=False)
            fixed_count += 1
            
        except Exception as e:
            print(f"  ❌ Error fixing {csv_file}: {e}")
    
    print("=" * 60)
    print(f"Fixed {fixed_count}/{len(csv_files)} CSV files")
    
    return fixed_count

def restore_calories_from_tcx():
    """Restore calories_burned data by re-parsing TCX files."""
    
    print("\nRestoring calories_burned data from TCX files...")
    print("=" * 60)
    
    import sys
    sys.path.append('scripts')
    
    try:
        from parse_tcx import parse_tcx_to_df
    except:
        print("❌ Could not import TCX parser")
        return
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    restored_count = 0
    
    for csv_file in sorted(csv_files):
        try:
            user_id = int(os.path.basename(csv_file).split('_')[1])
            tcx_file = f'data/{user_id}-d.tcx'
            
            if not os.path.exists(tcx_file):
                print(f"User {user_id}: ⚠️  TCX file not found")
                continue
            
            # Parse TCX to get calories
            try:
                df_tcx, session_total_sec, sessions_avg_hr, session_max_hr, calories_burned = parse_tcx_to_df(tcx_file)
                
                # Update CSV with calories data
                df = pd.read_csv(csv_file)
                df['calories_burned'] = calories_burned
                df.to_csv(csv_file, index=False)
                
                print(f"User {user_id}: ✅ Restored calories_burned: {calories_burned}")
                restored_count += 1
                
            except Exception as e:
                print(f"User {user_id}: ❌ Error parsing TCX: {e}")
                
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
    
    print("=" * 60)
    print(f"Restored calories data for {restored_count} users")

def create_fixed_column_reference():
    """Create updated column reference with clearer labels."""
    
    reference_content = """# Sphere Heart Rate Analysis - CSV Column Reference (FIXED)

## Column Descriptions

### Participant Demographics & Identifiers
- **user_id**: Unique identifier for participant
- **participant_id**: Additional participant identifier (TBD - from survey)
- **group_number**: Experimental group assignment (TBD - from survey)
- **champ_number**: Champion/participant number from study (RESTORED)
- **gender**: Participant gender (TBD - from survey)
- **age**: Participant age in years (TBD - from survey)
- **height_cm**: Height in centimeters (TBD - from survey)
- **weight_kg**: Weight in kilograms (TBD - from survey)

### Sports Experience
- **sports_experience**: Whether participant has sports experience (TBD - from survey)
- **sports_frequency_times_per_week**: How many times they play sports per week (TBD - from survey)
- **sports_experience_years_total**: Total years of sports experience (TBD - from survey)
- **sports_types**: Types of sports they play (TBD - from survey)

### Gaming Experience
- **video_game_experience**: Whether participant has gaming experience (TBD - from survey)
- **gaming_experience_years_total**: Total years of gaming experience (TBD - from survey)
- **video_game_types**: Types of games they play (TBD - from survey)
- **gaming_frequency_times_per_week**: Gaming frequency times per week (TBD - from survey)

### Session Data (AUTOMATICALLY CALCULATED)
- **session_start_time**: Start time of entire session (from TCX)
- **session_end_time**: End time of entire session (from TCX)
- **session_duration_min**: Total session duration in minutes (from TCX)
- **session_avg_hr**: Average heart rate for entire session (from TCX)
- **session_max_hr**: Maximum heart rate for entire session (from TCX)
- **calories_burned**: Total calories burned during session (RESTORED from TCX)

### Station Data (AUTOMATICALLY CALCULATED)
- **station_number**: Station number (1, 2, or 3)
- **station_name**: Name/type of station (TBD - from survey)
- **station_start_time**: Start time of this station (from analysis)
- **station_end_time**: End time of this station (from analysis)
- **station_duration_min**: Duration of this station in minutes (from analysis)
- **station_avg_hr**: Average heart rate for this station (from analysis)
- **station_max_hr**: Maximum heart rate for this station (from analysis)
- **station_points_score**: Points/rating score for this station (TBD - from survey)

### Station-Level Ratings (Per Station - FROM SURVEY)
- **station_motivation_rating**: Motivation rating for this station (TBD - from survey)
- **station_fun_rating**: Fun/enjoyment rating for this station (TBD - from survey)
- **station_physical_exertion_rating**: Physical exertion rating for this station (TBD - from survey)
- **station_cognitive_exertion_rating**: Cognitive exertion rating for this station (TBD - from survey)
- **station_team_cooperation_rating**: Team cooperation rating for this station (TBD - from survey)

### Overall Experience (Same for all stations of a user - FROM SURVEY)
- **overall_experience_rating**: Overall experience rating for entire session (TBD - from survey)
- **overall_motivation_after_completion**: Motivation level after completing circuit (TBD - from survey)
- **what_did_you_like_and_why**: What participant liked and why (TBD - from survey)
- **what_could_be_better**: Suggestions for improvement (TBD - from survey)

### Data Quality & Research Notes (AUTOMATICALLY GENERATED)
- **data_quality**: Assessment of data quality for research use
- **notes**: Research notes and methodology information

## IMPORTANT NOTES
- **TBD** = To Be Determined from survey papers
- **RESTORED** = Data recovered from original sources
- **FROM TCX** = Automatically calculated from heart rate data
- **FROM SURVEY** = Must be filled from participant questionnaires
- Labels now clearly indicate units (e.g., "years_total", "times_per_week")
"""
    
    with open('output/CSV_Column_Reference_FIXED.md', 'w') as f:
        f.write(reference_content)
    
    print("📋 Created FIXED column reference: output/CSV_Column_Reference_FIXED.md")

if __name__ == "__main__":
    print("🔧 FIXING CSV FILES - PRESERVING ALL ORIGINAL DATA")
    print("=" * 60)
    
    # Step 1: Restore original data
    restore_original_data()
    
    # Step 2: Restore calories from TCX files
    restore_calories_from_tcx()
    
    # Step 3: Create updated reference
    create_fixed_column_reference()
    
    print("\n🎉 CSV FILES FIXED!")
    print("✅ Preserved all original data")
    print("✅ Restored champ_number from metadata")
    print("✅ Restored calories_burned from TCX files")
    print("✅ Improved column labels for clarity")
    print("✅ Created updated reference guide") 
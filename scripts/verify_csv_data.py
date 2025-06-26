#!/usr/bin/env python3
"""
Verify that all CSV files have champ_number and calories_burned data.
Check all 48 CSV files for completeness.
"""

import pandas as pd
import glob
import os

def verify_csv_data():
    """Check all CSV files for champ_number and calories_burned data."""
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    csv_files.sort()
    
    print("VERIFYING CSV DATA COMPLETENESS")
    print("=" * 80)
    print(f"Checking {len(csv_files)} CSV files for champ_number and calories_burned...")
    print()
    
    missing_champ = []
    missing_calories = []
    all_good = []
    errors = []
    
    for csv_file in csv_files:
        try:
            user_id = int(os.path.basename(csv_file).split('_')[1])
            
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Check champ_number
            champ_values = df['champ_number'].unique()
            has_champ = not (pd.isna(champ_values).all() or 
                           (champ_values == 'TBD').all() or 
                           (champ_values == '').all())
            
            # Check calories_burned
            calories_values = df['calories_burned'].unique()
            has_calories = not (pd.isna(calories_values).all() or 
                              (calories_values == 'TBD').all() or 
                              (calories_values == '').all())
            
            # Report status
            champ_status = "✅" if has_champ else "❌"
            calories_status = "✅" if has_calories else "❌"
            
            if has_champ and has_calories:
                champ_val = champ_values[0] if len(champ_values) == 1 else champ_values
                calories_val = calories_values[0] if len(calories_values) == 1 else calories_values
                print(f"User {user_id:2d}: {champ_status} champ={champ_val} | {calories_status} calories={calories_val}")
                all_good.append(user_id)
            else:
                print(f"User {user_id:2d}: {champ_status} champ_number | {calories_status} calories_burned")
                if not has_champ:
                    missing_champ.append(user_id)
                if not has_calories:
                    missing_calories.append(user_id)
                    
        except Exception as e:
            print(f"User {user_id:2d}: ❌ ERROR reading file: {e}")
            errors.append(user_id)
    
    print()
    print("=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    
    print(f"✅ Complete data: {len(all_good)}/{len(csv_files)} users")
    if all_good:
        print(f"   Users: {all_good}")
    
    if missing_champ:
        print(f"❌ Missing champ_number: {len(missing_champ)} users")
        print(f"   Users: {missing_champ}")
    
    if missing_calories:
        print(f"❌ Missing calories_burned: {len(missing_calories)} users")
        print(f"   Users: {missing_calories}")
    
    if errors:
        print(f"❌ File errors: {len(errors)} users")
        print(f"   Users: {errors}")
    
    print()
    
    if len(all_good) == len(csv_files):
        print("🎉 SUCCESS: All CSV files have complete champ_number and calories_burned data!")
        return True
    else:
        print("⚠️  ISSUES FOUND: Some CSV files are missing data.")
        return False

def detailed_check():
    """Perform detailed check showing actual values."""
    
    print("\nDETAILED DATA CHECK")
    print("=" * 80)
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    csv_files.sort()
    
    for csv_file in csv_files:
        try:
            user_id = int(os.path.basename(csv_file).split('_')[1])
            df = pd.read_csv(csv_file)
            
            # Get unique values
            champ_vals = df['champ_number'].unique()
            calories_vals = df['calories_burned'].unique()
            
            print(f"User {user_id:2d}:")
            print(f"  champ_number: {champ_vals}")
            print(f"  calories_burned: {calories_vals}")
            print(f"  rows: {len(df)}")
            print()
            
        except Exception as e:
            print(f"User {user_id:2d}: ERROR - {e}")
            print()

if __name__ == "__main__":
    success = verify_csv_data()
    
    if not success:
        print("\nRunning detailed check to identify specific issues...")
        detailed_check() 
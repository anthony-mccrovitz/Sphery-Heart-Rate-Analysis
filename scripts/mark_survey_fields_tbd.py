#!/usr/bin/env python3
"""
Mark all survey-related fields as TBD since they need to come from paper surveys.
These fields will be filled in later from the actual research study surveys.
"""

import pandas as pd
import glob
import os

def mark_survey_fields_tbd():
    """Mark all survey-related fields as TBD."""
    
    # Survey fields that need to be marked as TBD
    survey_fields = [
        'gender',
        'age', 
        'height',
        'weight',
        'sports_experience_years_total',
        'gaming_experience_years_total',
        'station_1_name',
        'station_2_name', 
        'station_3_name',
        'station_1_motivation_rating',
        'station_2_motivation_rating',
        'station_3_motivation_rating',
        'station_1_fun_rating',
        'station_2_fun_rating',
        'station_3_fun_rating',
        'station_1_physical_exertion_rating',
        'station_2_physical_exertion_rating',
        'station_3_physical_exertion_rating',
        'station_1_cognitive_exertion_rating',
        'station_2_cognitive_exertion_rating',
        'station_3_cognitive_exertion_rating',
        'station_1_cooperation_rating',
        'station_2_cooperation_rating',
        'station_3_cooperation_rating',
        'overall_experience_rating',
        'overall_motivation_after_completion',
        'what_you_liked_and_why'
    ]
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    csv_files.sort()
    
    print("MARKING SURVEY FIELDS AS TBD")
    print("=" * 80)
    print(f"Processing {len(csv_files)} CSV files...")
    print(f"Survey fields to mark as TBD: {len(survey_fields)}")
    print()
    
    for field in survey_fields:
        print(f"  - {field}")
    print()
    
    updated_count = 0
    
    for csv_file in csv_files:
        try:
            user_id = int(os.path.basename(csv_file).split('_')[1])
            
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Mark survey fields as TBD
            for field in survey_fields:
                if field in df.columns:
                    df[field] = 'TBD'
                else:
                    print(f"⚠️  User {user_id}: Field '{field}' not found in CSV")
            
            # Save updated CSV
            df.to_csv(csv_file, index=False)
            updated_count += 1
            print(f"✅ User {user_id:2d}: Updated {len(survey_fields)} survey fields")
            
        except Exception as e:
            print(f"❌ User {user_id:2d}: ERROR - {e}")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully updated: {updated_count}/{len(csv_files)} CSV files")
    print(f"📋 Survey fields marked as TBD: {len(survey_fields)}")
    print()
    print("These fields will need to be filled in from the paper surveys:")
    print("  • Demographics: gender, age, height, weight")
    print("  • Experience: sports years, gaming years") 
    print("  • Station names: what each station was called")
    print("  • Station ratings: motivation, fun, physical exertion, cognitive exertion, cooperation")
    print("  • Overall feedback: experience rating, motivation after completion, what you liked")
    print()
    print("🎉 All CSV files are now ready for survey data integration!")

if __name__ == "__main__":
    mark_survey_fields_tbd() 
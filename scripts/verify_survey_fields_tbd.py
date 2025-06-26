#!/usr/bin/env python3
"""
Verify that all survey fields are properly marked as TBD or empty.
"""

import pandas as pd
import glob

def verify_survey_fields():
    """Verify survey fields are marked as TBD or empty."""
    
    # Survey fields that should be TBD or empty
    survey_fields = {
        'gender': 'TBD',
        'age': 'TBD', 
        'height_cm': 'empty',
        'weight_kg': 'empty',
        'sports_experience_years_total': 'TBD',
        'gaming_experience_years_total': 'TBD',
        'station_name': 'empty',
        'station_motivation_rating': 'empty',
        'station_fun_rating': 'empty',
        'station_physical_exertion_rating': 'empty',
        'station_cognitive_exertion_rating': 'empty',
        'station_team_cooperation_rating': 'empty',
        'overall_experience_rating': 'TBD',
        'overall_motivation_after_completion': 'TBD',
        'what_did_you_like_and_why': 'empty'
    }
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    csv_files.sort()
    
    print("VERIFYING SURVEY FIELDS ARE READY FOR DATA ENTRY")
    print("=" * 80)
    print(f"Checking {len(csv_files)} CSV files for survey field status...")
    print()
    
    all_good = True
    
    for csv_file in csv_files:
        user_id = int(csv_file.split('_')[1])
        df = pd.read_csv(csv_file)
        
        # Check first row for survey fields
        row = df.iloc[0]
        issues = []
        
        for field, expected in survey_fields.items():
            if field in df.columns:
                value = row[field]
                if expected == 'TBD':
                    if pd.isna(value) or value != 'TBD':
                        issues.append(f"{field}={value} (should be TBD)")
                elif expected == 'empty':
                    if pd.notna(value) and str(value).strip() != '':
                        issues.append(f"{field}={value} (should be empty)")
            else:
                issues.append(f"{field} missing")
        
        if issues:
            print(f"❌ User {user_id:2d}: {', '.join(issues)}")
            all_good = False
        else:
            print(f"✅ User {user_id:2d}: All survey fields ready for data entry")
    
    print()
    print("=" * 80)
    print("SURVEY FIELDS STATUS")
    print("=" * 80)
    
    if all_good:
        print("🎉 SUCCESS: All CSV files have survey fields properly marked as TBD/empty!")
        print()
        print("Ready for survey data entry:")
        print("  📋 Demographics: gender, age, height_cm, weight_kg")
        print("  🏃 Experience: sports_experience_years_total, gaming_experience_years_total") 
        print("  🎮 Station data: station_name (for each station)")
        print("  ⭐ Ratings: motivation, fun, physical exertion, cognitive exertion, cooperation")
        print("  💭 Feedback: overall_experience_rating, overall_motivation_after_completion")
        print("  📝 Open responses: what_did_you_like_and_why")
    else:
        print("⚠️  Some files need attention - see details above")
    
    return all_good

if __name__ == "__main__":
    verify_survey_fields() 
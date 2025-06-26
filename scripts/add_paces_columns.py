#!/usr/bin/env python3
"""
Add 17 PACES survey columns to all CSV files.
Each column represents a PACES survey item with negative/positive statement format.
Values will be 1-7 scale (1=negative, 7=positive) and initially set to TBD.
"""

import pandas as pd
import glob

def add_paces_columns():
    """Add PACES survey columns to all CSV files."""
    
    # PACES survey columns to add
    paces_columns = [
        "I hated it / I enjoyed it",
        "It was boring / It was interesting", 
        "I didn't like it at all / I liked it a lot",
        "It was unpleasant / It was pleasant",
        "I was not at all engaged in the activity / I was very engaged in the activity",
        "It was not fun at all / It was a lot of fun",
        "I found it very tiring / I found it very invigorating",
        "It made me feel depressed / It made me happy",
        "I felt physically bad during the activity / I felt physically good during the activity",
        "It was not at all stimulating/invigorating / It was very stimulating/invigorating",
        "I was very frustrated during the activity / I was not at all frustrated during the activity",
        "It was not enjoyable at all / It was very enjoyable",
        "It was not exciting at all / It was very exciting",
        "It was not at all stimulating / It was very stimulating",
        "It gave me no sense of accomplishment at all / It gave me a strong sense of accomplishment",
        "It was not at all refreshing / It was very refreshing",
        "I did not feel like I was just going through the motions / I felt like I was just going through the motions"
    ]
    
    csv_files = glob.glob('output/processed/user_*_station_data.csv')
    csv_files.sort()
    
    print("ADDING PACES SURVEY COLUMNS")
    print("=" * 80)
    print(f"Processing {len(csv_files)} CSV files...")
    print(f"Adding {len(paces_columns)} PACES columns...")
    print()
    
    for i, column in enumerate(paces_columns, 1):
        print(f"  {i:2d}. {column}")
    print()
    
    updated_count = 0
    
    for csv_file in csv_files:
        try:
            user_id = int(csv_file.split('_')[1])
            
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Add PACES columns with TBD values
            for column in paces_columns:
                if column not in df.columns:
                    df[column] = 'TBD'
                else:
                    print(f"⚠️  User {user_id}: Column '{column}' already exists")
            
            # Save updated CSV
            df.to_csv(csv_file, index=False)
            updated_count += 1
            print(f"✅ User {user_id:2d}: Added {len(paces_columns)} PACES columns")
            
        except Exception as e:
            print(f"❌ User {user_id:2d}: ERROR - {e}")
    
    print()
    print("=" * 80)
    print("PACES COLUMNS SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully updated: {updated_count}/{len(csv_files)} CSV files")
    print(f"📋 PACES columns added: {len(paces_columns)}")
    print()
    print("PACES Survey Information:")
    print("  📊 Scale: 1-7 (1=negative sentiment, 7=positive sentiment)")
    print("  📝 Format: 'Negative Statement / Positive Statement'")
    print("  🔄 No reverse scoring - raw values will be entered directly")
    print("  📋 Initial value: TBD (ready for survey data entry)")
    print()
    print("🎉 All CSV files now include PACES survey columns!")

if __name__ == "__main__":
    add_paces_columns() 
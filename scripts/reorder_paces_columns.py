#!/usr/bin/env python3
"""
Reorder CSV columns to move PACES survey items before data_quality and notes sections.
This will make the survey data more accessible and logically grouped.
"""

import pandas as pd
import glob

def reorder_paces_columns():
    """Reorder columns to move PACES before data_quality and notes."""
    
    # PACES survey columns to move
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
    
    print("REORDERING PACES COLUMNS")
    print("=" * 80)
    print(f"Processing {len(csv_files)} CSV files...")
    print("Moving PACES columns before data_quality and notes sections...")
    print()
    
    updated_count = 0
    
    for csv_file in csv_files:
        try:
            user_id = int(csv_file.split('_')[1])
            
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Get current column order
            current_columns = list(df.columns)
            
            # Find the positions of data_quality and notes
            data_quality_idx = current_columns.index('data_quality')
            notes_idx = current_columns.index('notes')
            
            # Create new column order
            # 1. All columns before data_quality (excluding PACES)
            before_data_quality = [col for col in current_columns[:data_quality_idx] 
                                 if col not in paces_columns]
            
            # 2. PACES columns
            paces_in_df = [col for col in paces_columns if col in current_columns]
            
            # 3. data_quality and notes
            data_notes = ['data_quality', 'notes']
            
            # 4. Any remaining columns after notes (excluding PACES)
            after_notes = [col for col in current_columns[notes_idx+1:] 
                          if col not in paces_columns]
            
            # Combine in new order
            new_column_order = before_data_quality + paces_in_df + data_notes + after_notes
            
            # Reorder the dataframe
            df_reordered = df[new_column_order]
            
            # Save reordered CSV
            df_reordered.to_csv(csv_file, index=False)
            updated_count += 1
            print(f"✅ User {user_id:2d}: Reordered columns (PACES now before data_quality)")
            
        except Exception as e:
            print(f"❌ User {user_id:2d}: ERROR - {e}")
    
    print()
    print("=" * 80)
    print("COLUMN REORDERING SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully updated: {updated_count}/{len(csv_files)} CSV files")
    print()
    print("New column order:")
    print("  1. Core identification & demographics")
    print("  2. Session & station data")
    print("  3. Experience ratings")
    print("  4. 📊 PACES survey items (17 columns)")
    print("  5. Data quality & research notes")
    print()
    print("🎉 PACES columns are now positioned before technical documentation!")

if __name__ == "__main__":
    reorder_paces_columns() 
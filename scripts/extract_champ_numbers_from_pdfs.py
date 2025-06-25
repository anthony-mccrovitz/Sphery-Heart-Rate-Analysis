#!/usr/bin/env python3
"""
Script to extract champ numbers from PDFs in the data folder and update metadata/user_metadata.csv.

- Scans all *-d.pdf files in the data/ directory
- Extracts champ numbers in the format (champ##) from the PDF text
- Updates the champ_number field in metadata/user_metadata.csv for each user
"""

import pdfplumber
import pandas as pd
import re
import os

metadata_path = 'metadata/user_metadata.csv'
data_dir = 'data'

# Load metadata
metadata_df = pd.read_csv(metadata_path)

for filename in os.listdir(data_dir):
    if filename.endswith('-d.pdf'):
        user_id = filename.split('-')[0]
        pdf_path = os.path.join(data_dir, filename)
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        # Find champ number
        match = re.search(r'\(champ(\d+)\)', text)
        if match:
            champ_number = match.group(1)
            print(f'User {user_id}: champ_number = {champ_number}')
            metadata_df.loc[metadata_df['user_id'] == int(user_id), 'champ_number'] = champ_number
        else:
            print(f'User {user_id}: champ number not found in {filename}')

# Save updated metadata
metadata_df.to_csv(metadata_path, index=False)
print('Metadata updated with champ numbers.') 
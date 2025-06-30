# Low-Quality Heart Rate Data Processing Template

## ✅ Changes Made to user_3_peak_detection.ipynb:

1. **Removed station-based plot saving** - No longer saves `heart_rate_with_stations.png`
2. **Added simple HR-over-time documentation plot** - Creates `heart_rate_over_time.png` for research transparency
3. **Maintained CSV export functionality** - Still exports session-level data with low-quality markers

## 📋 Template Notebook Usage Instructions:

When you encounter low-quality heart rate data for any user, follow these steps:

### Step 1: Copy the Template
```bash
cp notebooks/user_3_peak_detection.ipynb notebooks/user_XX_peak_detection.ipynb
```

### Step 2: Modify the User ID
In Cell 1, change:
```python
USER_ID = 3  # Change this to your actual user number
```

### Step 3: Remove Unnecessary Cells
- **Remove or skip** Cell 3 (Peak Detection) - not needed for low-quality data
- **Remove or skip** Cell 4 (Chart Alignment) - not needed for low-quality data  
- **Remove or skip** Cell 5 (Draggable Station Cutoffs) - not needed for low-quality data

### Step 4: Keep Essential Cells
- **Keep** Cell 1 (Setup)
- **Keep** Cell 2 (Data Loading)
- **Keep** Cell 6 (HR Documentation Plot) 
- **Keep** Cell 7 (Export CSV)

### Step 5: Run and Verify
- Run all remaining cells
- Verify the HR plot shows the data quality issues
- Verify the CSV export completes successfully

## 📊 What Gets Created for Low-Quality Users:

### Files Created:
- `output/plots/user_XX/heart_rate_over_time.png` - Simple HR documentation plot
- `output/processed/user_XX_station_data_peaks.csv` - Session-level CSV with low-quality markers

### Files NOT Created:
- No `heart_rate_with_stations.png` (station boundaries not meaningful)
- No `aligned_hr_data.png` (alignment not needed)

## 🎯 Research Benefits:

1. **Transparency** - Clear documentation of why data was excluded from station analysis
2. **Consistency** - Same CSV format as high-quality users for easy data compilation
3. **Traceability** - Visual evidence of data quality issues for peer review
4. **Efficiency** - Streamlined processing without unnecessary analysis steps

## 🔄 Quick Conversion Process:

For any existing peak detection notebook that needs to be converted to low-quality:

1. Change the title/header to indicate low-quality data
2. Remove cells 3, 4, 5 (peak detection, alignment, station cutoffs)
3. Ensure cell 6 creates the simple HR plot
4. Ensure cell 7 exports with low-quality markers
5. Update any comments to reflect low-quality processing

This approach maintains research rigor while being efficient for data that cannot support station-level analysis. 
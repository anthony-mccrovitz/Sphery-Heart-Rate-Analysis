# Sphere Heart Rate Analysis - Boss Review Package

## Overview
This package contains all the processed data and visualizations ready for survey data input and final analysis.

## Files Included

### 1. MASTER CSV FILE
- **Location**: `../processed/MASTER_sphere_heart_rate_data.csv`
- **Contents**: Combined data from all 48 users (214 total rows)
- **Status**: Ready for survey data input
- **Users**: 40 high-quality + 8 low-quality

### 2. LOW QUALITY GRAPHS FOLDER (`01_low_quality_graphs/`)
- **8 files**: Users 3, 6, 10, 20, 36, 41, 48, 69
- **Purpose**: Shows heart rate patterns that cannot be reliably segmented into stations
- **Data Issues**: 
  - Severe sensor disconnections (Users 3, 6, 20)
  - Frequent disconnections (Users 10, 36)
  - Excessive heart rate variability (Users 41, 48)
  - Poor peak distribution (User 69)

### 3. HIGH QUALITY STATION GRAPHS FOLDER (`02_high_quality_station_graphs/`)
- **44 files**: All high-quality users with clear station boundaries
- **Purpose**: Shows heart rate patterns with colored station boundaries for verification
- **Contents**: Each graph displays:
  - Heart rate over time
  - Colored regions indicating detected stations
  - Clear transitions between activity and recovery periods

## Data Quality Summary
- **Total Users**: 48
- **High Quality**: 40 users (206 station rows)
- **Low Quality**: 8 users (8 session-level rows only)
- **Station Distribution**: 4-6 stations per high-quality user

## Next Steps Required

### 1. Survey Data Input (Your Team)
Fill in these columns in the MASTER CSV for each applicable row:
- `participant_id`, `gender`, `age`, `height_cm`, `weight_kg`
- `sports_experience`, `sports_frequency_times_per_week`, `sports_experience_years_total`, `sports_types`
- `video_game_experience`, `gaming_experience_years_total`, `video_game_types`, `gaming_frequency_times_per_week`
- All station and experience rating columns
- `what_did_you_like_and_why`, `what_could_be_better`

### 2. Data Verification
- Review low-quality graphs to confirm exclusion decisions
- Verify high-quality station boundaries look reasonable
- Check that station counts match expectations (4-6 per user)

### 3. Quality Assurance
- Ensure survey data mapping matches `user_id` correctly
- Verify all rating scales are consistent
- Check for missing data patterns

## Important Notes
- **Low-quality users**: Station fields marked as "N/A - LOW QUALITY DATA" - do not fill station-specific ratings
- **High-quality users**: Fill all columns including station-specific data
- **Research notes**: Already included explaining data quality decisions
- **Station timing**: Based on actual heart rate patterns, not rigid protocol timing

## Contact
Questions about data processing, station boundaries, or quality classifications should be directed to the technical team before proceeding with survey data input.

---
**File prepared**: $(date)
**Total processing time**: Multiple analysis cycles with manual verification
**Ready for**: Survey data integration and statistical analysis 
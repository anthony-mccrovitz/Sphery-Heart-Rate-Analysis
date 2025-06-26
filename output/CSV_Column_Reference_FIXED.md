# Sphere Heart Rate Analysis - CSV Column Reference (FIXED)

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

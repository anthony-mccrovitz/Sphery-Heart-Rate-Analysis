# Sphere Heart Rate Analysis - CSV Column Reference

## Column Descriptions

### Participant Demographics & Identifiers
- **user_id**: Unique identifier for participant
- **participant_id**: Additional participant identifier (TBD)
- **group_number**: Experimental group assignment (TBD)
- **champ_number**: Champion/participant number from study
- **gender**: Participant gender
- **age**: Participant age in years
- **height_cm**: Height in centimeters
- **weight_kg**: Weight in kilograms

### Sports Experience
- **sports_experience**: Whether participant has sports experience (TBD)
- **sports_frequency_per_week**: How often they play sports per week (TBD)
- **sports_experience_years**: Years of sports experience (TBD)
- **sports_types**: Types of sports they play (TBD)

### Gaming Experience
- **video_game_experience**: Whether participant has gaming experience (TBD)
- **gaming_experience_years**: Years of gaming experience (TBD)
- **video_game_types**: Types of games they play (TBD)
- **gaming_frequency_per_week**: Gaming frequency per week (TBD)

### Session Data
- **session_start_time**: Start time of entire session
- **session_end_time**: End time of entire session
- **session_duration_min**: Total session duration in minutes
- **session_avg_hr**: Average heart rate for entire session
- **session_max_hr**: Maximum heart rate for entire session
- **calories_burned**: Total calories burned during session

### Station Data
- **station_number**: Station number (1, 2, or 3)
- **station_name**: Name/type of station
- **station_start_time**: Start time of this station
- **station_end_time**: End time of this station
- **station_duration_min**: Duration of this station in minutes
- **station_avg_hr**: Average heart rate for this station
- **station_max_hr**: Maximum heart rate for this station
- **station_points_score**: Points/rating score for this station (TBD)

### Station-Level Ratings (Per Station)
- **station_motivation_rating**: Motivation rating for this station (TBD)
- **station_fun_rating**: Fun/enjoyment rating for this station (TBD)
- **station_physical_exertion_rating**: Physical exertion rating for this station (TBD)
- **station_cognitive_exertion_rating**: Cognitive exertion rating for this station (TBD)
- **station_team_cooperation_rating**: Team cooperation rating for this station (TBD)

### Overall Experience (Same for all stations of a user)
- **overall_experience_rating**: Overall experience rating for entire session (TBD)
- **overall_motivation_after_completion**: Motivation level after completing circuit (TBD)
- **what_did_you_like_and_why**: What participant liked and why (TBD)
- **what_could_be_better**: Suggestions for improvement (TBD)

### Data Quality & Research Notes
- **data_quality**: Assessment of data quality for research use
- **notes**: Research notes and methodology information

## Notes
- Columns marked "(TBD)" need to be filled with actual survey/questionnaire data
- Heart rate data is automatically calculated from TCX files
- Each row represents one station for one participant
- Each participant should have exactly 3 rows (one per station)

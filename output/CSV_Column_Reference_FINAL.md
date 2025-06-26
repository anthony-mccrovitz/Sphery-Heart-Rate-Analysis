# CSV Column Reference - FINAL VERSION
**Sphere Heart Rate Analysis - Complete Dataset Documentation**

This document describes all 58 columns in the processed CSV files after adding PACES survey items.

---

## 📊 **Complete Column Structure (58 columns)**

### **Core Identification (4 columns)**
1. **user_id** - Participant identifier (2-69)
2. **participant_id** - TBD (from paper surveys)
3. **group_number** - TBD (from paper surveys) 
4. **champ_number** - Championship group (1-12, from metadata)

### **Demographics (8 columns)**
5. **gender** - TBD (from paper surveys)
6. **age** - TBD (from paper surveys)
7. **height_cm** - TBD (from paper surveys)
8. **weight_kg** - TBD (from paper surveys)
9. **sports_experience** - TBD (from paper surveys)
10. **sports_frequency_times_per_week** - TBD (from paper surveys)
11. **sports_experience_years_total** - TBD (from paper surveys)
12. **sports_types** - TBD (from paper surveys)

### **Gaming Experience (4 columns)**
13. **video_game_experience** - TBD (from paper surveys)
14. **gaming_experience_years_total** - TBD (from paper surveys)
15. **video_game_types** - TBD (from paper surveys)
16. **gaming_frequency_times_per_week** - TBD (from paper surveys)

### **Session Data (6 columns)**
17. **session_start_time** - Session start timestamp (from TCX)
18. **session_end_time** - Session end timestamp (from TCX)
19. **session_duration_min** - Total session duration in minutes
20. **session_avg_hr** - Average heart rate for entire session
21. **session_max_hr** - Maximum heart rate for entire session
22. **calories_burned** - Total calories burned (from TCX parsing)

### **Station Data (9 columns)**
23. **station_number** - Station identifier (1, 2, or 3)
24. **station_name** - TBD (from paper surveys)
25. **station_start_time** - Station start timestamp
26. **station_end_time** - Station end timestamp
27. **station_duration_min** - Station duration in minutes
28. **station_avg_hr** - Average heart rate for station
29. **station_max_hr** - Maximum heart rate for station
30. **station_points_score** - TBD (from paper surveys)
31. **station_motivation_rating** - TBD (from paper surveys)

### **Station Experience Ratings (4 columns)**
32. **station_fun_rating** - TBD (from paper surveys)
33. **station_physical_exertion_rating** - TBD (from paper surveys)
34. **station_cognitive_exertion_rating** - TBD (from paper surveys)
35. **station_team_cooperation_rating** - TBD (from paper surveys)

### **Overall Experience (3 columns)**
36. **overall_experience_rating** - TBD (from paper surveys)
37. **overall_motivation_after_completion** - TBD (from paper surveys)
38. **what_did_you_like_and_why** - TBD (from paper surveys)
39. **what_could_be_better** - TBD (from paper surveys)

### **PACES Survey Items (17 columns)**
*Scale: 1-7 (1=negative sentiment, 7=positive sentiment)*
*Format: "Negative Statement / Positive Statement"*

40. **I hated it / I enjoyed it** - TBD (from PACES survey)
41. **It was boring / It was interesting** - TBD (from PACES survey)
42. **I didn't like it at all / I liked it a lot** - TBD (from PACES survey)
43. **It was unpleasant / It was pleasant** - TBD (from PACES survey)
44. **I was not at all engaged in the activity / I was very engaged in the activity** - TBD (from PACES survey)
45. **It was not fun at all / It was a lot of fun** - TBD (from PACES survey)
46. **I found it very tiring / I found it very invigorating** - TBD (from PACES survey)
47. **It made me feel depressed / It made me happy** - TBD (from PACES survey)
48. **I felt physically bad during the activity / I felt physically good during the activity** - TBD (from PACES survey)
49. **It was not at all stimulating/invigorating / It was very stimulating/invigorating** - TBD (from PACES survey)
50. **I was very frustrated during the activity / I was not at all frustrated during the activity** - TBD (from PACES survey)
51. **It was not enjoyable at all / It was very enjoyable** - TBD (from PACES survey)
52. **It was not exciting at all / It was very exciting** - TBD (from PACES survey)
53. **It was not at all stimulating / It was very stimulating** - TBD (from PACES survey)
54. **It gave me no sense of accomplishment at all / It gave me a strong sense of accomplishment** - TBD (from PACES survey)
55. **It was not at all refreshing / It was very refreshing** - TBD (from PACES survey)
56. **I did not feel like I was just going through the motions / I felt like I was just going through the motions** - TBD (from PACES survey)

### **Technical Documentation (2 columns)**
57. **data_quality** - Technical data quality assessment
58. **notes** - Research notes and data validation information

---

## 📋 **Data Entry Status**

### ✅ **Complete & Verified**
- Core identification (user_id, champ_number)
- Session timing and heart rate data
- Station timing and heart rate data
- Calories burned data
- Data quality assessments
- Research notes

### 📝 **Ready for Survey Data Entry (TBD fields)**
- Demographics (gender, age, height, weight)
- Sports & gaming experience
- Station names and scores
- All rating scales (motivation, fun, exertion, cooperation)
- Overall experience feedback
- All 17 PACES survey items

---

## 🎯 **Key Information**

- **Total Users**: 48 participants
- **Total Columns**: 58 columns per CSV
- **Data Structure**: 3 rows per user (one per station)
- **PACES Scale**: 1-7 (no reverse scoring, raw values)
- **Survey Fields**: All marked as TBD, ready for data entry
- **Technical Data**: Complete and validated

---

**Status**: All CSV files are complete with full column structure and ready for survey data integration! 🎉 
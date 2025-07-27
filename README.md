# 📊 Team CodeFont Weather CSV Repository

A bare-bones CSV storage repository for team weather data comparison. Team members upload their CSV files here for shared analysis and the **Compare Cities** feature.

## 🎯 Purpose

- **Simple CSV storage** for team weather data
- **Compare Cities feature** - Core group collaboration functionality
- **Shared data source** for team members to build individual Compare Cities implementations
- **No complex setup** - just upload and analyze
- **Group collaboration** through standardized CSV format

## 🏙️ Compare Cities Feature

**The primary goal** of this repository is to support each team member's **Compare Cities** feature implementation:

- **Shared Data Source**: All team members use data from this repository
- **Standardized Format**: Consistent CSV structure for reliable comparisons
- **Multi-City Analysis**: Compare weather patterns across different locations
- **Team Collaboration**: Each member builds their own Compare Cities feature using this data
- **Data Consistency**: Same source data ensures accurate cross-member comparisons

## 📁 Repository Structure

```text
New_Team_Dashboard/
├── data/                          # CSV files from team members
│   ├── weather_data_Eric.csv      # Eric's weather data (4 cities, 30 days)
│   ├── weather_data_Shomari.csv   # Shomari's weather data
│   ├── weather_data_[member].csv  # Other team members' data
│   └── sample_weather_data.csv    # Example format
├── exports/                       # Generated export files for team imports
│   ├── team_weather_data_[timestamp].csv         # Complete normalized dataset
│   ├── compare_cities_analysis_[timestamp].json  # Cities comparison analysis
│   ├── team_summary_[timestamp].json             # Team statistics summary
│   └── [city]_weather_data_[timestamp].csv       # Individual city datasets
├── main.py                        # Data comparison & city analysis script
├── requirements.txt               # No external dependencies
├── CSV_FORMATS.md                 # Supported CSV format documentation
├── TEAM_GUIDE.md                  # Simple collaboration guide
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/StrayDogSyn/New_Team_Dashboard.git
cd New_Team_Dashboard
```

### 2. Run Analysis & Export Data for Import

```bash
python main.py
```

This command now:

- Analyzes all team data
- Shows Compare Cities analysis
- **Automatically exports data files** for team member imports

### 3. Add Your CSV for Compare Cities Feature

- Create your CSV file in the `data/` folder
- Include multiple cities for meaningful comparisons
- Follow the format in `CSV_FORMATS.md` (supports multiple formats!)
- Run `main.py` again to see updated analysis

## 🏙️ Compare Cities Implementation

Each team member will use this shared data to build their **Compare Cities** feature:

### Data Access Pattern

```python
# Load all team data for Compare Cities feature
from main import load_all_team_data
team_data = load_all_team_data()

# Filter by cities for comparison
cities_to_compare = ['Austin', 'New York', 'Providence']
city_data = [row for row in team_data if row['city'] in cities_to_compare]
```

### Available Cities (Current Data)

- **Austin, TX** - Hot climate data
- **Providence, RI** - Northeast weather patterns  
- **Rawlins, WY** - Mountain/continental climate
- **Ontario, OR** - Pacific Northwest patterns
- **New York, NY** - Urban Northeast data
- **Miami, FL** - Tropical/subtropical data
- **New Jersey** - Mid-Atlantic patterns

## 📦 Export Package for Team Imports

The repository automatically generates export files that team members can import into their individual Compare Cities projects:

### 🗂️ Generated Export Files

**Main Dataset:**

- `team_weather_data_[timestamp].csv` - Complete normalized dataset (225 records)
- All team member data in standardized format for easy import

**Analysis Files:**

- `compare_cities_analysis_[timestamp].json` - Pre-calculated city comparisons
- `team_summary_[timestamp].json` - Overall team statistics

**City-Specific Files:**

- `austin_weather_data_[timestamp].csv` - Austin data only (30 records)
- `providence_weather_data_[timestamp].csv` - Providence data only (30 records)  
- `rawlins_weather_data_[timestamp].csv` - Rawlins data only (30 records)
- `ontario_weather_data_[timestamp].csv` - Ontario data only (30 records)
- `new_york_weather_data_[timestamp].csv` - New York data only (2 records)
- `miami_weather_data_[timestamp].csv` - Miami data only (1 record)
- `new_jersey_weather_data_[timestamp].csv` - New Jersey data only (102 records)

### 💻 Team Member Import Examples

**Python/Pandas Import:**

```python
import pandas as pd
import json

# Import complete team dataset
team_data = pd.read_csv('exports/team_weather_data_[timestamp].csv')

# Import cities analysis for Compare Cities feature
with open('exports/compare_cities_analysis_[timestamp].json', 'r') as f:
    cities_analysis = json.load(f)

# Import specific city data for focused analysis
austin_data = pd.read_csv('exports/austin_weather_data_[timestamp].csv')
providence_data = pd.read_csv('exports/providence_weather_data_[timestamp].csv')
```

**JavaScript/Node.js Import:**

```javascript
const fs = require('fs');
const csv = require('csv-parser');

// Import cities analysis
const citiesAnalysis = JSON.parse(fs.readFileSync('exports/compare_cities_analysis_[timestamp].json'));

// Import team data CSV
const teamData = [];
fs.createReadStream('exports/team_weather_data_[timestamp].csv')
  .pipe(csv())
  .on('data', (row) => teamData.push(row));
```

## 📊 CSV Format & Flexible Support

The repository supports **multiple CSV formats** for maximum team flexibility! See `CSV_FORMATS.md` for full details.

**Standard format:**

```text
timestamp,member_name,city,country,temperature,feels_like,humidity,pressure,weather_main,weather_description,wind_speed,wind_direction,cloudiness,visibility,sunrise,sunset,timezone
```

**Also supports formats like:**

- `Timestamp,City,Temperature (F),Description` (Shomari's format)
- `Date,Location,Temp,Weather,Humidity,Wind` (alternative format)
- Automatic Fahrenheit to Celsius conversion
- Member name extraction from filenames

## 👥 Team Usage for Compare Cities

1. **Add your CSV file** to the `data/` folder with multiple cities
2. **Include diverse locations** for meaningful city comparisons
3. **Commit and push** your file to the repository
4. **Pull latest changes** to get other team members' data
5. **Use shared data** in your Compare Cities feature implementation

## 📈 What the Analysis Provides

The comparison script shows data useful for Compare Cities features:

- **City-wise data coverage** across all team members
- **Temperature patterns** by location and time
- **Weather condition variety** across different climates
- **Data quality metrics** for reliable comparisons
- **Geographic diversity** for robust city comparisons

## 🎯 Example Output (Compare Cities Ready)

```text
============================================================
TEAM WEATHER DATA SUMMARY
============================================================
Team Members: 3
Total Cities: 7
Total Records: 225
Cities: Austin, Miami, New Jersey, New York, Ontario, Providence, Rawlins
Members: Eric, Sample Member, Shomari

📊 TEMPERATURE DATA:
  Records with temperature: 225
  Range: 14.5°C to 42.1°C
  Average: 26.0°C

💧 HUMIDITY DATA:
  Records with humidity: 121
  Range: 16% to 82%
  Average: 42.7%

🌤️ WEATHER CONDITIONS:
  Conditions observed: Broken, Clear, Few, Heavy, Light, Moderate, Overcast, Scattered, Thunderstorm

🌍 COUNTRIES: US, Unknown
============================================================
✅ Successfully processed data from 3 team member(s)
============================================================
```

## 🤝 Contributing for Compare Cities Feature

1. **Create weather CSV file** with multiple cities (3+ recommended)
2. **Add diverse locations** (different climates/regions preferred)
3. **Use filename format**: `weather_data_[YourName].csv`
4. **Include time series data** for temporal comparisons
5. **Commit and push** to share with team for Compare Cities development

---

**🏙️ Shared data source for team Compare Cities feature implementation!** 📈

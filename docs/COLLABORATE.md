# 🤝 Team Collaboration Guide

## Team Weather Data Repository for Compare Cities Feature

This guide explains how team members can collaborate effectively using the shared weather data repository to build individual Compare Cities features.

## 🎯 Project Overview

- **Repository Purpose**: Shared CSV storage for team weather data
- **Core Feature**: Compare Cities functionality for individual projects
- **Team Goal**: Each member builds their own Compare Cities feature using shared data
- **Data Source**: Normalized weather data from all team members

## 📋 Prerequisites

- Git installed on your local machine
- GitHub account with access to the team repository
- Basic understanding of Git commands (clone, add, commit, push, pull)
- Python environment (if using Python for your Compare Cities implementation)

## 🚀 Getting Started

### Step 1: Repository Access

1. **Team Repository**: `https://github.com/StrayDogSyn/New_Team_Dashboard`
2. **Request Access**: Contact repository owner for collaboration access
3. **Clone Repository** (for contributing data):

```bash
git clone https://github.com/StrayDogSyn/New_Team_Dashboard.git
cd New_Team_Dashboard
```

### Step 2: Understanding the Data Structure

The repository contains:

- **Source Data**: Raw CSV files from team members (`data/` folder)
- **Export Package**: Processed data ready for import (`exports/` folder)
- **Multiple Formats**: CSV for data analysis, JSON for structured access

## 📊 Data Integration Methods

### Method 1: Use Export Package (Recommended)

**Best for**: Most team members who want ready-to-use data for Compare Cities features.

#### What You Get

The repository automatically generates export files when `python main.py` is run:

```text
exports/
├── team_weather_data_[timestamp].csv           # Complete dataset (225 records)
└── team_compare_cities_data_[timestamp].json   # Combined analysis & city comparisons
```

**Simple & Clean**: Just 2 files contain everything you need for Compare Cities implementation!

#### Steps for Your Compare Cities Project

1. **Download Export Files**:

```bash
# Navigate to the exports folder on GitHub
# Download the files you need for your project
```

1. **Python Integration Example**:

```python
import pandas as pd
import json

# Load complete team dataset
team_data = pd.read_csv('team_weather_data_20250717_200559.csv')

# Load combined analysis data
with open('team_compare_cities_data_20250717_200559.json', 'r') as f:
    analysis_data = json.load(f)
    cities_analysis = analysis_data['cities_analysis']
    team_summary = analysis_data['team_summary']

# Filter data for specific cities
austin_data = team_data[team_data['city'] == 'Austin']
providence_data = team_data[team_data['city'] == 'Providence']

# Example: Compare temperatures between cities
austin_avg_temp = austin_data['temperature'].mean()
providence_avg_temp = providence_data['temperature'].mean()

print(f"Austin average: {austin_avg_temp:.1f}°C")
print(f"Providence average: {providence_avg_temp:.1f}°C")
```

1. **JavaScript Integration Example**:

```javascript
const fs = require('fs');
const csv = require('csv-parser');

// Load combined analysis data
const analysisData = JSON.parse(
  fs.readFileSync('team_compare_cities_data_20250717_200559.json')
);
const citiesAnalysis = analysisData.cities_analysis;
const teamSummary = analysisData.team_summary;

// Load team data CSV
const teamData = [];
fs.createReadStream('team_weather_data_20250717_200559.csv')
  .pipe(csv())
  .on('data', (row) => teamData.push(row))
  .on('end', () => {
    console.log(`Loaded ${teamData.length} weather records`);
    // Filter data for specific cities
    const austinData = teamData.filter(row => row.city === 'Austin');
    const providenceData = teamData.filter(row => row.city === 'Providence');
    // Implement your Compare Cities logic here
  });
```

### Method 2: Git Submodules (Advanced)

**Best for**: Teams comfortable with Git, requiring version control of data updates.

#### Initial Setup

```bash
# In your personal capstone project
git submodule add https://github.com/StrayDogSyn/New_Team_Dashboard.git shared-weather-data

# Commit the submodule
git commit -m "Add team weather data as submodule"
git push origin main
```

#### Updating Data

```bash
# Update submodule when team data changes
git submodule update --remote shared-weather-data

# Generate fresh export files
cd shared-weather-data
python main.py

# Commit the update
cd ..
git add shared-weather-data
git commit -m "Update shared weather data to latest version"
git push origin main
```

### Method 3: Direct Download (Simple)

**Best for**: Quick setup, infrequent data updates.

#### Steps

1. **Navigate to GitHub**: Go to the team repository
2. **Browse to exports/**: Find the latest export files
3. **Download files**: Click "Raw" then save the files you need
4. **Place in your project**: Add downloaded files to your capstone project
5. **Import and use**: Follow the Python/JavaScript examples above

## 🏙️ Available Cities for Comparison

Current dataset includes **7 cities** with the following characteristics:

| City | Climate Type | Records | Temperature Range | Key Features |
|------|-------------|---------|------------------|--------------|
| **Austin, TX** | Hot/Humid | 30 | 30.7°C - 42.1°C | High temperatures, varied humidity |
| **Providence, RI** | Northeast | 30 | 20.5°C - 32.2°C | Four-season variation, moderate humidity |
| **Rawlins, WY** | Mountain/Continental | 30 | 14.5°C - 31.2°C | Low humidity, high wind speeds |
| **Ontario, OR** | Pacific Northwest | 30 | 24.8°C - 39.7°C | Dry summers, moderate conditions |
| **New York, NY** | Urban Northeast | 2 | 22.5°C - 24.4°C | Urban heat island effects |
| **Miami, FL** | Tropical/Subtropical | 1 | 28.4°C | High humidity, warm temperatures |
| **New Jersey** | Mid-Atlantic | 102 | 22.2°C - 22.3°C | Consistent moderate temperatures |

## 📈 Compare Cities Implementation Ideas

### Basic Temperature Comparison

```python
def compare_city_temperatures(city_data_dict):
    """Compare average temperatures across cities."""
    for city, data in city_data_dict.items():
        avg_temp = data['temperature'].mean()
        print(f"{city}: {avg_temp:.1f}°C average")
```

### Climate Classification

```python
def classify_climate(city_data):
    """Classify city climate based on temperature and humidity."""
    avg_temp = city_data['temperature'].mean()
    avg_humidity = city_data['humidity'].mean()
    
    if avg_temp > 35:
        return "Hot"
    elif avg_temp > 25:
        return "Warm"
    elif avg_temp > 15:
        return "Moderate"
    else:
        return "Cool"
```

### Weather Pattern Analysis

```python
def analyze_weather_patterns(city_data):
    """Analyze weather condition diversity."""
    conditions = city_data['weather_main'].value_counts()
    return {
        'most_common': conditions.index[0],
        'diversity_score': len(conditions),
        'conditions_distribution': conditions.to_dict()
    }
```

## 🔄 Contributing New Data

### Adding Your Weather Data

1. **Create CSV file**: Format as `weather_data_[YourName].csv`
2. **Place in data/ folder**: Add your file to the repository
3. **Follow format**: Use the standardized CSV structure (see `CSV_FORMATS.md`)
4. **Commit and push**:

```bash
git add data/weather_data_[YourName].csv
git commit -m "Add weather data for [YourName]"
git push origin main
```

### Generating Fresh Exports

After adding new data, generate updated export files:

```bash
python main.py
```

This will create 2 new timestamped export files that include your data:

- `team_weather_data_[timestamp].csv` - Complete dataset for analysis
- `team_compare_cities_data_[timestamp].json` - Combined analysis and city comparisons

## 🛠️ Troubleshooting

### Common Issues

**File format errors**:

- Ensure CSV headers match expected format
- Check for special characters in data
- Verify temperature units (Fahrenheit will be auto-converted)

**Git conflicts**:

- Pull latest changes before adding new data: `git pull origin main`
- Resolve conflicts in CSV files carefully
- Communicate with team about simultaneous updates

**Data inconsistencies**:

- Check `CSV_FORMATS.md` for supported field mappings
- Verify member_name field or use filename convention
- Ensure city names are spelled consistently

### Getting Help

1. **Check documentation**: `README.md`, `CSV_FORMATS.md`, `TEAM_GUIDE.md`
2. **Review examples**: Look at existing files in `data/` folder
3. **Test locally**: Run `python main.py` to verify your data loads correctly
4. **Contact team**: Reach out to repository maintainer for assistance

## 📚 Additional Resources

- **Repository README**: Comprehensive project overview
- **CSV_FORMATS.md**: Detailed format specifications
- **TEAM_GUIDE.md**: Quick collaboration steps
- **Sample files**: `data/sample_weather_data.csv` for reference

## 🎯 Success Criteria

Your Compare Cities implementation should:

- ✅ Load shared team weather data successfully
- ✅ Compare at least 2-3 different cities
- ✅ Analyze temperature, humidity, or weather patterns
- ✅ Present meaningful insights or visualizations
- ✅ Use current export package data for consistency

---

**🌟 Happy coding! Your Compare Cities feature will be powered by real team collaboration data!** 🏙️

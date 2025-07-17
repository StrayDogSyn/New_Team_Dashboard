# 👥 Team CSV Repository Guide

## 🎯 Simple Goal

1. Each team member creates a CSV file with weather data
2. Upload CSV files to this shared repository  
3. Run comparison script to analyze team data

## 📝 Quick Steps

### 1. Add Your CSV File

Create `weather_data_[YourName].csv` in the `data/` folder with this format:

```csv
timestamp,member_name,city,country,temperature,feels_like,humidity,pressure,weather_main,weather_description,wind_speed,wind_direction,cloudiness,visibility,sunrise,sunset,timezone
2025-07-17T14:30:00,YourName,YourCity,US,25.5,27.2,60,1015,Clear,clear sky,3.5,180,10,10.0,06:15,19:45,-5.0
```

### 2. Share With Team

```bash
git add data/weather_data_[YourName].csv
git commit -m "Add weather data for [YourName]"
git push origin main
```

### 3. Get Team Updates

```bash
git pull origin main
python main.py
```

## 📊 What the Script Shows

- Total team members and cities
- Temperature, humidity, and wind ranges  
- Weather conditions across all locations
- Basic statistics for comparison

## 📁 File Structure

```text
data/
├── weather_data_Eric.csv      # 30 days, 4 cities
├── weather_data_[Member].csv  # Your data here
└── sample_weather_data.csv    # Format example
```

## ✅ Requirements

- CSV file in correct format
- Use your name as member_name in all rows
- Include temperature, humidity, weather data
- At least one city/location

## 🚫 Keep It Simple

- No API keys needed
- No complex setup
- Just CSV files and basic Python script
- Focus on data sharing and comparison

---

Simple CSV sharing for team weather comparison! 📊

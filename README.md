# 📊 Team Weather CSV Repository

A bare-bones CSV storage repository for team weather data comparison. Team members upload their CSV files here for shared analysis and comparison.

## 🎯 Purpose

- **Simple CSV storage** for team weather data
- **Basic comparison analysis** across team members' data
- **No complex setup** - just upload and analyze
- **Group collaboration** through shared CSV files

## 📁 Repository Structure

```text
New_Team_Dashboard/
├── data/                          # CSV files from team members
│   ├── weather_data_Eric.csv      # Eric's weather data
│   ├── weather_data_[member].csv  # Other team members' data
│   └── sample_weather_data.csv    # Example format
├── main.py                        # Simple comparison script
├── requirements.txt               # No dependencies needed
└── README.md                      # This file
```

## � Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/StrayDogSyn/New_Team_Dashboard.git
cd New_Team_Dashboard
```

### 2. Run Comparison

```bash
python main.py
```

### 3. Add Your CSV

- Create your CSV file in the `data/` folder
- Follow the format shown in `sample_weather_data.csv`
- Run `main.py` again to see updated team comparison

## 📊 CSV Format

Each CSV file should contain:

```text
timestamp,member_name,city,country,temperature,feels_like,humidity,pressure,weather_main,weather_description,wind_speed,wind_direction,cloudiness,visibility,sunrise,sunset,timezone
```

## 👥 Team Usage

1. **Add your CSV file** to the `data/` folder
2. **Commit and push** your file to the repository
3. **Pull latest changes** to get other team members' data
4. **Run comparison** with `python main.py`

## 📈 What You Get

The comparison script shows:

- Team member count and cities covered
- Temperature ranges and averages across all data
- Humidity and wind speed statistics
- Weather conditions represented
- Total data records

## � Example Output

```text
==================================================
TEAM WEATHER DATA SUMMARY
==================================================
Team Members: 2
Total Cities: 4
Total Records: 120
Cities: Providence, Austin, Rawlins, Ontario
Members: Eric, Sample Member

Temperature Range: 14.5°C to 42.1°C
Average Temperature: 28.3°C

Humidity Range: 16% to 82%
Average Humidity: 42.1%

Wind Speed Range: 1.2 to 8.6 m/s
Average Wind Speed: 4.2 m/s

Weather Conditions: Clear, Clouds, Rain, Snow, Thunderstorm
==================================================
```

## 🤝 Contributing

1. Create your weather CSV file
2. Add it to the `data/` folder
3. Use descriptive filename: `weather_data_[YourName].csv`
4. Commit and push to share with team

---

Simple CSV storage for team weather comparison! 📈

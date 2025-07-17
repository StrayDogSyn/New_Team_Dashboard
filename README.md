# 🌤️ Team Weather Dashboard

A collaborative weather application that generates CSV files for team comparison. Each team member can use this to collect weather data for their city and compare with other team members' data.

## 🎯 Group Project Overview

This application is designed for the **Weather App Group Portion** assignment where:

- Each team member generates a CSV file with weather data from their home city
- All CSV files are shared through this GitHub repository
- Each person's individual project compares their city's weather with all team members' cities
- Implementation can vary between team members while maintaining the shared concept

## 🚀 Features

- **Individual Weather Collection**: Get current weather data for your city
- **CSV Generation**: Automatically save weather data in a standardized CSV format
- **Team Comparison**: Load and analyze all team members' weather data
- **Comprehensive Reports**: Generate detailed comparison reports across the team
- **Environment Security**: Secure API key management using .env files

## 📋 Prerequisites

1. **Python 3.8+**
2. **OpenWeatherMap API Key** (free at [openweathermap.org](https://openweathermap.org/api))
3. **Git** for repository collaboration

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/StrayDogSyn/New_Team_Dashboard.git
cd New_Team_Dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_API_KEY_BACKUP=backup_key_if_available

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
WEATHER_DATABASE_PATH=data/weather_dashboard.db
WEATHER_STORAGE_TYPE=csv
```

### 4. Get Your API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## 🏃‍♂️ Usage

### Running the Application

```bash
python main.py
```

### Interactive Process

1. **Enter your name** (for CSV identification)
2. **Enter your city** (where you want weather data from)
3. **Optional country code** (e.g., 'US', 'UK' for better accuracy)
4. **View current weather** in your terminal
5. **CSV file generated** in the `data/` folder
6. **Team comparison** (if other CSV files are present)

### Example Output

```text
🌤️  TEAM WEATHER DASHBOARD
==================================================
Enter your name: Alice Johnson
Enter your city: New York
Enter country code (optional, e.g., 'US', 'UK'): US

🔄 Getting weather data for New York...

🌡️  Current Weather in New York, US:
   Temperature: 22.5°C (feels like 24.1°C)
   Condition: Clear Sky
   Humidity: 45%
   Wind: 3.2 m/s
   Sunrise: 06:15 | Sunset: 19:45

💾 Data saved to: data/weather_alice_johnson_20250716_143022.csv
```

## 📊 CSV File Format

Each generated CSV contains the following columns:

- `timestamp`: When the data was collected
- `member_name`: Team member's name
- `city`: City name
- `country`: Country code
- `temperature`: Temperature in Celsius
- `feels_like`: Perceived temperature
- `humidity`: Humidity percentage
- `pressure`: Atmospheric pressure
- `weather_main`: Main weather condition
- `weather_description`: Detailed description
- `wind_speed`: Wind speed in m/s
- `wind_direction`: Wind direction in degrees
- `cloudiness`: Cloud coverage percentage
- `visibility`: Visibility in kilometers
- `sunrise`: Sunrise time
- `sunset`: Sunset time
- `timezone`: Timezone offset in hours

## 👥 Team Collaboration

### For Team Members

1. **Run the application** and generate your CSV file
2. **Upload your CSV** to the shared repository's `data/` folder
3. **Pull latest changes** to get other team members' data
4. **Re-run the application** to see team comparisons

### Repository Structure

```text
New_Team_Dashboard/
├── data/                          # CSV files directory
│   ├── weather_alice_20250716.csv
│   ├── weather_bob_20250716.csv
│   └── weather_charlie_20250716.csv
├── main.py                        # Main application
├── requirements.txt               # Dependencies
├── .env                          # Environment variables (not committed)
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🔒 Security Notes

- **Never commit your `.env` file** - it contains your API key
- The `.gitignore` file prevents accidental commits of sensitive data
- Use the `.env.example` file as a template for team members

## 🐛 Troubleshooting

### Common Issues

1. **"API key not found" error**
   - Check your `.env` file exists and contains `OPENWEATHER_API_KEY`
   - Verify the API key is valid at OpenWeatherMap

2. **"City not found" error**
   - Try adding a country code
   - Check city name spelling
   - Use English city names

3. **Import errors**
   - Run `pip install -r requirements.txt`
   - Ensure you're using Python 3.8+

4. **Permission errors**
   - Ensure the `data/` directory is writable
   - Check file permissions

## 🔧 Development

### Project Structure

- `EnvironmentConfig`: Manages API keys and configuration
- `WeatherDashboard`: Main application class
- `main()`: Interactive command-line interface

### Extending the Application

- Add new weather metrics to the CSV format
- Implement additional API providers
- Create visualization features
- Add database storage options

## 📈 Team Comparison Features

When multiple CSV files are present, the application generates:

- **Temperature Analysis**: Hottest/coldest cities, averages, ranges
- **Humidity Comparison**: Humidity levels across locations
- **Wind Analysis**: Wind speeds and patterns
- **Weather Conditions**: Summary of weather types
- **Geographic Coverage**: Countries and cities represented

## 🤝 Contributing

1. Each team member works independently on their implementation
2. Share CSV files through the repository
3. Respect different coding styles and approaches
4. Focus on the shared goal of weather comparison

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for providing the weather API
- Team members for collaboration and data sharing
- Python community for excellent libraries

---

Happy Weather Tracking! 🌟

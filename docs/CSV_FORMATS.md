# 📊 Supported CSV Formats

## 🎯 Flexible Format Support

The team repository now supports multiple CSV formats! Team members can use different column names and the script will automatically normalize the data.

## 📝 Supported Field Mappings

### 🆔 Member Identification

- `member_name` → Direct member name
- **Filename extraction** → `weather_data_[Name].csv` → extracts "Name"

### 📅 Timestamp Fields

- `timestamp`, `Timestamp`, `date`, `Date`, `time`, `Time`

### 🏙️ Location Fields

- **City**: `city`, `City`, `location`, `Location`, `place`, `Place`
- **Country**: `country`, `Country`, `nation`, `Nation`

### 🌡️ Temperature Fields

- `temperature`, `Temperature`, `temp`, `Temp`
- `Temperature (F)`, `Temperature (C)`
- **Auto-conversion**: Fahrenheit → Celsius (when detected)

### 🌤️ Weather Condition Fields

- `weather_description`, `Description`, `description`
- `weather`, `Weather`, `conditions`, `Conditions`

### 💧 Humidity Fields

- `humidity`, `Humidity`, `humid`, `Humid`

### 🌬️ Wind Speed Fields

- `wind_speed`, `Wind Speed`, `wind`, `Wind`, `windspeed`, `WindSpeed`

## ✅ Example Formats

### Format 1: Eric's Standard Format

```csv
timestamp,member_name,city,country,temperature,feels_like,humidity,pressure,weather_main,weather_description,wind_speed,wind_direction,cloudiness,visibility,sunrise,sunset,timezone
2025-07-17T14:30:00,Eric,Austin,US,25.5,27.2,60,1015,Clear,clear sky,3.5,180,10,10.0,06:15,19:45,-5.0
```

### Format 2: Shomari's Simplified Format

```csv
Timestamp,City,Temperature (F),Description
2025-07-08 22:58:02,New York,75.97,clear sky
```

### Format 3: Other Possible Formats

```csv
Date,Location,Temp,Weather,Humidity,Wind
2025-07-17,Boston,72.5,Sunny,45,5.2
```

## 🔄 Automatic Processing

- **Temperature Conversion**: Fahrenheit automatically converted to Celsius
- **Member Name Extraction**: Pulled from filename if not in data
- **Weather Conditions**: Main condition extracted from descriptions
- **Missing Data Handling**: Script continues with available data
- **Format Validation**: Safely handles different column structures

## 📊 Output Statistics

Shows comprehensive comparison including:

- Temperature ranges and averages (in Celsius)
- Humidity data (when available)
- Wind speed data (when available)
- Weather conditions observed
- Cities and countries covered
- Team member participation

---

🚀 **Ready for any CSV format your team uses!**

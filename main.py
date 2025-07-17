#!/usr/bin/env python3
"""
Team Weather Dashboard
=====================
A collaborative weather application that generates CSV files for team comparison.
Each team member can use this to collect weather data for their city and compare
with other team members' data.
"""

import os
import sys
import csv
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import logging
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnvironmentConfig:
    """
    Environment configuration manager for API keys and settings.
    
    This class handles loading and validating environment variables
    from .env files while providing fallback values and error handling.
    """
    
    def __init__(self, env_file: str = '.env'):
        """
        Initialize the environment configuration.
        
        Args:
            env_file (str): Path to the .env file
        """
        self.env_file = env_file
        self.load_environment()
        self.validate_required_keys()
    
    def load_environment(self) -> None:
        """Load environment variables from .env file."""
        env_path = Path(self.env_file)
        
        if env_path.exists():
            load_dotenv(env_path)
            logger.info(f"Successfully loaded environment from {env_path}")
        else:
            logger.warning(f"Environment file {env_path} not found. Using system environment variables only.")
    
    def get_api_key(self, key_name: str, fallback_key: Optional[str] = None) -> Optional[str]:
        """
        Get API key from environment variables with optional fallback.
        
        Args:
            key_name (str): Primary API key name
            fallback_key (str, optional): Fallback API key name
            
        Returns:
            str: API key value or None if not found
        """
        api_key = os.getenv(key_name)
        
        if not api_key and fallback_key:
            api_key = os.getenv(fallback_key)
            if api_key:
                logger.info(f"Using fallback API key: {fallback_key}")
        
        if not api_key:
            logger.error(f"API key not found: {key_name}")
            return None
        
        # Mask API key in logs for security
        masked_key = f"{api_key[:8]}{'*' * (len(api_key) - 12)}{api_key[-4:]}"
        logger.info(f"API key loaded: {key_name} = {masked_key}")
        
        return api_key
    
    def get_config_value(self, key: str, default: Any = None, data_type: type = str) -> Any:
        """
        Get configuration value with type conversion and default fallback.
        
        Args:
            key (str): Environment variable name
            default (Any): Default value if not found
            data_type (type): Expected data type for conversion
            
        Returns:
            Any: Configuration value with proper type
        """
        value = os.getenv(key, default)
        
        if value is None:
            return default
        
        try:
            if data_type == bool:
                return str(value).lower() in ('true', '1', 'yes', 'on')
            elif data_type == int:
                return int(value)
            elif data_type == float:
                return float(value)
            else:
                return str(value)
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to convert {key}={value} to {data_type}: {e}")
            return default
    
    def validate_required_keys(self) -> None:
        """Validate that all required API keys are present."""
        required_keys = [
            'OPENWEATHER_API_KEY',
            # Add other required keys here
        ]
        
        missing_keys = []
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            logger.error(f"Missing required environment variables: {', '.join(missing_keys)}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
    
    def get_all_config(self) -> Dict[str, Any]:
        """
        Get all configuration values as a dictionary.
        
        Returns:
            Dict[str, Any]: All configuration values
        """
        return {
            # API Keys
            'openweather_api_key': self.get_api_key('OPENWEATHER_API_KEY', 'OPENWEATHER_API_KEY_BACKUP'),
            'api_key': self.get_api_key('API_KEY'),
            
            # Database Configuration
            'database_path': self.get_config_value('WEATHER_DATABASE_PATH', 'data/weather_dashboard.db'),
            'storage_type': self.get_config_value('WEATHER_STORAGE_TYPE', 'sql'),
            
            # Application Configuration
            'debug': self.get_config_value('DEBUG', False, bool),
            'log_level': self.get_config_value('LOG_LEVEL', 'INFO'),
            
            # Optional API Keys
            'openai_api_key': self.get_api_key('OPENAI_API_KEY'),
            'google_api_key': self.get_api_key('GOOGLE_API_KEY'),
        }


class WeatherDashboard:
    """
    Main weather dashboard class for collecting and comparing weather data.
    """
    
    def __init__(self, config: EnvironmentConfig):
        """
        Initialize the weather dashboard.
        
        Args:
            config (EnvironmentConfig): Environment configuration instance
        """
        self.config = config
        self.api_key = config.get_api_key('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key is required")
        
        # Create data directory if it doesn't exist
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def get_weather_data(self, city: str, country_code: str = "") -> Dict[str, Any]:
        """
        Get current weather data for a city.
        
        Args:
            city (str): City name
            country_code (str): ISO country code (optional)
            
        Returns:
            Dict[str, Any]: Weather data
        """
        location = f"{city},{country_code}" if country_code else city
        
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully retrieved weather data for {city}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get weather data for {city}: {e}")
            raise
    
    def get_forecast_data(self, city: str, days: int = 5) -> Dict[str, Any]:
        """
        Get 5-day weather forecast for a city.
        
        Args:
            city (str): City name
            days (int): Number of days (max 5 for free API)
            
        Returns:
            Dict[str, Any]: Forecast data
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        try:
            response = requests.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully retrieved forecast data for {city}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get forecast data for {city}: {e}")
            raise
    
    def format_weather_data(self, weather_data: Dict[str, Any], member_name: str) -> Dict[str, Any]:
        """
        Format weather data into a standardized structure.
        
        Args:
            weather_data (Dict[str, Any]): Raw weather data from API
            member_name (str): Name of the team member
            
        Returns:
            Dict[str, Any]: Formatted weather data
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'member_name': member_name,
            'city': weather_data['name'],
            'country': weather_data['sys']['country'],
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'weather_main': weather_data['weather'][0]['main'],
            'weather_description': weather_data['weather'][0]['description'],
            'wind_speed': weather_data.get('wind', {}).get('speed', 0),
            'wind_direction': weather_data.get('wind', {}).get('deg', 0),
            'cloudiness': weather_data['clouds']['all'],
            'visibility': weather_data.get('visibility', 0) / 1000,  # Convert to km
            'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M'),
            'timezone': weather_data['timezone'] / 3600,  # Convert to hours
        }
    
    def save_to_csv(self, weather_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save weather data to CSV file.
        
        Args:
            weather_data (Dict[str, Any]): Formatted weather data
            filename (str, optional): Custom filename
            
        Returns:
            str: Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            member_name = weather_data['member_name'].replace(' ', '_').lower()
            filename = f"weather_{member_name}_{timestamp}.csv"
        
        csv_path = self.data_dir / filename
        
        # Check if file exists to determine if we need headers
        file_exists = csv_path.exists()
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(weather_data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header only if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(weather_data)
        
        logger.info(f"Weather data saved to {csv_path}")
        return str(csv_path)
    
    def load_team_data(self, csv_directory: str = "data") -> List[Dict[str, Any]]:
        """
        Load all CSV files from the team repository.
        
        Args:
            csv_directory (str): Directory containing CSV files
            
        Returns:
            List[Dict[str, Any]]: Combined weather data from all team members
        """
        team_data = []
        csv_dir = Path(csv_directory)
        
        if not csv_dir.exists():
            logger.warning(f"Directory {csv_directory} does not exist")
            return team_data
        
        for csv_file in csv_dir.glob("*.csv"):
            try:
                with open(csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Convert numeric strings back to numbers
                        for key in ['temperature', 'feels_like', 'humidity', 'pressure', 
                                  'wind_speed', 'wind_direction', 'cloudiness', 'visibility', 'timezone']:
                            if key in row and row[key]:
                                try:
                                    row[key] = float(row[key])
                                except ValueError:
                                    pass
                        team_data.append(row)
                
                logger.info(f"Loaded data from {csv_file}")
                
            except Exception as e:
                logger.error(f"Failed to load {csv_file}: {e}")
        
        return team_data
    
    def compare_team_weather(self, team_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare weather data across all team members.
        
        Args:
            team_data (List[Dict[str, Any]]): Weather data from all team members
            
        Returns:
            Dict[str, Any]: Comparison statistics
        """
        if not team_data:
            return {}
        
        # Extract numeric data for comparison
        temperatures = [float(data['temperature']) for data in team_data if data.get('temperature')]
        humidity_levels = [float(data['humidity']) for data in team_data if data.get('humidity')]
        wind_speeds = [float(data['wind_speed']) for data in team_data if data.get('wind_speed')]
        
        comparison = {
            'total_members': len(set(data['member_name'] for data in team_data)),
            'total_cities': len(set(data['city'] for data in team_data)),
            'temperature_stats': {
                'highest': max(temperatures) if temperatures else 0,
                'lowest': min(temperatures) if temperatures else 0,
                'average': sum(temperatures) / len(temperatures) if temperatures else 0,
                'hottest_city': next((data['city'] for data in team_data 
                                    if float(data['temperature']) == max(temperatures)), 'N/A') if temperatures else 'N/A',
                'coldest_city': next((data['city'] for data in team_data 
                                    if float(data['temperature']) == min(temperatures)), 'N/A') if temperatures else 'N/A',
            },
            'humidity_stats': {
                'highest': max(humidity_levels) if humidity_levels else 0,
                'lowest': min(humidity_levels) if humidity_levels else 0,
                'average': sum(humidity_levels) / len(humidity_levels) if humidity_levels else 0,
            },
            'wind_stats': {
                'highest': max(wind_speeds) if wind_speeds else 0,
                'lowest': min(wind_speeds) if wind_speeds else 0,
                'average': sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0,
            },
            'weather_conditions': list(set(data['weather_main'] for data in team_data if data.get('weather_main'))),
            'countries': list(set(data['country'] for data in team_data if data.get('country'))),
        }
        
        return comparison
    
    def generate_comparison_report(self, comparison: Dict[str, Any]) -> str:
        """
        Generate a human-readable comparison report.
        
        Args:
            comparison (Dict[str, Any]): Comparison statistics
            
        Returns:
            str: Formatted report
        """
        if not comparison:
            return "No data available for comparison."
        
        report = f"""
🌤️  TEAM WEATHER DASHBOARD REPORT
=======================================
📊 Overview:
   • Team Members: {comparison['total_members']}
   • Cities Covered: {comparison['total_cities']}
   • Countries: {', '.join(comparison['countries'])}

🌡️  Temperature Analysis:
   • Hottest: {comparison['temperature_stats']['highest']:.1f}°C in {comparison['temperature_stats']['hottest_city']}
   • Coldest: {comparison['temperature_stats']['lowest']:.1f}°C in {comparison['temperature_stats']['coldest_city']}
   • Team Average: {comparison['temperature_stats']['average']:.1f}°C
   • Temperature Range: {comparison['temperature_stats']['highest'] - comparison['temperature_stats']['lowest']:.1f}°C

💧 Humidity Analysis:
   • Highest: {comparison['humidity_stats']['highest']:.0f}%
   • Lowest: {comparison['humidity_stats']['lowest']:.0f}%
   • Team Average: {comparison['humidity_stats']['average']:.1f}%

💨 Wind Analysis:
   • Strongest: {comparison['wind_stats']['highest']:.1f} m/s
   • Calmest: {comparison['wind_stats']['lowest']:.1f} m/s
   • Team Average: {comparison['wind_stats']['average']:.1f} m/s

☁️  Weather Conditions Across Team:
   • {', '.join(comparison['weather_conditions'])}

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return report.strip()


def main():
    """
    Main function for the Team Weather Dashboard.
    """
    try:
        # Initialize environment configuration
        config = EnvironmentConfig()
        
        # Initialize weather dashboard
        dashboard = WeatherDashboard(config)
        
        print("🌤️  TEAM WEATHER DASHBOARD")
        print("=" * 50)
        
        # Get user information
        member_name = input("Enter your name: ").strip()
        if not member_name:
            member_name = "Team Member"
        
        city = input("Enter your city: ").strip()
        if not city:
            print("❌ City name is required!")
            return
        
        country_code = input("Enter country code (optional, e.g., 'US', 'UK'): ").strip()
        
        print(f"\n🔄 Getting weather data for {city}...")
        
        # Get weather data
        weather_data = dashboard.get_weather_data(city, country_code)
        formatted_data = dashboard.format_weather_data(weather_data, member_name)
        
        # Display current weather
        print(f"\n🌡️  Current Weather in {formatted_data['city']}, {formatted_data['country']}:")
        print(f"   Temperature: {formatted_data['temperature']:.1f}°C (feels like {formatted_data['feels_like']:.1f}°C)")
        print(f"   Condition: {formatted_data['weather_description'].title()}")
        print(f"   Humidity: {formatted_data['humidity']}%")
        print(f"   Wind: {formatted_data['wind_speed']:.1f} m/s")
        print(f"   Sunrise: {formatted_data['sunrise']} | Sunset: {formatted_data['sunset']}")
        
        # Save to CSV
        csv_file = dashboard.save_to_csv(formatted_data)
        print(f"\n💾 Data saved to: {csv_file}")
        
        # Load and compare team data
        print(f"\n📊 Loading team comparison data...")
        team_data = dashboard.load_team_data()
        
        if len(team_data) > 1:
            comparison = dashboard.compare_team_weather(team_data)
            report = dashboard.generate_comparison_report(comparison)
            print(report)
            
            # Save comparison report
            report_file = dashboard.data_dir / f"team_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📋 Comparison report saved to: {report_file}")
        else:
            print("\n📝 Add more team member data files to generate comparison reports!")
            print("   Each team member should run this app and share their CSV file.")
        
        print(f"\n✅ Weather dashboard complete!")
        print(f"📁 Check the 'data' folder for CSV files to share with your team.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Weather dashboard interrupted by user.")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
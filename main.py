#!/usr/bin/env python3
"""
Team Weather Data Standardizer
=============================
This script loads all CSV files from the data/ folder, normalizes and standardizes the fields,
and exports a single clean CSV and JSON file for team use.

Usage:
    python main.py

Exports:
    exports/team_weather_data_[timestamp].csv   # Clean, uniform dataset
    exports/team_weather_data_[timestamp].json  # Same data as JSON
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


def normalize_row_data(row: Dict[str, Any], filename: str) -> Dict[str, Any]:
    """
    Normalize different CSV formats to a common structure.
    
    Args:
        row (Dict[str, Any]): Raw row data from CSV
        filename (str): Name of the source CSV file
        
    Returns:
        Dict[str, Any]: Normalized row data
    """
    normalized = {}
    
    # Extract member name from filename if not in data
    if 'member_name' in row and row['member_name']:
        normalized['member_name'] = row['member_name']
    elif 'weather_data_' in filename:
        # Extract name from filename like "weather_data_Eric.csv"
        name_part = filename.replace('weather_data_', '').replace('.csv', '')
        normalized['member_name'] = name_part.capitalize()
    else:
        normalized['member_name'] = 'Unknown'
    
    # Handle different timestamp formats
    timestamp_fields = ['timestamp', 'Timestamp', 'date', 'Date', 'time', 'Time']
    for field in timestamp_fields:
        if field in row and row[field]:
            normalized['timestamp'] = row[field]
            break
    else:
        normalized['timestamp'] = ''
    
    # Handle different city name formats
    city_fields = ['city', 'City', 'location', 'Location', 'place', 'Place']
    for field in city_fields:
        if field in row and row[field]:
            normalized['city'] = row[field]
            break
    else:
        normalized['city'] = ''
    
    # Handle different country formats
    country_fields = ['country', 'Country', 'nation', 'Nation']
    for field in country_fields:
        if field in row and row[field]:
            normalized['country'] = row[field]
            break
    else:
        normalized['country'] = ''
    
    # Handle temperature (convert Fahrenheit to Celsius if needed)
    temp_fields = ['temperature', 'Temperature', 'temp', 'Temp', 'Temperature (F)', 'Temperature (C)']
    for field in temp_fields:
        if field in row and row[field]:
            try:
                temp_value = float(row[field])
                # Convert Fahrenheit to Celsius if the field indicates Fahrenheit
                if '(F)' in field or temp_value > 50:  # Assume >50 is Fahrenheit
                    temp_value = (temp_value - 32) * 5/9
                normalized['temperature'] = round(temp_value, 2)
                break
            except (ValueError, TypeError):
                pass
    
    # Handle weather description
    desc_fields = ['weather_description', 'Description', 'description', 'weather', 'Weather', 'conditions', 'Conditions']
    for field in desc_fields:
        if field in row and row[field]:
            normalized['weather_description'] = row[field]
            normalized['weather_main'] = row[field].split()[0].capitalize() if row[field] else ''
            break
    
    # Handle humidity
    humidity_fields = ['humidity', 'Humidity', 'humid', 'Humid']
    for field in humidity_fields:
        if field in row and row[field]:
            try:
                normalized['humidity'] = round(float(row[field]), 2)
                break
            except (ValueError, TypeError):
                pass
    
    # Handle wind speed
    wind_fields = ['wind_speed', 'Wind Speed', 'wind', 'Wind', 'windspeed', 'WindSpeed']
    for field in wind_fields:
        if field in row and row[field]:
            try:
                normalized['wind_speed'] = round(float(row[field]), 2)
                break
            except (ValueError, TypeError):
                pass
    
    # Copy any other fields that might be useful
    for key, value in row.items():
        if key not in normalized and value:
            normalized[key] = value
    return normalized


def load_and_normalize_all_data(csv_directory: str = "data") -> List[Dict[str, Any]]:
    """
    Load and normalize all CSV files from the data directory.
    Returns a list of standardized row dicts.
    """
    team_data = []
    csv_dir = Path(csv_directory)
    if not csv_dir.exists():
        print(f"Directory {csv_directory} does not exist")
        return []
    for csv_file in csv_dir.glob("*.csv"):
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    normalized_row = normalize_row_data(row, csv_file.name)
                    team_data.append(normalized_row)
            print(f"Loaded {csv_file.name}")
        except Exception as e:
            print(f"Failed to load {csv_file}: {e}")
    return team_data

def export_standardized_data(team_data: List[Dict[str, Any]], output_dir: str = "exports") -> None:
    """
    Export the standardized team data to a single CSV and JSON file.
    """
    export_path = Path(output_dir)
    export_path.mkdir(exist_ok=True)
    csv_filename = "team_weather_data.csv"
    json_filename = f"team_weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    csv_filepath = export_path / csv_filename
    json_filepath = export_path / json_filename

    # Get all unique field names
    all_fields = set()
    for row in team_data:
        all_fields.update(row.keys())
    standard_fields = ['timestamp', 'member_name', 'city', 'country', 'temperature', 'humidity', 'wind_speed', 'weather_main', 'weather_description']
    ordered_fields = [f for f in standard_fields if f in all_fields] + sorted(all_fields - set(standard_fields))

    # Write CSV
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ordered_fields)
        writer.writeheader()
        writer.writerows(team_data)
    print(f"✅ Exported standardized CSV: {csv_filepath}")



def compare_team_data(team_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare weather data across all team members with flexible field handling.
    
    Args:
        team_data (List[Dict[str, Any]]): Weather data from all team members
        
    Returns:
        Dict[str, Any]: Comparison statistics
    """
    if not team_data:
        return {}
    
    # Extract numeric data for comparison (handle missing fields gracefully)
    temperatures = []
    humidity_levels = []
    wind_speeds = []
    
    for data in team_data:
        if 'temperature' in data and data['temperature'] is not None:
            try:
                temperatures.append(float(data['temperature']))
            except (ValueError, TypeError):
                pass
        
        if 'humidity' in data and data['humidity'] is not None:
            try:
                humidity_levels.append(float(data['humidity']))
            except (ValueError, TypeError):
                pass
        
        if 'wind_speed' in data and data['wind_speed'] is not None:
            try:
                wind_speeds.append(float(data['wind_speed']))
            except (ValueError, TypeError):
                pass
    
    # Get unique values with safe extraction
    members = set()
    cities = set()
    countries = set()
    weather_conditions = set()
    
    for data in team_data:
        if data.get('member_name'):
            members.add(data['member_name'])
        if data.get('city'):
            cities.add(data['city'])
        if data.get('country'):
            countries.add(data['country'])
        if data.get('weather_main'):
            weather_conditions.add(data['weather_main'])
        elif data.get('weather_description'):
            # Extract main condition from description if weather_main not available
            main_condition = data['weather_description'].split()[0].capitalize()
            weather_conditions.add(main_condition)
    
    comparison = {
        'total_members': len(members),
        'total_cities': len(cities),
        'total_records': len(team_data),
        'temperature_stats': {
            'count': len(temperatures),
            'highest': max(temperatures) if temperatures else None,
            'lowest': min(temperatures) if temperatures else None,
            'average': sum(temperatures) / len(temperatures) if temperatures else None,
        },
        'humidity_stats': {
            'count': len(humidity_levels),
            'highest': max(humidity_levels) if humidity_levels else None,
            'lowest': min(humidity_levels) if humidity_levels else None,
            'average': sum(humidity_levels) / len(humidity_levels) if humidity_levels else None,
        },
        'wind_stats': {
            'count': len(wind_speeds),
            'highest': max(wind_speeds) if wind_speeds else None,
            'lowest': min(wind_speeds) if wind_speeds else None,
            'average': sum(wind_speeds) / len(wind_speeds) if wind_speeds else None,
        },
        'weather_conditions': sorted(list(weather_conditions)),
        'countries': sorted(list(countries)),
        'cities': sorted(list(cities)),
        'members': sorted(list(members)),
    }
    
    return comparison


def compare_cities_analysis(team_data: List[Dict[str, Any]], cities: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform Compare Cities analysis - core feature for team collaboration.
    
    Args:
        team_data (List[Dict[str, Any]]): Weather data from all team members
        cities (List[str], optional): Specific cities to compare. If None, compares all cities.
        
    Returns:
        Dict[str, Any]: City comparison analysis
    """
    if not team_data:
        return {}
    
    # Filter data by cities if specified
    if cities:
        filtered_data = [row for row in team_data if row.get('city') and row['city'] in cities]
    else:
        filtered_data = team_data
    
    if not filtered_data:
        return {"error": "No data found for specified cities"}
    
    # Group data by city
    city_groups = {}
    for row in filtered_data:
        city = row.get('city', 'Unknown')
        if city not in city_groups:
            city_groups[city] = []
        city_groups[city].append(row)
    
    # Analyze each city
    city_analysis = {}
    for city, city_data in city_groups.items():
        temperatures = []
        humidity_levels = []
        wind_speeds = []
        weather_conditions = set()
        
        for row in city_data:
            if 'temperature' in row and row['temperature'] is not None:
                try:
                    temperatures.append(float(row['temperature']))
                except (ValueError, TypeError):
                    pass
            
            if 'humidity' in row and row['humidity'] is not None:
                try:
                    humidity_levels.append(float(row['humidity']))
                except (ValueError, TypeError):
                    pass
            
            if 'wind_speed' in row and row['wind_speed'] is not None:
                try:
                    wind_speeds.append(float(row['wind_speed']))
                except (ValueError, TypeError):
                    pass
            
            if row.get('weather_main'):
                weather_conditions.add(row['weather_main'])
            elif row.get('weather_description'):
                main_condition = row['weather_description'].split()[0].capitalize()
                weather_conditions.add(main_condition)
        
        city_analysis[city] = {
            'records': len(city_data),
            'temperature': {
                'count': len(temperatures),
                'avg': sum(temperatures) / len(temperatures) if temperatures else None,
                'min': min(temperatures) if temperatures else None,
                'max': max(temperatures) if temperatures else None,
            },
            'humidity': {
                'count': len(humidity_levels),
                'avg': sum(humidity_levels) / len(humidity_levels) if humidity_levels else None,
                'min': min(humidity_levels) if humidity_levels else None,
                'max': max(humidity_levels) if humidity_levels else None,
            },
            'wind': {
                'count': len(wind_speeds),
                'avg': sum(wind_speeds) / len(wind_speeds) if wind_speeds else None,
                'min': min(wind_speeds) if wind_speeds else None,
                'max': max(wind_speeds) if wind_speeds else None,
            },
            'weather_conditions': sorted(list(weather_conditions)),
            'members': list(set(row.get('member_name', 'Unknown') for row in city_data))
        }
    
    return {
        'cities_analyzed': len(city_groups),
        'total_records': len(filtered_data),
        'city_data': city_analysis,
        'comparison_ready': True
    }


def print_compare_cities_summary(analysis: Dict[str, Any]) -> None:
    """
    Print Compare Cities analysis - formatted for team collaboration.
    
    Args:
        analysis (Dict[str, Any]): City comparison analysis
    """
    if not analysis or 'city_data' not in analysis:
        print("❌ No city comparison data available.")
        return
    
    print("\n" + "="*70)
    print("🏙️  COMPARE CITIES ANALYSIS (Team Collaboration Feature)")
    print("="*70)
    print(f"Cities Available for Comparison: {analysis['cities_analyzed']}")
    print(f"Total Records Analyzed: {analysis['total_records']}")
    print()
    
    for city, data in analysis['city_data'].items():
        print(f"📍 {city.upper()}")
        print(f"   Records: {data['records']} | Team Members: {', '.join(data['members'])}")
        
        # Temperature comparison
        if data['temperature']['count'] > 0:
            temp_data = data['temperature']
            print(f"   🌡️  Temperature: {temp_data['avg']:.1f}°C avg (range: {temp_data['min']:.1f}°C to {temp_data['max']:.1f}°C)")
        
        # Humidity comparison  
        if data['humidity']['count'] > 0:
            humid_data = data['humidity']
            print(f"   💧 Humidity: {humid_data['avg']:.1f}% avg (range: {humid_data['min']:.0f}% to {humid_data['max']:.0f}%)")
        
        # Wind comparison
        if data['wind']['count'] > 0:
            wind_data = data['wind']
            print(f"   🌬️  Wind: {wind_data['avg']:.1f} m/s avg (range: {wind_data['min']:.1f} to {wind_data['max']:.1f} m/s)")
        
        # Weather conditions
        if data['weather_conditions']:
            print(f"   🌤️  Conditions: {', '.join(data['weather_conditions'])}")
        
        print()
    
    print("="*70)
    print("✅ Compare Cities data ready for team feature implementation!")
    print("💡 Use load_all_team_data() and compare_cities_analysis() in your projects")
    print("="*70)


def export_team_data_csv(team_data: List[Dict[str, Any]], output_dir: str = "exports") -> str:
    """
    Export normalized team data to CSV format for team member imports.
    
    Args:
        team_data (List[Dict[str, Any]]): Normalized team weather data
        output_dir (str): Directory to save the export file
        
    Returns:
        str: Path to the exported CSV file
    """
    # Create exports directory if it doesn't exist
    export_path = Path(output_dir)
    export_path.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"team_weather_data_{timestamp}.csv"
    csv_filepath = export_path / csv_filename
    
    if not team_data:
        print("❌ No data to export")
        return ""
    
    # Get all unique field names from the data
    all_fields = set()
    for row in team_data:
        all_fields.update(row.keys())
    
    # Define standard field order for better usability
    standard_fields = ['timestamp', 'member_name', 'city', 'country', 'temperature', 'humidity', 'wind_speed', 'weather_main', 'weather_description']
    ordered_fields = []
    
    # Add standard fields first if they exist
    for field in standard_fields:
        if field in all_fields:
            ordered_fields.append(field)
            all_fields.remove(field)
    
    # Add remaining fields
    ordered_fields.extend(sorted(all_fields))
    
    # Write CSV file
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ordered_fields)
        writer.writeheader()
        writer.writerows(team_data)
    
    print(f"✅ Exported team data to: {csv_filepath}")
    print(f"   Records: {len(team_data)} | Fields: {len(ordered_fields)}")
    return str(csv_filepath)


def create_export_package(team_data: List[Dict[str, Any]], cities_analysis: Dict[str, Any], team_summary: Dict[str, Any], output_dir: str = "exports") -> Dict[str, str]:
    """
    Create a simplified export package with essential files for team member imports.
    
    Args:
        team_data (List[Dict[str, Any]]): Normalized team weather data
        cities_analysis (Dict[str, Any]): City comparison analysis
        team_summary (Dict[str, Any]): Team comparison statistics
        output_dir (str): Directory to save export files
        
    Returns:
        Dict[str, str]: Dictionary with export file paths
    """
    print("\n" + "="*70)
    print("📦 CREATING SIMPLIFIED EXPORT PACKAGE FOR TEAM COLLABORATION")
    print("="*70)
    
    export_files = {}
    
    # Clear existing export files first
    export_path = Path(output_dir)
    if export_path.exists():
        for file in export_path.glob("*.csv"):
            file.unlink()
        for file in export_path.glob("*.json"):
            file.unlink()
        print("🧹 Cleared existing export files")
    
    # Export team data CSV (comprehensive dataset)
    csv_path = export_team_data_csv(team_data, output_dir)
    if csv_path:
        export_files['team_data_csv'] = csv_path
    
    # Create combined analysis JSON with all relevant data
    combined_analysis = {
        'cities_analysis': cities_analysis,
        'team_summary': team_summary,
        'export_info': {
            'total_records': len(team_data),
            'cities_available': list(cities_analysis.get('city_data', {}).keys()) if cities_analysis else [],
            'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'usage_note': 'This file contains pre-calculated city comparisons and team statistics for Compare Cities implementation'
        }
    }
    
    # Export combined analysis JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"team_compare_cities_data_{timestamp}.json"
    json_filepath = export_path / json_filename
    
    with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(combined_analysis, jsonfile, indent=2, ensure_ascii=False)
    
    export_files['combined_analysis_json'] = str(json_filepath)
    
    print("\n" + "="*70)
    print("✅ SIMPLIFIED EXPORT PACKAGE COMPLETE!")
    print("="*70)
    print("📁 Team collaboration files created:")
    print(f"   📊 CSV Data: {Path(csv_path).name if csv_path else 'None'}")
    print(f"   📈 JSON Analysis: {Path(json_filepath).name}")
    print(f"   📋 Total Records: {len(team_data)}")
    print(f"   🏙️  Cities Available: {len(cities_analysis.get('city_data', {}))} cities")
    
    print("\n💡 Team members need only these 2 files for Compare Cities implementation!")
    print("="*70)
    
    return export_files


def print_team_summary(comparison: Dict[str, Any]) -> None:
    """
    Print a comprehensive summary of team weather data with flexible field handling.
    
    Args:
        comparison (Dict[str, Any]): Comparison statistics
    """
    if not comparison:
        print("No data available for comparison.")
        return
    
    print("\n" + "="*60)
    print("TEAM WEATHER DATA SUMMARY")
    print("="*60)
    print(f"Team Members: {comparison['total_members']}")
    print(f"Total Cities: {comparison['total_cities']}")
    print(f"Total Records: {comparison['total_records']}")
    print(f"Cities: {', '.join(comparison['cities']) if comparison['cities'] else 'None'}")
    print(f"Members: {', '.join(comparison['members']) if comparison['members'] else 'None'}")
    
    # Temperature statistics
    temp_stats = comparison['temperature_stats']
    print("\n📊 TEMPERATURE DATA:")
    if temp_stats['count'] > 0:
        print(f"  Records with temperature: {temp_stats['count']}")
        print(f"  Range: {temp_stats['lowest']:.1f}°C to {temp_stats['highest']:.1f}°C")
        print(f"  Average: {temp_stats['average']:.1f}°C")
    else:
        print("  No temperature data available")
    
    # Humidity statistics
    humidity_stats = comparison['humidity_stats']
    print("\n💧 HUMIDITY DATA:")
    if humidity_stats['count'] > 0:
        print(f"  Records with humidity: {humidity_stats['count']}")
        print(f"  Range: {humidity_stats['lowest']:.0f}% to {humidity_stats['highest']:.0f}%")
        print(f"  Average: {humidity_stats['average']:.1f}%")
    else:
        print("  No humidity data available")
    
    # Wind statistics
    wind_stats = comparison['wind_stats']
    print("\n🌬️  WIND DATA:")
    if wind_stats['count'] > 0:
        print(f"  Records with wind speed: {wind_stats['count']}")
        print(f"  Range: {wind_stats['lowest']:.1f} to {wind_stats['highest']:.1f} m/s")
        print(f"  Average: {wind_stats['average']:.1f} m/s")
    else:
        print("  No wind speed data available")
    
    # Weather conditions
    print("\n🌤️  WEATHER CONDITIONS:")
    if comparison['weather_conditions']:
        print(f"  Conditions observed: {', '.join(comparison['weather_conditions'])}")
    else:
        print("  No weather condition data available")
    
    # Countries
    if comparison['countries']:
        print(f"\n🌍 COUNTRIES: {', '.join(comparison['countries'])}")
    
    print("="*60)
    print(f"✅ Successfully processed data from {comparison['total_members']} team member(s)")
    print("="*60)


def main():
    """
    Main function to load, standardize, and export all team weather data.
    """
    print("Team Weather Data Standardizer")
    print("Loading and normalizing all team CSV files...")
    team_data = load_and_normalize_all_data()
    if not team_data:
        print("No CSV files found in the data directory.")
        print("Team members should add their weather CSV files to the 'data' folder.")
        return
    export_standardized_data(team_data)
    print("\nDone! Your clean CSV and JSON exports are ready in the exports/ folder.")


if __name__ == "__main__":
    main()
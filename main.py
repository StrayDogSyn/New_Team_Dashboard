#!/usr/bin/env python3
"""
Team Weather Data Repository
===========================
A simple CSV storage repository for team weather data comparison.
Each team member uploads their CSV files here for shared analysis.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Any


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
    if 'member_name' in row:
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
        normalized['timestamp'] = 'Unknown'
    
    # Handle different city name formats
    city_fields = ['city', 'City', 'location', 'Location', 'place', 'Place']
    for field in city_fields:
        if field in row and row[field]:
            normalized['city'] = row[field]
            break
    else:
        normalized['city'] = 'Unknown'
    
    # Handle different country formats
    country_fields = ['country', 'Country', 'nation', 'Nation']
    for field in country_fields:
        if field in row and row[field]:
            normalized['country'] = row[field]
            break
    else:
        normalized['country'] = 'Unknown'
    
    # Handle temperature (convert Fahrenheit to Celsius if needed)
    temp_fields = ['temperature', 'Temperature', 'temp', 'Temp', 'Temperature (F)', 'Temperature (C)']
    for field in temp_fields:
        if field in row and row[field]:
            try:
                temp_value = float(row[field])
                # Convert Fahrenheit to Celsius if the field indicates Fahrenheit
                if '(F)' in field or temp_value > 50:  # Assume >50 is Fahrenheit
                    temp_value = (temp_value - 32) * 5/9
                normalized['temperature'] = temp_value
                break
            except (ValueError, TypeError):
                pass
    
    # Handle weather description
    desc_fields = ['weather_description', 'Description', 'description', 'weather', 'Weather', 'conditions', 'Conditions']
    for field in desc_fields:
        if field in row and row[field]:
            normalized['weather_description'] = row[field]
            normalized['weather_main'] = row[field].split()[0].capitalize()  # First word as main condition
            break
    
    # Handle humidity
    humidity_fields = ['humidity', 'Humidity', 'humid', 'Humid']
    for field in humidity_fields:
        if field in row and row[field]:
            try:
                normalized['humidity'] = float(row[field])
                break
            except (ValueError, TypeError):
                pass
    
    # Handle wind speed
    wind_fields = ['wind_speed', 'Wind Speed', 'wind', 'Wind', 'windspeed', 'WindSpeed']
    for field in wind_fields:
        if field in row and row[field]:
            try:
                normalized['wind_speed'] = float(row[field])
                break
            except (ValueError, TypeError):
                pass
    
    # Copy any other fields that might be useful
    for key, value in row.items():
        if key not in normalized and value:
            normalized[key] = value
    
    return normalized


def load_all_team_data(csv_directory: str = "data") -> List[Dict[str, Any]]:
    """
    Load all CSV files from the team repository with format normalization.
    
    Args:
        csv_directory (str): Directory containing CSV files
        
    Returns:
        List[Dict[str, Any]]: Combined and normalized weather data from all team members
    """
    team_data = []
    csv_dir = Path(csv_directory)
    
    if not csv_dir.exists():
        print(f"Directory {csv_directory} does not exist")
        return team_data
    
    for csv_file in csv_dir.glob("*.csv"):
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                file_count = 0
                
                for row in reader:
                    # Normalize the row data to handle different formats
                    normalized_row = normalize_row_data(row, csv_file.name)
                    team_data.append(normalized_row)
                    file_count += 1
            
            print(f"Loaded {file_count} records from {csv_file}")
            
        except Exception as e:
            print(f"Failed to load {csv_file}: {e}")
    
    return team_data


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
    Main function to load and display team weather data comparison.
    """
    print("Team Weather Data Repository")
    print("Loading all team CSV files...")
    
    # Load all team data
    team_data = load_all_team_data()
    
    if not team_data:
        print("\nNo CSV files found in the data directory.")
        print("Team members should add their weather CSV files to the 'data' folder.")
        return
    
    # Generate and display comparison
    comparison = compare_team_data(team_data)
    print_team_summary(comparison)


if __name__ == "__main__":
    main()
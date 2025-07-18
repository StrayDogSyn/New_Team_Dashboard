#!/usr/bin/env python3
"""
Team Weather Data Repository
===========================
A simple CSV storage repository for team weather data comparison.
Each team member uploads their CSV files here for shared analysis.
"""

import csv
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


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
    from datetime import datetime
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


def export_cities_analysis_json(cities_analysis: Dict[str, Any], output_dir: str = "exports") -> str:
    """
    Export Compare Cities analysis to JSON format for team member imports.
    
    Args:
        cities_analysis (Dict[str, Any]): City comparison analysis
        output_dir (str): Directory to save the export file
        
    Returns:
        str: Path to the exported JSON file
    """
    # Create exports directory if it doesn't exist
    export_path = Path(output_dir)
    export_path.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"compare_cities_analysis_{timestamp}.json"
    json_filepath = export_path / json_filename
    
    if not cities_analysis or 'city_data' not in cities_analysis:
        print("❌ No cities analysis data to export")
        return ""
    
    # Write JSON file with pretty formatting
    with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(cities_analysis, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported cities analysis to: {json_filepath}")
    print(f"   Cities: {cities_analysis.get('cities_analyzed', 0)} | Records: {cities_analysis.get('total_records', 0)}")
    return str(json_filepath)


def export_team_summary_json(team_summary: Dict[str, Any], output_dir: str = "exports") -> str:
    """
    Export team summary statistics to JSON format for team member imports.
    
    Args:
        team_summary (Dict[str, Any]): Team comparison statistics
        output_dir (str): Directory to save the export file
        
    Returns:
        str: Path to the exported JSON file
    """
    # Create exports directory if it doesn't exist
    export_path = Path(output_dir)
    export_path.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"team_summary_{timestamp}.json"
    json_filepath = export_path / json_filename
    
    if not team_summary:
        print("❌ No team summary data to export")
        return ""
    
    # Write JSON file with pretty formatting
    with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(team_summary, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported team summary to: {json_filepath}")
    print(f"   Members: {team_summary.get('total_members', 0)} | Cities: {team_summary.get('total_cities', 0)}")
    return str(json_filepath)


def export_city_specific_csv(team_data: List[Dict[str, Any]], city_name: str, output_dir: str = "exports") -> str:
    """
    Export data for a specific city to CSV format for targeted analysis.
    
    Args:
        team_data (List[Dict[str, Any]]): Normalized team weather data
        city_name (str): Name of the city to filter and export
        output_dir (str): Directory to save the export file
        
    Returns:
        str: Path to the exported CSV file
    """
    # Create exports directory if it doesn't exist
    export_path = Path(output_dir)
    export_path.mkdir(exist_ok=True)
    
    # Filter data for specific city
    city_data = [row for row in team_data if row.get('city', '').lower() == city_name.lower()]
    
    if not city_data:
        print(f"❌ No data found for city: {city_name}")
        return ""
    
    # Generate filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_city_name = city_name.replace(' ', '_').replace(',', '').lower()
    csv_filename = f"{safe_city_name}_weather_data_{timestamp}.csv"
    csv_filepath = export_path / csv_filename
    
    # Get all unique field names from the city data
    all_fields = set()
    for row in city_data:
        all_fields.update(row.keys())
    
    # Define standard field order
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
        writer.writerows(city_data)
    
    print(f"✅ Exported {city_name} data to: {csv_filepath}")
    print(f"   Records: {len(city_data)} | Fields: {len(ordered_fields)}")
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
    from datetime import datetime
    
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
    Main function to load, display team weather data comparison, show Compare Cities analysis, and create export packages.
    """
    print("Team Weather Data Repository")
    print("Loading all team CSV files...")
    
    # Load all team data
    team_data = load_all_team_data()
    
    if not team_data:
        print("\nNo CSV files found in the data directory.")
        print("Team members should add their weather CSV files to the 'data' folder.")
        return
    
    # Generate and display general comparison
    comparison = compare_team_data(team_data)
    print_team_summary(comparison)
    
    # Generate and display Compare Cities analysis
    print("\n" + "🏙️" * 25)
    cities_analysis = compare_cities_analysis(team_data)
    print_compare_cities_summary(cities_analysis)
    
    # Create export package for team member imports
    export_files = create_export_package(team_data, cities_analysis, comparison)
    
    # Print usage instructions for team members
    print("\n" + "="*70)
    print("📚 TEAM MEMBER IMPORT INSTRUCTIONS")
    print("="*70)
    print("Python import examples:")
    print()
    print("# Import complete team data CSV")
    print("import pandas as pd")
    print("team_data = pd.read_csv('exports/team_weather_data_[timestamp].csv')")
    print()
    print("# Import combined analysis JSON")
    print("import json")
    print("with open('exports/team_compare_cities_data_[timestamp].json', 'r') as f:")
    print("    analysis_data = json.load(f)")
    print("    cities_analysis = analysis_data['cities_analysis']")
    print("    team_summary = analysis_data['team_summary']")
    print()
    print("# Quick city comparison example")
    print("austin_data = team_data[team_data['city'] == 'Austin']")
    print("providence_data = team_data[team_data['city'] == 'Providence']")
    print("print(f'Austin avg temp: {austin_data[\"temperature\"].mean():.1f}°C')")
    print("print(f'Providence avg temp: {providence_data[\"temperature\"].mean():.1f}°C')")
    print("="*70)


if __name__ == "__main__":
    main()
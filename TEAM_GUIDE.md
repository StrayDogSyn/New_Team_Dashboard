# 👥 Team Collaboration Guide

## 🎯 Project Goal

Each team member will:

1. Generate a CSV file with weather data from their home city
2. Share CSV files through this repository
3. Compare weather across all team cities

## 📝 Step-by-Step Instructions

### For Each Team Member

#### 1. Setup (One-time)

```bash
# Clone the repository
git clone https://github.com/StrayDogSyn/New_Team_Dashboard.git
cd New_Team_Dashboard

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
# (On Mac/Linux: cp .env.example .env)

```

#### 2. Generate Your Weather Data

```bash
# Run the application
python main.py

# Follow prompts:
# - Enter your name
# - Enter your city
# - Optional: country code for accuracy
```

#### 3. Share Your Data

```bash
# Add your CSV file to git
git add data/weather_[yourname]_*.csv

# Commit with descriptive message
git commit -m "Add weather data for [Your City]"

# Push to shared repository
git push origin main
```

#### 4. Get Team Updates

```bash
# Pull latest team data
git pull origin main

# Run app again to see comparisons
python main.py
```

## 📊 What Gets Generated

### Individual CSV File

- `data/weather_[yourname]_[timestamp].csv`
- Contains comprehensive weather data for your city
- Standardized format for team comparison

### Team Comparison Report

When multiple CSV files exist:

- Temperature analysis across all cities
- Humidity, wind, and weather condition comparisons
- Automatic report generation
- Saved as `team_comparison_[timestamp].txt`

## 🔄 Workflow Example

```text
Alice (NYC) → Generates weather_alice_20250716.csv → Pushes to repo
Bob (London) → Pulls Alice's data → Generates weather_bob_20250716.csv → Pushes
Charlie (Tokyo) → Pulls all data → Generates weather_charlie_20250716.csv → Pushes
David (Sydney) → Pulls all data → Sees full team comparison
```

## 📁 Expected Repository Structure

```text
New_Team_Dashboard/
├── data/
│   ├── weather_alice_20250716_143022.csv
│   ├── weather_bob_20250716_150315.csv
│   ├── weather_charlie_20250716_152045.csv
│   ├── weather_david_20250716_154230.csv
│   └── team_comparison_20250716_160000.txt
├── main.py
├── requirements.txt
├── .env (individual, not shared)
├── .env.example (template)
└── README.md
```

## 🚨 Important Notes

### ✅ DO

- Add your CSV files to the repository
- Use descriptive commit messages
- Pull before working to get latest team data
- Keep your .env file private

### ❌ DON'T

- Commit your .env file (contains your API key)
- Modify other team members' CSV files
- Change the main.py structure drastically (variations are fine)

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'requests'"**

   ```bash
   pip install -r requirements.txt
   ```

2. **"API key not found"**
   - Check your .env file exists
   - Verify OPENWEATHER_API_KEY is set correctly

3. **Git conflicts**

   ```bash
   git pull --rebase origin main
   ```

4. **City not found**
   - Add country code (e.g., "London, UK")
   - Check spelling

## 💡 Tips for Success

### Team Communication

- Coordinate when to collect data (same time for better comparison)
- Share interesting findings in your city's weather
- Discuss different implementation approaches

### Technical Tips

- Run the app multiple times to see how data accumulates
- Check the generated reports for insights
- Experiment with different cities if you want

## 🏆 Project Success Criteria

✅ Each team member has generated a CSV file
✅ All CSV files are in the shared repository
✅ Team comparison reports are generated
✅ Each person can see weather data from all team cities
✅ Individual implementations show creativity while maintaining core concept

---

Remember: The goal is collaboration, not perfection! 🌟

import json
import csv

# Load JSON data
with open('dynasty_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare CSV file
with open('dynasty_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    
    # Header
    header = [
        "ID", "Name", "Period", "Start Year", "End Year", "Duration", 
        "Capital", "Key Figures", "Territory", 
        "Fall Trigger", "Structural Contradiction", "External Pressure",
        "Conquest Victor", "Conquest Loser", "Decisive Battle", "Winning Factor",
        "Population (Million)", "Temp Anomaly", "War Frequency"
    ]
    writer.writerow(header)
    
    # Rows
    for d in data:
        row = [
            d['id'],
            d['name'],
            d['period'],
            d['start_year'],
            d['end_year'],
            d['duration'],
            ", ".join(d['capital']),
            ", ".join(d['key_figures']),
            d['territory'],
            d['fall_analysis']['trigger'],
            d['fall_analysis']['structural'],
            d['fall_analysis']['external'],
            d.get('conquest_chain', {}).get('victor', ''),
            d.get('conquest_chain', {}).get('loser', ''),
            d.get('conquest_chain', {}).get('battle', ''),
            d.get('conquest_chain', {}).get('factor', ''),
            d['stats']['population_million'],
            d['stats']['temperature_anomaly'],
            d['stats']['war_frequency']
        ]
        writer.writerow(row)

print("CSV generation complete.")

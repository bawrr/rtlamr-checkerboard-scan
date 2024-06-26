import os
import json
import re
import csv


# Configuration
log_directory = "./"
pattern = re.compile(r"log_(\d+)_(\d+).txt")
detailed_csv = "summary_results.csv"
executive_csv = "executive_summary_results.csv"

# Dictionary to store results
results = {}

# Function to process a single log file
def process_log_file(filepath):
    filename = os.path.basename(filepath)
    match = pattern.search(filename)
    if not match:
        return  # Skip files that don't match the pattern
    
    frequency, gain = map(int, match.groups())
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            if "Message" in data:
                message = data["Message"]
                if "EndpointID" in message:
                    id_key = message["EndpointID"]
                elif "ID" in message:
                    id_key = message["ID"]
                else:
                    continue
                
                if id_key not in results:
                    results[id_key] = []

                results[id_key].append((frequency, gain))

# Process all log files in the directory
for log_file in os.listdir(log_directory):
    if log_file.endswith(".txt"):
        process_log_file(os.path.join(log_directory, log_file))

# Summarize results
detailed_summary = []
executive_summary = {}

for id_key, occurrences in results.items():
    unique_files = set(occurrences)
    count = len(unique_files)
    executive_summary[id_key] = count
    for freq_gain in unique_files:
        detailed_summary.append([id_key, count, freq_gain[0], freq_gain[1]])

# Save detailed summary to CSV
with open(detailed_csv, mode='w', newline='') as csv_file:
    fieldnames = ['ID', 'Count', 'Frequency', 'Gain']
    writer = csv.writer(csv_file)

    writer.writerow(fieldnames)
    for row in detailed_summary:
        writer.writerow(row)

# Save executive summary to CSV
with open(executive_csv, mode='w', newline='') as csv_file:
    fieldnames = ['ID', 'Count']
    writer = csv.writer(csv_file)

    writer.writerow(fieldnames)
    for id_key, count in executive_summary.items():
        writer.writerow([id_key, count])

print(f"Detailed summary saved to {detailed_csv}")
print(f"Executive summary saved to {executive_csv}")
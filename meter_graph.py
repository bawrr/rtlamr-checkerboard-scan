import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load the detailed summary CSV
detailed_csv = "./summary_results.csv"
df = pd.read_csv(detailed_csv)

# Get unique IDs
unique_ids = df['ID'].unique()

# Directory to save heatmap images
output_dir = "heatmaps"
os.makedirs(output_dir, exist_ok=True)

# Function to create a heatmap for each ID
def create_heatmap(df, id_key, output_dir):
    # Filter data for the given ID
    df_id = df[df['ID'] == id_key]
    
    # Define the range for frequencies and gains
    freq_range = np.arange(902000000, 928500000, 500000)  # from 902 MHz to 928 MHz
    gain_range = np.arange(0, 50)  # from 1 dB to 49 dB
    
    # Create a grid for the heatmap
    grid = np.zeros((len(freq_range), len(gain_range)))
    
    # Fill the grid with 1 where signal was detected
    for _, row in df_id.iterrows():
        if row['Frequency'] in freq_range and row['Gain'] in gain_range:
            freq_idx = np.where(freq_range == row['Frequency'])[0][0]
            gain_idx = np.where(gain_range == row['Gain'])[0][0]
            grid[freq_idx, gain_idx] = 1
    
    # Plot the heatmap
    plt.figure(figsize=(20, 20))
    plt.imshow(grid, cmap='Reds', interpolation='nearest', aspect='auto')
    plt.xticks(np.arange(len(gain_range)), gain_range, rotation=90, fontsize=12)
    plt.yticks(np.arange(len(freq_range)), freq_range, fontsize=12)
    plt.xlabel('Gain (dB)', fontsize=14)
    plt.ylabel('Frequency (Hz)', fontsize=14)
    plt.title(f'Heatmap for ID {id_key}', fontsize=16)
    
    # Save the heatmap
    output_path = os.path.join(output_dir, f"heatmap_{id_key}.png")
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()

# Create heatmaps for each ID
for id_key in unique_ids:
    create_heatmap(df, id_key, output_dir)

print(f"Heatmaps saved in {output_dir}")

